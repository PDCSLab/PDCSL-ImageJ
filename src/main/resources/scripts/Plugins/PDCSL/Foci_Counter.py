# @ ImagePlus img
#
# PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
# Copyright © 2020 Damien Goutte-Gattat
#
# Foci_Counter: Count H2A.X foci

from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin import ChannelSplitter, ZProjector
from ij.plugin.filter import ParticleAnalyzer
from ij.process import AutoThresholder, ImageProcessor


def run_script():
    img = IJ.getImage()
    ch = img.getC()

    # Save any existing ROI
    roi = img.getRoi()
    if roi:
        roi = roi.getInverse(img)

    # Save existing thresholds
    mint = img.getProcessor().getMinThreshold()
    maxt = img.getProcessor().getMaxThreshold()

    # Max project the image if needed and split the channels
    if img.getNSlices() > 1:
        channels = ChannelSplitter.split(ZProjector.run(img, 'max'))
    else:
        channels = ChannelSplitter.split(img)
    channel = channels[ch-1]

    if mint > 0 and maxt > 0:
        # Reapply original threshold
        channel.getProcessor().setThreshold(mint, maxt, ImageProcessor.NO_LUT_UPDATE)
    else:
        # Or apply automatic threshold
        threshold = AutoThresholder().getThreshold('MaxEntropy', channel.getProcessor().getHistogram())
        channel.getProcessor().setThreshold(threshold, 255, ImageProcessor.NO_LUT_UPDATE)
        
    # Create thresholded image
    thresholded = channel.getProcessor().createMask()
    thresholdedImage = ImagePlus("Thresholded", thresholded)
        
    # Do a close-open cycle to smooth the mask
    thresholded.dilate(1, 0)
    thresholded.erode(1, 0)
    thresholded.erode(1, 0)
    thresholded.dilate(1, 0)

    # If a ROI was active on the original image, apply it to the projection
    if roi:
        thresholdedImage.setRoi(roi)

    thresholdedImage.show()

    # Run the particle analyzer
    rt = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_OUTLINES | ParticleAnalyzer.DISPLAY_SUMMARY, 0, rt, 3.0, 50.0, 0.0, 1.0)
    if analyzer.analyze(thresholdedImage):
        output = analyzer.getOutputImage()
        output.show()


run_script()
