# -*- coding: utf-8 -*-
# OncoChrome.py - Helper functions for the OncoChrome
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ, ImagePlus
from ij.process import AutoThresholder

from qmul.pdcsl.helper import apply_binary_filters, auto_threshold, apply_mask


_default_channel_names = ['EGFP', 'mTurquoise', 'mCherry', 'mCitrine', 'Cy5']
_default_thresholders = [
    AutoThresholder.Method.Moments,
    AutoThresholder.Method.Moments,
    AutoThresholder.Method.Moments,
    AutoThresholder.Method.Moments,
    AutoThresholder.Method.MaxEntropy
    ]


def create_masks(image, channels=_default_channel_names, thresholders=_default_thresholders):
    nslices = image.getNSlices()
    nchannels = image.getNChannels()

    masks = IJ.createHyperStack("{} Masks".format(image.getTitle()),
                                image.getWidth(), image.getHeight(),
                                nchannels, nslices, 1, 8)

    for i in range(nslices):
        for j in range(nchannels):
            image.setPosition(j+1, i+1, 1)
            if j < 4:
                mask = auto_threshold(image, thresholders[j], channels[j]).getProcessor()
            else:
                mask = image.getProcessor().duplicate()
            masks.setPosition(j+1, i+1, 1)
            masks.setProcessor(mask)

    return masks


def apply_masks(image):
    nslices = image.getNSlices()
    nchannels = image.getNChannels()

    masked = IJ.createHyperStack("{} Applied".format(image.getTitle()),
                                 image.getWidth(), image.getHeight(),
                                 nchannels, nslices, 1, 8)

    for i in range(nslices):
        for j in range(4):
            image.setPosition(5, i+1, 1)
            src = image.getProcessor().duplicate()
            masked.setPosition(5, i+1, 1)
            masked.setProcessor(src.duplicate())

            image.setPosition(j+1, i+1, 1)
            mask = image.getProcessor()

            result = apply_mask(src, mask)
            masked.setPosition(j+1, i+1, 1)
            masked.setProcessor(result)

    return masked
