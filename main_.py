import torch
from transformers import AutoTokenizer
from diffusers import (
    AutoencoderKL,
    DDPMScheduler,
    UNet2DConditionModel,
)

from config import *
from utils import *
import torch
import yaml
from PIL import Image
from torchvision import transforms

# Set the parameters

with open('Config.yaml', 'rb') as f:
    conf = yaml.safe_load(f.read())    # load the config file
hps = get_amnet_config(conf)




# ---------------------------------------------------------------------------------------
torch.manual_seed(25)
device = "cuda" if torch.cuda.is_available() else "cpu"
height = hps.height   # default height of Stable Diffusion
width = hps.width   # default width of Stable Diffusion
num_inference_steps = hps.num_inference_steps  # Number of denoising steps
g1 = hps.g1   # Scale for  guidance prompt1
g2 = hps.g2    # Scale for  guidance with original image
bs = hps.bs  # batch size of the input prompts
step = hps.step    #step of noise. we do not start from pure noise. we start from the last steps that already an image is added a little bit of noise
Image_Path = hps.Image_Path # address of the image that we suppose to add noise to it
prompt = hps.prompt 
output_path = hps.output_path 
#-----------------------------------------------------------------------------------------



# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    hps.pretrained_model_name_or_path,
    subfolder="tokenizer",    
    use_fast=False,
)


## Import models

# import correct text encoder class
text_encoder_cls = import_model_class_from_model_name_or_path(hps.pretrained_model_name_or_path,hps.revision)
text_encoder = text_encoder_cls.from_pretrained(
    hps.pretrained_model_name_or_path, subfolder="text_encoder",revision=hps.revision, variant=hps.variant)
# Load scheduler and models
noise_scheduler = DDPMScheduler.from_pretrained(hps.pretrained_model_name_or_path, subfolder="scheduler")
# Load unet pre-trained check points
unet = UNet2DConditionModel.from_pretrained(hps.pretrained_model_name_or_path, subfolder="unet").to(device)
# Load vae model for latent space
vae = AutoencoderKL.from_pretrained(
            hps.pretrained_model_name_or_path, subfolder="vae", revision=hps.revision, variant=hps.variant
        ).to(device)

vae.to(device)
    




def input_image_to_memo_score(prompt):


    # call the CLIP model and extract the unconditional language emmbedding for the empty prompt
    input_var_1 =  compute_text_embeddings([""],tokenizer,text_encoder,hps.tokenizer_max_length)
    control_1 = input_var_1.to(device)
  
    # Converting  prompts to conditioned embedding through CLIP model
    pre_computed_encoder_hidden_states1 = compute_text_embeddings(prompt,tokenizer,text_encoder,hps.tokenizer_max_length).to(device)
    
    
    # Adding an unconditional prompt to the conditioned prompt , helps in the generation process
    emb = torch.cat([control_1, pre_computed_encoder_hidden_states1])
    
    
    
    # Get input image and add noise to it ---------------------------------------------------
    im = Image.open(Image_Path)
    newsize = (height, width)
    im = im.resize(newsize)
    im = im.convert('RGB')
    transform = transforms.Compose([ 
    transforms.PILToTensor()
    ]) 
    norm = transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)) 
    im = transform(im).to(device) 
    im = im/255
    im = norm(im)
    im = im.unsqueeze(0)
    im = im.to(device)

    
    # give the image to vae model to transfer it to the latent space
    if vae is not None:
        vae.requires_grad_(False)
        weight_dtype = torch.float32
        # Convert images to latent space
        model_input = vae.encode(im.to(dtype=weight_dtype)).latent_dist.sample()
        model_input = model_input * vae.config.scaling_factor

    noise = torch.randn_like(model_input) * noise_scheduler.init_noise_sigma
    noise_scheduler.set_timesteps(num_inference_steps)    
    # Add noise to the model input according to the noise magnitude at each timestep
    # (this is the forward diffusion process)
    noisy_model_input = noise_scheduler.add_noise(model_input, noise, noise_scheduler.timesteps)
    # -------------------------------------------------------------------------------------------------------

    # The image is added noise in different timesteps. We can choose the added level of the noise by choosing step parameter
    
    # input of the  diffusion model
    latents = torch.randn(
        (bs, unet.config.in_channels, height // 8, width // 8),    
        device=device
    )
    # give the image with added noise as the input image
    latents[0] = noisy_model_input[step]
    count = -1
    for t in noise_scheduler.timesteps[step:]:        
        count += 1
        # expand the latents if we are doing classifier-free guidance to avoid doing two forward passes.
        latent_model_input = torch.cat([latents] * 2)
        # predict the noise residual
        with torch.no_grad():
            noise_pred1 = unet(latent_model_input, t, encoder_hidden_states=emb).sample
            # noise guidence regarding the original image
            noise_pred2 = noisy_model_input[step + count] - model_input #unet(latent_model_input, t, encoder_hidden_states=emb2).sample

        # perform guidance by the prompt
        noise_pred_uncond, noise_pred_text1 = noise_pred1.chunk(2)
        noise_pred_text2 = noise_pred2

        print(torch.min(noise_pred_text2), torch.max(noise_pred_text2),torch.min(noise_pred_text1), torch.max(noise_pred_text1) )
        
        if count<5:
            noise_pred = noise_pred_uncond + g1 * (noise_pred_text1 - noise_pred_uncond)+ g2 * (noise_pred_text2 - noise_pred_uncond)
        else:
            noise_pred = noise_pred_uncond + g1 * (noise_pred_text1 - noise_pred_uncond)

        # compute the previous noisy sample x_t -> x_t-1
        latents = noise_scheduler.step(noise_pred, t, latents).prev_sample
        latent_to_pil(latents,vae,output_path)
            

    return 





input_image_to_memo_score(prompt)





