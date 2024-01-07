import os
import numpy as np
import torch
from torch.autograd import Variable
import pkg_resources

class HParameters:

    def __init__(self):
        self.use_cuda = True
        self.cuda_device = 0
        return


def get_amnet_config(args):

    hps = HParameters()


    # Diffusion model setting
    hps.pretrained_model_name_or_path = args["pretrained_model_name_or_path"]
    hps.revision = args["revision"]
    hps.variant = args["variant"]
    hps.tokenizer_name = args["tokenizer_name"]
    # hps.instance_prompt = args["instance_prompt"]
    hps.tokenizer_max_length = args["tokenizer_max_length"]
    hps.text_encoder_use_attention_mask = args["text_encoder_use_attention_mask"],
    hps.height = args["height"]   # default height of Stable Diffusion
    hps.width = args["width"]   # default width of Stable Diffusion
    hps.num_inference_steps = args["num_inference_steps"]  # Number of denoising steps
    hps.g1 = args["g1"]   # Scale for classifier-free guidance
    hps.g2 = args["g2"]   # Scale for classifier-free guidance
    hps.bs = args["bs"]  # batch size of the input prompts
    hps.step = args["step"]    #step of noise. we do not start from pure noise. we start from the last steps that already an image is added a little bit of noise
    hps.Image_Path = args["Image_Path"] # address of the image that we suppose to add noise to it
    hps.prompt = args["prompt"] 
    hps.output_path = args["output_path"] 




    return hps

