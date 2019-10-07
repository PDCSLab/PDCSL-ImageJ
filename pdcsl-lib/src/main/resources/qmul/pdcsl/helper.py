# -*- coding: utf-8 -*-
# Helper.py - Common helper functions
# Copyright © 2019 Damien Goutte-Gattat

"""Common helper functions for ImageJ."""

import os.path

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
    """Count the number of black pixels in an image.

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


def extract_volumes(image, channels='all'):
    """Get volumes occupied by black pixels in a stack.

    :param image: The image to extract volumes from
    :type image: ij.ImagePlus
    :param channels: A list of 0-based channel indexes to process,
        or 'all' (default) to process all channels
    :type channels: list(int) or 'all'
    :returns: An array containing the volume for each channel
    :rtype: list(float)
    """
    cal = image.getCalibration()
    voxel = cal.pixelWidth * cal.pixelHeight * cal.pixelDepth
    volumes = []
    if channels == 'all':
        channels = range(image.getNChannels())

    for i in channels:
        n = 0
        for j in range(image.getNSlices()):
            image.setPosition(i + 1, j + 1, 1)
            n = n + (get_black_pixels_count(image.getProcessor()) * voxel)
        volumes.append(n)

    return volumes


def parse_csv_batch(pathname):
    """Parse a CSV file containing a list of images to process.

    The file is expected to contain one line per image file to process.
    Each line should contain at list a 'Image' field containing the pathname
    to the image. If that pathname is not absolute, it is assumed to be
    relative to the directory containing the CSV file.

    The file may contain a header line starting with '#HDR:' giving the
    name of the different fields.

    :param pathname: The pathname to the file to read
    :type pathname: str
    :returns: A tuple containing the list of items found in the file and
        the list of headers
    """
    headers = ['Image']
    image_index = 0
    items = []
    basename = os.path.dirname(pathname)

    with open(pathname, 'r') as f:
        for line in f:
            line = line.strip()

            if len(line) == 0:
                continue

            if line.startswith('#HDR:'):
                headers = line[5:].split(',')
                try:
                    image_index = headers.index('Image')
                except ValueError:
                    raise RuntimeError("No 'Image' field in headers list")
                continue

            if line.startswith('#'):
                continue

            fields = line.split(',')
            if len(fields) != len(headers):
                raise RuntimeError("Unexpected number of fields (expected {}, found {})".format(len(headers), len(fields)))

            if not fields[image_index].startswith('/'):
                fields[image_index] = os.path.join(basename, fields[image_index])
            items.append(fields)

    return (items, headers)
