# @ ImagePlus img
# @ String(label='Thresholding method', value='MaxEntropy') thresholding_method
# @ Boolean(label='Project stack', value=false) project_stack
# @ Float(label='Minimum size', value=3.0, min=0, max=500) minimum_size
# @ Float(label='Maximum size', value=50.0, min=0, max=500) maximum_size
# @ Boolean(label='Include ROI', value=false) include_roi
#
#
# PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
# Copyright © 2020 Damien Goutte-Gattat
#
# Foci_Counter: Count H2A.X foci

from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin import ZProjector
from ij.plugin.filter import ParticleAnalyzer
from ij.process import AutoThresholder, ImageProcessor

from org.incenp.imagej.Helper import getResultsTable

def threshold_processor(ip, method):
    # Get threshold: use specified algorithm or pre-set threshold levels
    if isinstance(method, basestring):
        min_threshold = AutoThresholder().getThreshold(method, ip.getHistogram())
        max_threshold = 255
    else:
        min_threshold, max_threshold = method
        
    # Create thresholded image
    ip.setThreshold(min_threshold, max_threshold, ImageProcessor.NO_LUT_UPDATE)
    thresholded = ip.createMask()
    
    # Do a close-open cycle to smooth the mask
    thresholded.dilate(1, 0)
    thresholded.erode(1, 0)
    thresholded.erode(1, 0)
    thresholded.dilate(1, 0)
    
    return thresholded


def process_image(image, method, project, min_size, max_size, roi_in):
    current_channel = image.getC()
    
    # Save any existing ROI
    roi = image.getRoi()
    if roi and not roi_in:
        # The ROI is to be *excluded* from the analysis
        roi = roi.getInverse(image)
        
    if method == 'preset':
        # Get pre-defined threshold
        min_threshold = image.getProcessor().getMinThreshold()
        max_threshold = image.getProcessor().getMaxThreshold()
        method = (min_threshold, max_threshold)
    
    # Project the image?
    if image.getNSlices() > 1 and project:
        image = ZProjector.run(image, 'max')
        
    # Create thresholded image
    thresholded_image = IJ.createHyperStack("Thresholded", image.getWidth(), image.getHeight(),
                                            1, image.getNSlices(), 1, 8)        
    for i in range(image.getNSlices()):
        image.setC(current_channel)
        image.setZ(i + 1)
        thresholded_image.setZ(i + 1)
        thresholded_image.setProcessor(threshold_processor(image.getProcessor(), method))
        
    # If the original image had a ROI, re-apply it
    if roi:
        thresholded_image.setRoi(roi)
    
    # Analyze the thresholded image
    rt = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_OUTLINES, 0, rt, min_size, max_size, 0.0, 1.0)
    analyzer.setHideOutputImage(True)
    outline_image = IJ.createHyperStack("Outlines", image.getWidth(), image.getHeight(),
                                        1, thresholded_image.getNSlices(), 1, 8)
    for i in range(thresholded_image.getNSlices()):
        thresholded_image.setZ(i + 1)
        analyzer.analyze(thresholded_image)
        outline_image.setZ(i + 1)
        outline_image.setProcessor(analyzer.getOutputImage().getProcessor())
        
    # Display the images and the results
    thresholded_image.show()
    outline_image.show()
    results = getResultsTable("Foci Counter Results")
    results.incrementCounter()
    results.addValue("Image", image.getTitle())
    results.addValue("Foci", rt.getCounter())
    results.show("Foci Counter Results")


process_image(img, thresholding_method, project_stack, minimum_size, maximum_size, include_roi)
