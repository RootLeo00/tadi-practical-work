dilation inflates bright areas and deflate dark areas
erosion inflates dark areas and deflates bright areas
opening (anti-extensive=removes parts of an object) =    erosion + dilation --> darkens narrow bright zones
closing (extensive=add parts of an object) = dilation + erosion --> brightens narrow dark zones

dilation and opening deform corners which are convex () on the bright side
erosion and closing deform cornners which are convex () on the dark side

filters obtained by composing opening and closing can be used to remove objects smaller than the structuring element

erosion and dilation are duals + opening and closing are duals --> if you invert the 
gray level of the image and apply, for example, opening you get the same result as closing on the original image

opening by reconstruction = erosion + reconstruction --> removes (white) objects smaller than the structuring element
closing by reconstruction = dilation + reconstruction --> removes (black) objects smaller than the structuring element

alternate sequential filters = opening by reconstruction + closing by reconstruction ---> progrssively removes grains (white) and pores (dark) of increasing size -->simplify image
