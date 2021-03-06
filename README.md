# MVA-minimum-variance-algorithm


## What is the MVA? ##

The MVA is an algorithm that, given one or multiple 'objects', each with their own data set, is able to find the weights to allocate to each object.

The weights are allocated following this idea: The less volatile, the more weight.

## Description of repository ##

This repository mainly contains two python files.
One file is the code for the MVA.
The other one is an example of how such code can be implemented in a program.

Since I first used the MVA to calculate the weights of some financial securities in a personal project, these files describe how the MVA works in this particular field.
It is however possible to 'generalise' the MVA, i.e. extrapolate the idea of how it works and implement it in many other fields.

## Important ##

These files are provided 'as is' and they will not work out-of-the-box, but they need to be adapted one's specific needs and software usage.

The files are written in Python and will require some libraries to function correctly.

More detailed information about which libraries are necessary and other specific information can be found inside the related file.

## A little bit more about the MVA ##

The MVA simply finds the average covariance of each asset versus all other assets - including its own variance - and then converts the average value for each asset to a cross-sectional distribution using normalization. This is used to proportionately weight each asset to find an initial set of weights.
The final weights are derived by multiplying each initial asset weight by its inverse variance and then releveraging to sum up the weights to a total of 100%.

The result is that weights reflect both the asset’s own relative variance and also average covariance to the universe of assets.
However, the weights are less dependent on correlation estimates (which are critical in complex minimum variance but are noisier than volatility estimates) and do a better job of distributing risk since allocations are made to all assets in the universe.

## Credits ##

The development of this MVA algorithm would have not been possible without the many open source information, files and works that people are willing to share.
This is the main reason why I am 'giving back' what I have learned, and I hope this small project will help many others.

For more info about the sources, have a look at the CREDITS file.
