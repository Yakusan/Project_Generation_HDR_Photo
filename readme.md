# Project: Generation of HDR Photograph.

A scholar project which contains a set of python scripts generating HDR image from aligned LDR photographs.

We first use the Debevec's algorithm to retrieve the Camera response curve ie: "Recovering High Dynamic Range Radiance Maps from Photographs" research paper of Debevec et al [97] depending on given exposure time and pixel intensity sampling.
Then, we use the camera response function that we recovered to build the radiance map and generate a raw HDR image thanks to the following formula.

![Alt text](https://github.com/Yakusan/CHPS0932_TP2_HDR/blob/master/radiance_map_formula.jpg)

However, we can also calculate the weighted average of the current radiance map with the reference image having the middle exposure value to generate a final HDR image.

We can summarize the process as the schema below.

![Alt text](https://github.com/Yakusan/CHPS0932_TP2_HDR/blob/master/HDR_generation_steps.jpg)

Which give us the following result without tone mapping:

![Alt text](https://github.com/Yakusan/CHPS0932_TP2_HDR/blob/master/result/aligned_adjusted_HDR.hdr)