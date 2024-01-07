from PIL import Image 
import torch
from transformers import  PretrainedConfig
try:
    import cv2
except:
    print("WARNING: Could not load OpenCV python package. Some functionality may not be available.")


def import_model_class_from_model_name_or_path(pretrained_model_name_or_path: str, revision: str):
    text_encoder_config = PretrainedConfig.from_pretrained(
        pretrained_model_name_or_path,
        subfolder="text_encoder",
        revision=revision,
    )
    model_class = text_encoder_config.architectures[0]

    if model_class == "CLIPTextModel":
        from transformers import CLIPTextModel

        return CLIPTextModel
    elif model_class == "RobertaSeriesModelWithTransformation":
        from diffusers.pipelines.alt_diffusion.modeling_roberta_series import RobertaSeriesModelWithTransformation

        return RobertaSeriesModelWithTransformation
    elif model_class == "T5EncoderModel":
        from transformers import T5EncoderModel

        return T5EncoderModel
    else:
        raise ValueError(f"{model_class} is not supported.")


def tokenize_prompt(tokenizer, prompt, tokenizer_max_length=None):
    if tokenizer_max_length is not None:
        max_length = tokenizer_max_length
    else:
        max_length = tokenizer.model_max_length

    text_inputs = tokenizer(
        prompt,
        truncation=True,
        padding="max_length",
        max_length=max_length,
        return_tensors="pt",
    )

    return text_inputs


def encode_prompt(text_encoder, input_ids, attention_mask, text_encoder_use_attention_mask=None):
    text_input_ids = input_ids.to(text_encoder.device)

    if text_encoder_use_attention_mask:
        attention_mask = attention_mask.to(text_encoder.device)
    else:
        attention_mask = None

    prompt_embeds = text_encoder(
        text_input_ids,
        attention_mask=attention_mask,
    )
    prompt_embeds = prompt_embeds[0]

    return prompt_embeds


def compute_text_embeddings(prompt,tokenizer,text_encoder,tokenizer_max_length):
    with torch.no_grad():
        text_inputs = tokenize_prompt(tokenizer, prompt, tokenizer_max_length)
        prompt_embeds = encode_prompt(
            text_encoder,
            text_inputs.input_ids,
            text_inputs.attention_mask,
            text_encoder_use_attention_mask=False,
        )

    return prompt_embeds


def latent_to_pil(latents, vae,output_path):
    '''
    Function to convert latents to images
    '''
    latents = (1 / 0.18215) * latents

    image = vae.decode(latents).sample.to("cuda")
    image = (image / 2 + 0.5).clamp(0, 1)


    im = image.clone()
    im = im.detach().cpu().permute(0, 2, 3, 1).numpy()
    image = (image * 255).round()
    im = (im * 255).round().astype("uint8")[0]


    pil_images = Image.fromarray(im) 
    pil_images.save(output_path)
    return 