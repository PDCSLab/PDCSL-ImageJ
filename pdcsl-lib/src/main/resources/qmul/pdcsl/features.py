# -*- coding: utf-8 -*-
# features.py - Helper module to analyze object features
# Copyright © 2019 Damien Goutte-Gattat

"""Helper module to analyze object features in images."""

from ij import IJ
from ij.plugin.filter import EDM, GaussianBlur
from ij.process import AutoThresholder, ImageProcessor


class NucleiSegmenter():
    """Helper class for Watershed nuclei segmentation.

    This class provides methods implementing the Watershed segmentation
    of cell nuclei as described in
    <https://imagej.net/Nuclei_Watershed_Separation>.
    """

    def __init__(self, blur=2.0, thresholding=AutoThresholder.Method.Moments):
        """Creates a NucleiSegmenter instance.

        :param blur: The radius to use in the Gaussian blur step
            (default: 2.0)
        :type blur: float
        :param thresholding: The thresholding algorithm to use
            (default: Moments)
        :type thresholding: ij.process.AutoThresholder.Moment
        """
        self._gb = GaussianBlur()
        self._thresholder = AutoThresholder()
        self._EDM = EDM()
        self._blur_radius = blur
        self._method = thresholding

    def segment(self, ip):
        """Segment nuclei in a single image processor.

        :param ip: The source image processor
        :type ip: ij.process.ImageProcessor
        :returns: The segmented image
        :rtype: ij.process.ImageProcessor
        """
        copy = ip.duplicate()
        self._gb.blurGaussian(copy, self._blur_radius)
        threshold = self._thresholder.getThreshold(self._method, copy.getHistogram())
        copy.setThreshold(threshold, 255, ImageProcessor.NO_LUT_UPDATE)

        segmented = copy.createMask()
        self._EDM.toWatershed(segmented)
        segmented.invert()

        return segmented

    def segment_hyperstack(self, image, channels='current', slices='all', frames='all'):
        """Segment nuclei in a hyperstack.

        :param image: The source image
        :type image: ij.ImagePlus
        :param channels: A list of channels to process, or 'all' to
            process all channels, or 'current' to process only the
            current channel
        :type channels: list(int) or str
        :param slices: A list of Z-slices to process, or 'all' to
            process all slices, or 'current' to process only the
            current slice
        :type slices: list(int) or str
        :param framess: A list of T-frames to process, or 'all' to
            process all frames, or 'current' to process only the
            current frame
        :type frames: list(int) or str
        :returns: The segmented image
        :rtype: ij.ImagePlus
        """
        if channels == 'current':
            channels = [image.getC()]
        elif channels == 'all':
            channels = [n + 1 for n in range(image.getNChannels())]

        if slices == 'current':
            slices = [image.getZ()]
        elif slices == 'all':
            slices = [n + 1 for n in range(image.getNSlices())]

        if frames == 'current':
            frames = [image.getT()]
        elif frames == 'all':
            frames = [n + 1 for n in range(image.getNFrames())]

        result = IJ.createHyperStack(image.getTitle(), image.getWidth(), image.getHeight(),
                                     len(channels), len(slices), len(frames), 8)
        result.setCalibration(image.getCalibration())

        for i in channels:
            for j in slices:
                for k in frames:
                    image.setPosition(i, j, k)
                    result.setPosition(i, j, k)
                    result.setProcessor(self.segment(image.getProcessor()))

        return result
