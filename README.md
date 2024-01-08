# Ads Generator

The goal of this project is to generate ads given few images of a specific item that we are going to generate ads about. In this project, instead of describing the ad scene in the text (prompt), I use a sample scene image as the description example. Sometimes it is hard for us to explain every detail of the scene that we are going to create. The model uses the sample given scene image and recreates the scene with the specific item.

I have used [DreamBooth](https://github.com/google/dreambooth) to train a StableDiffusion model with few samples of the specific item that I have. Here my samples were Apple watch and DARA doll. Then the stable diffusion is capable of generating the items.

Given the sample scene image and prompting with just the brand item name like Apple watch or DARA doll, I am capable of creating new images with the theme of the given scene image.

Some samples are provided below. In the left colomn, the sample ad scene images are given. the generated image is demonstrated in the right column.


<img src="./steps/in1.jpg" width="350" height="350"> <img src="./steps/out1.jpg" width="350" height="350">
<img src="./steps/in2.jpg" width="350" height="350"> <img src="./steps/out2.jpg" width="350" height="350">
<img src="./steps/in6.jpg" width="350" height="350"> <img src="./steps/out6.jpg" width="350" height="350">
<img src="./steps/in7.jpg" width="350" height="350"> <img src="./steps/out7.jpg" width="350" height="350">
<img src="./steps/in8.jpg" width="350" height="350"> <img src="./steps/out8.jpg" width="350" height="350">
<img src="./steps/in11.jpg" width="350" height="350"> <img src="./steps/out11.jpg" width="350" height="350">
<img src="./steps/in12.jpg" width="350" height="350"> <img src="./steps/out12.jpg" width="350" height="350">
<img src="./steps/in13.jpg" width="350" height="350"> <img src="./steps/out13.jpg" width="350" height="350">


## How to run?
pip install -r requirements. txt

Go to the DreamBooth page download the code and train the model with the desired item images.

Copy the model folder to the main root folder of the project.

Use the Config.yaml file to adjust the hyperparameters to reproduce the images in a way that you like.

All the parameters are defined in Config.yaml file like input and output images' addresses.

Run main_.py

