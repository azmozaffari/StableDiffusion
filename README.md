# Ad Generator

The goal of this project is to generate advertisement images about specific brand items using StableDiffusion model. 
Generative models like SD are usually general-purpose models and are not trained to reproduce specific brand items. Then the first challenge in this project is to fine-tune the model with a few samples that after fine-tuning it still can reproduce high-quality images of that brand in variant shapes. The next challenge is prompting. Sometimes to reach an acceptable result, we really should know how to ask the model by a good prompting.

To address the fine-tuning challenge, I have used [DreamBooth](https://github.com/google/dreambooth) approach to retrain a StableDiffusion model with few samples of the specific item. Here my samples are DARA&SARA doll. The fine-tuned StableDiffusion model is capable of generating the items in variant viewpoints.

<img src="./steps/darasara.jpg" width="350" height="350">


To address the prompting challenge, instead of describing the scene by the text (prompt), I want to use a sample scene image as a description. Here, ControlNet cannot be a good choice as we need to re-train the model for new given style images.

I have added a guidance gradient term to the denoising process of SD. Like the classifier-free guidance approach, that the captioned image is used as a guide for the denoising process, I have used a noised input image as a guide for the only 5 beginning denoising steps with the declining weight. The weights of these two guidance terms are considered as the hyperparameters. 

Given the sample scene image and prompting shortly like DARA&SARA doll, I am capable of creating new images with the theme of the given scene image.

Some samples are provided below. In the left column, the sample ad scene images are given. the generated images are demonstrated in the right column.


<img src="./steps/in11.jpg" width="350" height="350"> <img src="./steps/out11.jpg" width="350" height="350">
<img src="./steps/in12.jpg" width="350" height="350"> <img src="./steps/out12.jpg" width="350" height="350">
<img src="./steps/in13.jpg" width="350" height="350"> <img src="./steps/out13.jpg" width="350" height="350">
<img src="./steps/in14.jpg" width="350" height="350"> <img src="./steps/out14.jpg" width="350" height="350">


## How to run?
pip install -r requirements. txt

Go to the DreamBooth page download the code and follow the instructions to train the model with the desired item images and given prompt.

Copy the trained model folder to the root folder of the project.

Use the Config.yaml file to adjust the hyperparameters to reproduce the images in a way that you like.

All the parameters are defined in Config.yaml file like input and output images' addresses, denoising steps, prompt,starting denoising timestamps, similarity scales g1 and g2 which are the weights to adjust the similarity to the prompt and scene image, respectively.

Run main_.py

