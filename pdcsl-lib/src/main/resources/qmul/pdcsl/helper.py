# -*- coding: utf-8 -*-
# Helper.py - Common helper functions
# Copyright © 2019 Damien Goutte-Gattat

from ij import ImagePlus
from ij.plugin import ImageCalculator
from ij.plugin.filter import Binary
from ij.process import AutoThresholder, ImageProcessor


def apply_binary_filters(filters, image):
    """Apply the named binary filters sequentially to the image."""
    bf = Binary()
    for name in filters:
        bf.setup(name, image)
        bf.run(image.getProcessor())


def auto_threshold(image, method, name=None):
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
    calc = ImageCalculator()
    source_image = ImagePlus("src", source.duplicate())
    mask_image = ImagePlus("mask", mask.duplicate())
    mask_image.getProcessor().invert()
    mask_image.getProcessor().subtract(254)

    masked = calc.run("Multiply create", source_image, mask_image)
    return masked.getProcessor()
