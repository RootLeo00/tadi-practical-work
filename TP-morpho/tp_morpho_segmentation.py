#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct 2023
@author: Caterina Leonelli, Kimia Sadreddini
"""

#%% SECTION 1 -- inclusion of packages

import numpy as np
import matplotlib.pyplot as plt
from skimage import io as skio
from skimage import exposure

import skimage.morphology as morpho
from skimage.segmentation import watershed
from skimage.draw import line
import skimage.feature as skf
import skimage.color as color
from skimage import measure
from utils import *

#%% load images

# Binary images
# im = skio.imread('cellbin.bmp')
# im = skio.imread('cafe.bmp')

# Gray-scale images
#im = skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/retina2.gif')

im = skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/bat200.bmp')

# im = skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/bulles.bmp')

#im = grayscale_from_color(skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/cailloux.png'))
#im = grayscale_from_color(skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/cailloux2.png'))
# im = skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/laiton.bmp')

# for retina2.gif 
# print(im.shape)
# im = im[0,:, :]
# print(im.shape)


if len(im.shape)>2 and im.shape[2] == 3:
    im=grayscale_from_color(im)
    
plt.imshow(im, cmap="gray", vmin=0, vmax=255)
plt.show()
# viewimage(im) - Usable instead of plt.imshow if GIMP is installed.


#%% SECTION SEGMENTATION

# 1) Compute the morphological gradient (dilation - erosion with an elementary structuring
# element, of size 1), for instance on image bat200.bmp. Comment the results.

shape ="disk"
size = 1
se = strel(shape,size)

# compute morpho gradient
morpho_grad = morpho.dilation(im, se) - morpho.erosion(im, se)
morpho_grad = np.int32(morpho_grad > 40) * morpho_grad # manual thresholding
plt.imshow(morpho_grad, cmap="gray")
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/exsegm_1_morphograd_{shape}_{size}_threshold.png')

# %% 2)Compute the watershed on this gradient image (see the corresponding section in the code).
# Comment the results. For the visualization, the watershed lines 
# (having value 0 in the result) can be superimposed on the original image.

# Generate the markers
inverted_morpho_grad = 255 - morpho_grad
peak_idx_local_mini = skf.peak_local_max(inverted_morpho_grad)
peak_mask = np.zeros_like(inverted_morpho_grad, dtype=bool)
peak_mask[tuple(peak_idx_local_mini.T)] = True
markers, _ = measure.label(peak_mask, return_num = True)

# compute the watershed
labels = watershed(morpho_grad, markers, watershed_line=True)
plt.title("Watershed labels") 
plt.imshow(random_colors(labels))
plt.show()

# Visualization of the result
segm = labels.copy()
for i in range(segm.shape[0]):
    for j in range(segm.shape[1]):
        if segm[i, j] == 0:
            segm[i, j] = 255
        else:
            segm[i, j] = 0
# Superimposition of segmentation contours on the original image
contourSup = np.maximum(segm, im)
plt.imshow(contourSup, cmap="gray")
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/exsegm_5_watershed_{shape}_{size}.png')


# %% 3) Try to improve the result by filtering the original image by an appropriate morphological
# filter and/or by filtering the gradient image by a closing, before computing the watersheds.

# apply closing by reconstruction
im_preprocessed = morpho.closing(im, strel("disk", 2))
im_preprocessed = morpho.reconstruction(im_preprocessed, im, method='erosion')
plt.title("Image preprocessed")  
plt.imshow(im_preprocessed, cmap="gray")
plt.show()

# compute morpho gradient
morpho_grad = morpho.dilation(im_preprocessed, strel("disk",1)) - morpho.erosion(im_preprocessed, strel("disk",1))
morpho_grad = np.int32(morpho_grad > 40) * morpho_grad # manual thresholding

#apply closing to the gradient
morpho_grad = morpho.closing(morpho_grad, strel('disk', 1)) 
plt.title("Morphological gradient after closing")  
plt.imshow(morpho_grad, cmap="gray")
plt.show()

# Generate the markers
inverted_morpho_grad = 255 - morpho_grad
peak_idx_local_mini = skf.peak_local_max(inverted_morpho_grad)
peak_mask = np.zeros_like(inverted_morpho_grad, dtype=bool)
peak_mask[tuple(peak_idx_local_mini.T)] = True
markers, _ = measure.label(peak_mask, return_num = True)

# compute the watershed
labels = watershed(morpho_grad, markers, watershed_line=True)
plt.title("Watershed labels") 
plt.imshow(random_colors(labels))
plt.show()

# Visualization of the result
segm = labels.copy()
for i in range(segm.shape[0]):
    for j in range(segm.shape[1]):
        if segm[i, j] == 0:
            segm[i, j] = 255
        else:
            segm[i, j] = 0
# Superimposition of segmentation contours on the original image
contourSup = np.maximum(segm, im)
plt.title("Watershed segmentation")  
plt.imshow(contourSup, cmap="gray")
plt.show()
plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/exsegm_3_watershed_im_preprocess.png')

# %% 4.1) Eliminate regional minima with a dynamic less that some value before applying the water-
# shed. Explain the sequence of operations and comment the results.

#load image
im = skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/laiton.bmp')
if len(im.shape)>2 and im.shape[2] == 3:
    im=grayscale_from_color(im)
plt.title("Original image")
plt.imshow(im, cmap="gray")
plt.show()

# compute gradient and threshold
morpho_grad = morpho.dilation(im, strel("disk",1)) - morpho.erosion(im, strel("disk",1))
morpho_grad = np.int32(morpho_grad > 10) * morpho_grad # manual thresholding: the 5 eliminates the shadows
plt.title("Morphological gradient")
plt.imshow(morpho_grad, cmap="gray")
plt.show()

# for each pixel, add some fixed value
morpho_grad_with_max = morpho_grad + 50
#apply reconstruction
morpho_grad = morpho.reconstruction(morpho_grad,morpho_grad_with_max)
plt.title("Reconstruction")
plt.imshow(morpho_grad, cmap="gray")
plt.show()

# compute markers
inverted_morpho_grad = 255 - morpho_grad
peak_idx_local_mini = skf.peak_local_max(inverted_morpho_grad)
peak_mask = np.zeros_like(inverted_morpho_grad, dtype=bool)
peak_mask[tuple(peak_idx_local_mini.T)] = True
markers, _ = measure.label(peak_mask, return_num = True)

# # compute the watershed
labels = watershed(morpho_grad, markers, watershed_line=True)
plt.title("Watershed labels")
plt.imshow(random_colors(labels))
plt.show()

# Visualization of the result
segm = labels.copy()
for i in range(segm.shape[0]):
    for j in range(segm.shape[1]):
        if segm[i, j] == 0:
            segm[i, j] = 255
        else:
            segm[i, j] = 0
# Superimposition of segmentation contours on the original image
contourSup = np.maximum(segm, im)
plt.title("Watershed segmentation")
plt.imshow(contourSup, cmap="gray")
plt.show()
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/exsegm_6_watershed_{shape}_{size}.png')

# %% 5) Watersheds constraint by markers (on bulles.bmp)

im = skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/bulles.bmp')

if len(im.shape)>2 and im.shape[2] == 3:
    im=grayscale_from_color(im)
    
plt.imshow(im, cmap="gray", vmin=0, vmax=255)
plt.show()

#Define markers (manually or using a dedicated pre-processing)
# Let m be the marker, such that m takes value 0 in the marked regions and 255 elsewhere
# For this example, let's create markers manually (you can define your own logic)
# ATT! the x and y coordinates are inverted in the image
markers_inside = np.zeros_like(im)
markers_inside += 255
markers_inside[58:92,42:47] = 0  # Region inside the object
markers_inside[135:161,122:130] = 0  # Region inside the object
markers_inside[173:180, 154:156] = 0  # Region inside the object
markers_inside[181:190,172:176] = 0  # Region inside the object
markers_inside[214:224,121:125] = 0  # Region inside the object
markers_outside = np.zeros_like(im)
markers_outside += 255
# markers_outside[0:252, 0] = 0  # Region outside the object : Border
# markers_outside[0:252, 254] = 0  # Region outside the object: Border
# markers_outside[0, 0:254] = 0  # Region outside the object:     Border
# markers_outside[252, 0:254] = 0  # Region outside the object:  Border
markers_outside[0:255,0:36] = 0
markers_outside[0:255,55:116] = 0
markers_outside[0:255,136:150] = 0
markers_outside[0:255,163:169] = 0
markers_outside[0:255,180:253] = 0
markers_outside[0:46,0:255] = 0
markers_outside[106:123, 0:255] = 0
markers_outside[202:207, 0:255] = 0
markers_outside[231:255, 0:255] = 0


# Combine the markers
# keep all the 0 values from markers_inside and markers_outside
markers = np.minimum(markers_inside, markers_outside)
plt.imshow(markers, cmap="gray")
plt.show()


# compute gradient
morpho_grad = morpho.dilation(im, strel("disk",1)) - morpho.erosion(im, strel("disk",1))
morpho_grad = np.int32(morpho_grad > 5) * morpho_grad # manual thresholding: the 5 eliminates the shadows
plt.imshow(morpho_grad, cmap="gray")
plt.show()

# Compute I' = I ∧ m where I is the
# image on which we want to compute the watershed 
# (e.g. gradient, or the inverted image
# in the case of laiton.bmp, etc.)
im_and_markers = np.minimum(morpho_grad, markers)
plt.imshow(im_and_markers, cmap="gray")
plt.show()

# Reconstruct I' by erosion from m
im_reconstructed = morpho.reconstruction(im_and_markers, markers)

# The reconstructed image should have minima only in the regions defined by m
# plot to see this
plt.imshow(im_reconstructed, cmap="gray")
plt.show()

# Compute the watersheds of the reconstructed image
peak_mask = np.zeros_like(morpho_grad, dtype=bool)
peak_mask[markers==0] = True
markers, _ = measure.label(peak_mask, return_num = True)

labels = watershed(im_reconstructed, markers, watershed_line=True)
plt.imshow(random_colors(labels))

# Visualization of the result
segm = labels.copy()
for i in range(segm.shape[0]):
    for j in range(segm.shape[1]):
        if segm[i, j] == 0:
            segm[i, j] = 255
        else:
            segm[i, j] = 0
# Superimposition of segmentation contours on the original image
contourSup = np.maximum(segm, im)
plt.imshow(contourSup, cmap="gray")
plt.show()
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/exsegm_4_watershed.png')

# %% 6) How could the watersheds be used to segment the black lines in image bulles.bmp or
# laiton.bmp? Discuss the different steps of the method you propose.

#load image
im = skio.imread('/home/leo/github/tadi-practical-work/TP-morpho/Images/laiton.bmp')
if len(im.shape)>2 and im.shape[2] == 3:
    im=grayscale_from_color(im)
plt.title("Original image")
plt.imshow(im, cmap="gray")
plt.show()


# compute bottomhat
im_preprocessed = im
im_closing = morpho.closing(im_preprocessed, strel("disk", 15))
im_preprocessed = im_closing - im_preprocessed # bottomhat
plt.title("Image preprocessed - bottomhat")
plt.imshow(im_preprocessed, cmap="gray")
plt.show()
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/4.6/exsegm_6_bottomhat.png')


# opening by reconstruction
im_open = morpho.opening(im_preprocessed, strel("disk", 3))
im_preprocessed = morpho.reconstruction(im_open, im_preprocessed)
plt.title("Image preprocessed - opening by reconstruction")
# plt.figure(figsize=(5,5))
plt.imshow(im_preprocessed, cmap="gray")
plt.show()
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/4.6/exsegm_6_open_by_recon.png')


morpho_grad = np.int32(im_preprocessed > 12) * im_preprocessed # manual thresholding 
plt.title("Image preprocessed - threshold")
plt.imshow(im_preprocessed, cmap="gray")
plt.show()
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/4.6/exsegm_6_threshold.png')

# invert the image in order to have the lines as maxima
inverted_morpho_grad = 255 - morpho_grad
peak_idx_local_mini = skf.peak_local_max(inverted_morpho_grad) #indices=False NO LONGER AVAILABLE!!!! , min_distance=40
peak_mask = np.zeros_like(inverted_morpho_grad, dtype=bool)
peak_mask[tuple(peak_idx_local_mini.T)] = True
markers, _ = measure.label(peak_mask, return_num = True)

# compute the watershed
labels = watershed(morpho_grad, markers, watershed_line=True)
plt.title("Watershed labels")
plt.imshow(random_colors(labels))
plt.show()
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/4.6/exsegm_6_watershed_labels.png')


# Visualization of the result
segm = labels.copy()
for i in range(segm.shape[0]):
    for j in range(segm.shape[1]):
        if segm[i, j] == 0:
            segm[i, j] = 255
        else:
            segm[i, j] = 0
# Superimposition of segmentation contours on the original image
contourSup = np.maximum(segm, im)
plt.title("Watershed segmentation")
plt.imshow(contourSup, cmap="gray")
plt.show()
# plt.savefig(f'/home/leo/github/tadi-practical-work/TP-morpho/results/4.6/exsegm_6_watershed_lines.png')

