import numpy as np
import platform
import tempfile
import os
import matplotlib.pyplot as plt
from skimage import io as skio

import skimage.morphology as morpho
from skimage.draw import line

structuring_elements_list= ['disk', 'diamond', 'square', 'line']
sizes= [4,8]

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

def image_show(image, cmap='gray', **kwargs):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
    ax.imshow(image, cmap=cmap)
    ax.axis('off')
    return fig, ax

def image_show_multi(imlist, nrows=1, ncols=1, cmap='gray'):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols, 8*nrows))
    i=0
    for r in range(nrows):
        for c in range(ncols):
            ax[i].imshow(imlist[i])
            ax[i].axis('off')
            i=i+1
            
    return fig, ax

