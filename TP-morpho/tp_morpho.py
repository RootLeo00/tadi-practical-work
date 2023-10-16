#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 10:23:50 2018
Modified Oct 2020, Oct 2021, Oct 2023
@author: Said Ladjal, Isabelle Bloch
"""

#%% SECTION 1 -- inclusion of packages

import numpy as np
import platform
import tempfile
import os
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import io as skio

import skimage.morphology as morpho
from skimage.segmentation import watershed
from skimage.draw import line
import skimage.feature as skf
from scipy import ndimage as ndi

#%% SECTION 2 -- Useful functions

def viewimage(im, normalize=True, MINI=0.0, MAXI=255.0):
    """
    This function displays the image in grayscale in GIMP. If GIMP is already open, it will be used.
    By default, normalize is set to True. In this case, the image is normalized between 0 and 255 before saving.
    If normalize is set to False, MINI and MAXI will be set to 0 and 255 in the resulting image.
    """
    imt = np.float32(im.copy())
    if platform.system() == 'Darwin':  # macOS
        prephrase = 'open -a GIMP '
        endphrase = ' '
    elif platform.system() == 'Linux':
        prephrase = 'gimp '
        endphrase = ' &'
    elif platform.system() == 'Windows':
        prephrase = 'start /B "D:/GIMP/bin/gimp-2.10.exe" -a '  # Replace 'D:/...' with your GIMP's path
        endphrase = ''
    else:
        print('System not supported for GIMP display')
        return 'display error'

    if normalize:
        m = imt.min()
        imt = imt - m
        M = imt.max()
        if M > 0:
            imt = imt / M
    else:
        imt = (imt - MINI) / (MAXI - MINI)
        imt[imt < 0] = 0
        imt[imt > 1] = 1

    nomfichier = tempfile.mktemp('TPIMA.png')
    commande = prephrase + nomfichier + endphrase
    skio.imsave(nomfichier, imt)
    os.system(commande)

def viewimage_color(im, normalize=True, MINI=0.0, MAXI=255.0):
    """
    This function displays the image in grayscale in GIMP. If GIMP is already open, it will be used.
    By default, normalize is set to True. In this case, the image is normalized between 0 and 255 before saving.
    If normalize is set to False, MINI (default 0) and MAXI (default 255) will be set to 0 and 255 in the resulting image.
    """
    imt = np.float32(im.copy())
    if platform.system() == 'Darwin':  # macOS
        prephrase = 'open -a GIMP '
        endphrase = ' '
    elif platform.system() == 'Linux':
        prephrase = 'gimp '
        endphrase = ' &'
    elif platform.system() == 'Windows':
        prephrase = 'start /B "D:/GIMP/bin/gimp-2.10.exe" -a '  # Replace 'D:/...' with your GIMP's path
        endphrase = ''
    else:
        print('System not supported for GIMP display')
        return 'display error'

    if normalize:
        m = imt.min()
        imt = imt - m
        M = imt.max()
        if M > 0:
            imt = imt / M
    else:
        imt = (imt - MINI) / (MAXI - MINI)
        imt[imt < 0] = 0
        imt[imt > 1] = 1

    nomfichier = tempfile.mktemp('TPIMA.pgm')
    commande = prephrase + nomfichier + endphrase
    skio.imsave(nomfichier, imt)
    os.system(commande)

def strel(shape, size, angle=45):
    """
    Returns a structuring element of the specified shape and size.
    'diamond' returns a closed diamond-shaped element of radius 'size'.
    'disk' returns a closed disk-shaped element of radius 'size'.
    'square' returns a square-shaped element of size 'size' (it's better to use an odd size).
    'line' returns a line segment of length 'size' and angle 'angle' (0 to 180 degrees).
    (This function is not standard in Python)
    """
    if shape == 'diamond':
        return morpho.diamond(size)
    if shape == 'disk':
        return morpho.disk(size)
    if shape == 'square':
        return morpho.square(size)
    if shape == 'line':
        angle = int(-np.round(angle))
        angle = angle % 180
        angle = np.float32(angle) / 180.0 * np.pi
        x = int(np.round(np.cos(angle) * size))
        y = int(np.round(np.sin(angle) * size))
        if x**2 + y**2 == 0:
            if abs(np.cos(angle)) > abs(np.sin(angle)):
                x = int(np.sign(np.cos(angle)))
                y = 0
            else:
                y = int(np.sign(np.sin(angle)))
                x = 0
        rr, cc = line(0, 0, y, x)
        rr = rr - rr.min()
        cc = cc - cc.min()
        img = np.zeros((rr.max() + 1, cc.max() + 1))
        img[rr, cc] = 1
        return img
    raise RuntimeError('Error in the strel function: Unrecognized shape')

def random_colors(im):
    """
    Assigns random colors to a grayscale image. This function is useful when grayscale is interpreted as region numbers
    or for visualizing slight grayscale variations.
    """
    sh = im.shape
    out = np.zeros((sh[0], sh[1], 3), dtype=np.uint8)
    num_colors = np.int32(im.max())
    color_table = np.random.randint(0, 256, size=(num_colors + 1, 3))
    color_table[0, :] = 0
    for k in range(sh[0]):
        for l in range(sh[1]):
            out[k, l, :] = color_table[im[k, l]]
    return out

def grayscale_from_color(im):
    """
    Transforms a color image into a grayscale image.
    """
    return im[:, :, :3].sum(axis=2) / 3

structuring_elements_list= ['disk', 'diamond', 'square', 'line']
sizes= [4,8]

#%% load images

# Binary images
# im = skio.imread('cellbin.bmp')
# im = skio.imread('cafe.bmp')

# Gray-scale images
#im = skio.imread('/home/leo/tadi/TP-morpho/Images/retina2.gif')

#im = skio.imread('/home/leo/tadi/TP-morpho/Images/bat200.bmp')

#im = skio.imread('/home/leo/tadi/TP-morpho/Images/bulles.bmp')
#im = grayscale_from_color(skio.imread('/home/leo/tadi/TP-morpho/Images/cailloux.png'))
#im = grayscale_from_color(skio.imread('/home/leo/tadi/TP-morpho/Images/cailloux2.png'))
im = skio.imread('/home/leo/tadi/TP-morpho/Images/laiton.bmp')

# for retina2.gif 
# print(im.shape)
# im = im[0,:, :]
# print(im.shape)

    
if len(im.shape)>2 and im.shape[2] == 3:
    im=grayscale_from_color(im)
    
plt.imshow(im, cmap="gray", vmin=0, vmax=255)
# viewimage(im) - Usable instead of plt.imshow if GIMP is installed.


#%% SECTION 3 -- Examples of functions for this work

for struct_el in structuring_elements_list:
    for size in sizes:
        se = strel(struct_el, size)

        # Dilation
        dil = morpho.dilation(im, se)
        plt.imshow(dil, cmap="gray", vmin=0, vmax=255)
        plt.savefig(f'/home/leo/tadi/TP-morpho/results/dil_{struct_el}_{size}.png')

        # Erosion
        ero = morpho.erosion(im, se)
        plt.imshow(ero, cmap="gray", vmin=0, vmax=255)
        plt.savefig(f'/home/leo/tadi/TP-morpho/results/ero_{struct_el}_{size}.png')

        # Opening
        open = morpho.opening(im, se)
        plt.imshow(open, cmap="gray", vmin=0, vmax=255)
        plt.savefig(f'/home/leo/tadi/TP-morpho/results/open_{struct_el}_{size}.png')

        # Closing
        close = morpho.closing(im, se)
        plt.imshow(close, cmap="gray", vmin=0, vmax=255)
        plt.savefig(f'/home/leo/tadi/TP-morpho/results/close_{struct_el}_{size}.png')

#%% SECTION 3.3.1 -- succession of a dilation by a square of size 3×3 and a dilation by a square of size 5 × 5 / opening

# successive dilations
# Dilation 3x3
dil = morpho.dilation(im, strel('square', 3))
# Dilation 5x5
dil = morpho.dilation(dil, strel('square', 5))
plt.imshow(dil, cmap="gray", vmin=0, vmax=255)
plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex3_successivedils_dil_{struct_el}_{size}.png')

# sum of dilations
# Dilation 8x8
dil = morpho.dilation(im, strel('square', 8))
plt.imshow(dil, cmap="gray", vmin=0, vmax=255)
plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex3_sumofdils_dil_{struct_el}_{size}.png')


# successive openings
# Opening 3x3
dil = morpho.opening(im, strel('square', 3))
# Opening 5x5
dil = morpho.opening(dil, strel('square', 5))
plt.imshow(dil, cmap="gray", vmin=0, vmax=255)
plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex3_successiveopen_open_{struct_el}_{size}.png')

# sum of openings
# Opening 8x8
dil = morpho.opening(im, strel('square', 8))
plt.imshow(dil, cmap="gray", vmin=0, vmax=255)
plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex3_sumofopen_open_{struct_el}_{size}.png')


#%% Top-hat transform
im = skio.imread('/home/leo/tadi/TP-morpho/Images/retina2.gif')
print(im.shape)
im = im[0,:, :]
print(im.shape)

sizes = [4, 8, 10,20]
angles = [0, 45, 90, 135]
for struct_el in structuring_elements_list:
    for size in sizes:
        if struct_el == 'line':
            for angle in angles:
                se = strel(struct_el, size, angle)
                ch = im - morpho.opening(im, se)
                plt.imshow(ch, cmap="gray", vmin=0, vmax=255)
                plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex4_tophat_{struct_el}_{size}_{angle}.png')
        
        else:
                se = strel(struct_el, size)
                ch = im - morpho.opening(im, se)
                plt.imshow(ch, cmap="gray", vmin=0, vmax=255)
                plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex4_tophat_{struct_el}_{size}.png')

# %%  
# interesting result: take all the image results of a top-hat of the same image with the same structuring element line, size but different angles, compute the max of all of them for each pixel 
# and then display the result. It's a bit like a top-hat with a line of size 20 but with a better result.
im = skio.imread('/home/leo/tadi/TP-morpho/Images/retina2.gif')
print(im.shape)
im = im[0,:, :]
print(im.shape)

shape= 'line'
size = 10
ch= []
for angle in angles:
    se = strel(shape, size, angle)
    ch.append(im - morpho.opening(im, se))

# for every image in ch (ch is a list of images), take the max of all the images for each pixel
i = range (0, len(ch))
for i in range (0, len(ch)):
    if i == len(ch)-1:
        break
    else:
        res= np.maximum(ch[i], ch[i+1])
plt.imshow(res, cmap="gray", vmin=0, vmax=255)
plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex4_tophat_max_{struct_el}_{size}_{angle}.png')

#%% - dual operation: bottom-hat transform
im = skio.imread('/home/leo/tadi/TP-morpho/Images/laiton.bmp')
if len(im.shape)>2 and im.shape[2] == 3:
    im=grayscale_from_color(im)

sizes = [4, 8, 10,20]
angles = [0, 45, 90, 135]
for struct_el in structuring_elements_list:
    for size in sizes:
        if struct_el == 'line':
            for angle in angles:
                se = strel(struct_el, size, angle)
                ch = morpho.closing(im, se) -im
                plt.imshow(ch, cmap="gray", vmin=0, vmax=255)
                plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex4_bottomhat_{struct_el}_{size}_{angle}.png')
        
        else:
                se = strel(struct_el, size)
                ch =  morpho.closing(im, se) -im
                plt.imshow(ch, cmap="gray", vmin=0, vmax=255)
                plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex4_bottomhat_{struct_el}_{size}.png')

# %%  
# interesting result: take all the image results of a bottom-hat of the same image with the same structuring element line, size but different angles, compute the max of all of them for each pixel 
# and then display the result. It's a bit like a bottom-hat with a line of size 20 but with a better result.
im = skio.imread('/home/leo/tadi/TP-morpho/Images/laiton.bmp')
if len(im.shape)>2 and im.shape[2] == 3:
    im=grayscale_from_color(im)

angles = [0, 45, 90, 135]
shape= 'line'
size = 10
ch= []
for angle in angles:
    se = strel(shape, size, angle)
    ch.append(morpho.closing(im, se) -im)

# for every image in ch (ch is a list of images), take the max of all the images for each pixel
i = range (0, len(ch))
for i in range (0, len(ch)):
    if i == len(ch)-1:
        break
    else:
        res= np.maximum(ch[i], ch[i+1])
plt.imshow(res, cmap="gray", vmin=0, vmax=255)
plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex4_bottomhat_max_{struct_el}_{size}_{angle}.png')


#%% Section 4: top hat
im = skio.imread('/home/leo/tadi/TP-morpho/Images/retina2.gif')
print(im.shape)
im = im[0,:, :]
print(im.shape)

t = 10
se = strel('line', t, -45)
ch = im - morpho.opening(im, se)
plt.imshow(ch, cmap="gray", vmin=0, vmax=255)




#%% Section 5: apply an opening with each of them as structuring
# element, and compute the point-wise maximum of the results
im = skio.imread('/home/leo/tadi/TP-morpho/Images/retina2.gif')
print(im.shape)
im = im[0,:, :]
print(im.shape)

angles = [0, 45, 90, 135]
shape= 'line'
size = 10
ch= []
for angle in angles:
    se = strel(shape, size, angle)
    ch.append(morpho.opening(im, se))

# for every image in ch (ch is a list of images), take the max of all the images for each pixel
res = ch[0]
for i in range (0, len(ch)-1):
    print("compute max on res", i, "ch", i+1)
    res= np.maximum(res[i-1], ch[i+1])
plt.imshow(res, cmap="gray", vmin=0, vmax=255)
plt.savefig(f'/home/leo/tadi/TP-morpho/results/ex5_open_max_{struct_el}_{size}_{angle}.png')




#%% Alternate sequential filter
im = skio.imread('/home/leo/tadi/TP-morpho/Images/retina2.gif')
imt = im.copy()
N = 3
for k in range(N):
    se = strel('disk', k)
    imt = morpho.closing(morpho.opening(imt, se), se)
plt.imshow(imt, cmap="gray", vmin=0, vmax=255)

#%% Watersheds
# im = skio.imread('Images/bat200.bmp')
se = morpho.disk(1)

grad = morpho.dilation(im, se) - morpho.erosion(im, se)
grad = np.int32(grad > 40) * grad
plt.imshow(grad, cmap="gray")

local_mini = skf.peak_local_max(255 - grad, indices=False)
markers = ndi.label(local_mini)[0]
plt.imshow(local_mini, cmap="gray")

labels = watershed(grad, markers, watershed_line=True)
plt.imshow(random_colors(labels))
# viewimage_color(random_colors(labels)) - Usable if GIMP is installed

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

#%% Reconstruction
im = skio.imread('Images/retina2.gif')
# for retina2.gif 
print(im.shape)
im = im[0,:, :]
print(im.shape)

se4 = strel('disk', 4)
open4 = morpho.opening(im, se4)
reco = morpho.reconstruction(open4, im)
plt.imshow(reco, cmap="gray")
# %%
