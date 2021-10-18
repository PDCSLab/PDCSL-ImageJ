# @ ImagePlus img
# @ String(label='Thresholding method', choices={"NONE", "PRESET", "HUANG", "IJ_ISODATA", "INTERMODES", "ISODATA", "LI", "MAX_ENTROPY", "MEAN", "MIN_ERROR", "MINIMUM", "MOMENTS", "OTSU", "PERCENTILE", "RENYI_ENTROPY", "TRIANGLE", "YEN", "BERNSEN", "CONTRAST", "MEAN_LOCAL", "MEDIAN", "MIDGREY", "NIBLACK", "OTSU_LOCAL", "PHANSALKAR", "SAUVOLA"}) thresholding_method
# @ String(label='Channel(s) to process', value='selected') channel_list
# @ Boolean(label='Project stack', value=false) project_stack
# @ Float(label='Minimum size', value=3.0, min=0, max=500) minimum_size
# @ Float(label='Maximum size', value=50.0, min=0, max=500) maximum_size
# @ Boolean(label='Include ROI', value=false) include_roi
#
#
# PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
# Copyright © 2020,2021 Damien Goutte-Gattat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the Gnu General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Foci_Counter: Count H2A.X foci

from ij import IJ
from ij.plugin import ZProjector

from org.incenp.imagej.Helper import getResultsTable
from org.incenp.imagej.ChannelMasker import createMasker
from uk.ac.qmul.bci.pdcsl.imagej.Util import countParticles, parseChannels


def process_image(image, channels, method, project, min_size, max_size, roi_in):
    # Save any existing ROI
    roi = image.getRoi()
    if roi and not roi_in:
        # The ROI is to be *excluded* from the analysis
        roi = roi.getInverse(image)
        
    if method == 'PRESET':
        # Get pre-defined threshold
        min_threshold = image.getProcessor().getMinThreshold()
        method = 'MASK(FIXED,{:.0f})'.format(min_threshold)
    elif method == 'NONE':
        method = 'COPY()'
    else:
        method = 'MASK({:s})'.format(method)
    
    # Project the image?
    if image.getNSlices() > 1 and project:
        image = ZProjector.run(image, 'max')
        
    # Build the masking command
    cmd = ''
    for i, channel in enumerate(channels):
        if i > 0:
            cmd += ','
        cmd += '{:d}:{:s}'.format(channel, method)
    
    # Create the thresholded image
    masker = createMasker(cmd)
    thresholded_image = masker.apply(image, "Foci Counter Threshold and Outline")
        
    # If the original image had a ROI, re-apply it
    if roi:
        thresholded_image.setRoi(roi)
    
    # Analyze the thresholded image
    foci = countParticles(thresholded_image, min_size, max_size, range(1, len(channels) + 1), thresholded_image, 0)
        
    # Display the images and the results
    thresholded_image.show()
    results = getResultsTable("Foci Counter Results")
    results.incrementCounter()
    results.addValue("Image", image.getTitle())
    for i in range(len(channels)):
        results.addValue("Foci (channel {:d})".format(channels[i]), foci[i])
    results.show("Foci Counter Results")

channels = parseChannels(img, channel_list)
process_image(img, channels, thresholding_method, project_stack, minimum_size, maximum_size, include_roi)
