# Ads Generator

The gole of this project is to generate ads by given few number of images of a specific brand. In this project, instead of describing the ad in text to generate the sample, we use a sample image and just replace the similar item with a brand item.

I have used DreamBooth https://github.com/google/dreambooth to train a StableDiffusion model with few number of AppleWatch photos. 


Some samples are provided as below for apple watch.

In the left row the sample ad image is given to the generative model that is trained with few samples of the apple watch and the model generate the similar image with replacing the presented watch in the image with the apple watch. the generated image is demonstrated in the left colomn.

<img src="./steps/in1.jpg" width="450" height="450"> <img src="./steps/out1.jpg" width="450" height="450">
<img src="./steps/in2.jpg" width="450" height="450"> <img src="./steps/out2.jpg" width="450" height="450">
<img src="./steps/in6.jpg" width="450" height="450"> <img src="./steps/out6.jpg" width="450" height="450">
<img src="./steps/in7.jpg" width="450" height="450"> <img src="./steps/out7.jpg" width="450" height="450">
<img src="./steps/in8.jpg" width="450" height="450"> <img src="./steps/out8.jpg" width="450" height="450">
