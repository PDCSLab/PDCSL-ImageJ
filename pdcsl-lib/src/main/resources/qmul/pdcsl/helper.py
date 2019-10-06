# -*- coding: utf-8 -*-
# Helper.py - Common helper functions
# Copyright © 2019 Damien Goutte-Gattat

"""Common helper functions for ImageJ."""

from ij import ImagePlus
from ij.plugin import ImageCalculator
from ij.plugin.filter import Binary
from ij.process import AutoThresholder, ImageProcessor


def apply_binary_filters(filters, image):
    """Apply the named binary filters sequentially to the image.

    :param filters: An array of filter names
    :type filters: [str]
    :param image: The image to apply the filter to
    :type image: ij.ImagePlus
    """
    bf = Binary()
    for name in filters:
        bf.setup(name, image)
        bf.run(image.getProcessor())


def auto_threshold(image, method, name=None):
    """Apply an automatic threshold to an image.

    :param image: The image to process
    :type image: ij.ImagePlus
    :param method: The thresholding method to use
    :type method: ij.process.AutoThresholder.Method
    :param name: The name to give to the resulting image
        (default is the name of the original image + " Mask")
    :returns: The thresholded image
    :rtype: ij.ImagePlus
    """
    thresholder = AutoThresholder()
    ip = image.getProcessor()
    threshold = thresholder.getThreshold(method, ip.getHistogram())
    ip.setThreshold(threshold, 255, ImageProcessor.NO_LUT_UPDATE)
    if not name:
        name = "{} Mask".format(image.getTitle())
    mask = ImagePlus(name, ip.createMask())
    mask.getProcessor().invert()
    apply_binary_filters(['close', 'open'], mask)
    return mask


def apply_mask(source, mask):
    """Apply a binary mask to an image.

    The mask is expected to contain to be a 8-bit binary image,
    with black pixels (0) defining the regions to keep in the
    masked image.

    :param source: The source image to apply the mask to
    :type source: ij.process.ImageProcessor
    :param mask: The image containing the mask to apply
    :type mask: ij.process.ImageProcessor
    :returns: The masked image
    :rtype: ij.process.ImageProcessor
    """
    calc = ImageCalculator()
    source_image = ImagePlus("src", source.duplicate())
    mask_image = ImagePlus("mask", mask.duplicate())
    mask_image.getProcessor().invert()
    mask_image.getProcessor().subtract(254)

    masked = calc.run("Multiply create", source_image, mask_image)
    return masked.getProcessor()


def get_black_pixels_count(ip):
    """Count the number of black pixels in an inage.

    :param ip: The image whose black pixels should be counted
    :type ip: ij.process.ImageProcessor
    :returns: The number of black pixels
    :rtype: int
    """
    width = ip.getWidth()
    height = ip.getHeight()
    pixels = ip.getIntArray()
    n = 0

    for x in range(width):
        for y in range(height):
            if pixels[x][y] == 0:
                n += 1
    return n
