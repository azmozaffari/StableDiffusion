# Ads Generator

The gole of this project is to generate ads by given few number of images of a specific brand. In this project, instead of describing the ad scene in text, I use a sample image. The model uses the scene image and just replaces the similar item with a brand item.

I have used [DreamBooth](https://github.com/google/dreambooth) to train a StableDiffusion model with few number of AppleWatch photos. Later, the trained model in models folder would be copied in the root folder of this project.

To run the project set the parameters like given input image address and in config.yaml file and run main_.py 

Some samples are provided as below for apple watch example.

In the left row the sample ad image is given to the generative model that is trained with few samples of the apple watch and the model generate the similar image with replacing the presented watch in the image with the apple watch. the generated image is demonstrated in the left colomn.

<img src="./steps/in1.jpg" width="350" height="350"> <img src="./steps/out1.jpg" width="350" height="350">
<img src="./steps/in2.jpg" width="350" height="350"> <img src="./steps/out2.jpg" width="350" height="350">
<img src="./steps/in6.jpg" width="350" height="350"> <img src="./steps/out6.jpg" width="350" height="350">
<img src="./steps/in7.jpg" width="350" height="350"> <img src="./steps/out7.jpg" width="350" height="350">
<img src="./steps/in8.jpg" width="350" height="350"> <img src="./steps/out8.jpg" width="350" height="350">
<img src="./steps/in11.jpg" width="350" height="350"> <img src="./steps/out11.jpg" width="350" height="350">
<img src="./steps/in12.jpg" width="350" height="350"> <img src="./steps/out12.jpg" width="350" height="350">
<img src="./steps/in13.jpg" width="350" height="350"> <img src="./steps/out13.jpg" width="350" height="350">
