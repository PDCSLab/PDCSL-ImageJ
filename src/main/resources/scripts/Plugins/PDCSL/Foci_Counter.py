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

from ij.plugin import ZProjector

from org.incenp.imagej.Helper import getResultsTable
from org.incenp.imagej.ChannelMasker import createMasker
from uk.ac.qmul.bci.pdcsl.imagej.Helper import countParticles


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
        method = 'FIXED,{:.0f}'.format(min_threshold)
    
    # Project the image?
    if image.getNSlices() > 1 and project:
        image = ZProjector.run(image, 'max')
    
    # Create the thresholded image
    masker = createMasker('{:d}:MASK({:s})'.format(current_channel, method))
    thresholded_image = masker.apply(image, "Foci Counter Threshold and Outline")
        
    # If the original image had a ROI, re-apply it
    if roi:
        thresholded_image.setRoi(roi)
    
    # Analyze the thresholded image
    foci = countParticles(thresholded_image, min_size, max_size, [1], thresholded_image, 0)
        
    # Display the images and the results
    thresholded_image.show()
    results = getResultsTable("Foci Counter Results")
    results.incrementCounter()
    results.addValue("Image", image.getTitle())
    results.addValue("Foci", foci[0])
    results.show("Foci Counter Results")


process_image(img, thresholding_method, project_stack, minimum_size, maximum_size, include_roi)
