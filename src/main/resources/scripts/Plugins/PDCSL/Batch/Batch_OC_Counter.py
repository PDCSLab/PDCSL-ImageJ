# @ File (label='Choose a CSV file', style='file') input_file
# @ Boolean (label='Save mask images', value=false, persist=false) save_masks
# @ Boolean (label='Analyse non-OC channel', value=false) process_non_oc_channel
# @ String (label='Threshold for non-OC channel', value='MaxEntropy') non_oc_threshold
# @ Integer (label='Subtract background radius', value=50, min=0) subtract_radius
# @ Integer (label='Blur radius', value=2, min=0) blur_radius
# @ Float (label='Minimum size', value=3.0, min=0, max=500) minimum_size
# @ Float (label='Maximum size', value=50.0, min=0, max=500) maximum_size
#
#
# PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
# Copyright © 2021 Damien Goutte-Gattat
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

import os

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin.filter import GaussianBlur

from org.incenp.imagej import BatchReader
from org.incenp.imagej import Helper
from org.incenp.imagej import NucleiSegmenter
from uk.ac.qmul.bci.pdcsl.imagej import OncoChrome
from uk.ac.qmul.bci.pdcsl.imagej import Util


def save_image(image, savedir):
    if savedir:
        outname = os.path.join(savedir, image.getTitle()) + '.tiff'
        IJ.saveAsTiff(image, outname)


def process_image(image, order, oncochrome, process_fr_channel, fr_threshold, sizes, results, savedir, subtract, blur):
    channelNames = oncochrome.getChannelNames()
    channelNumbers = range(1, oncochrome.getNChannels() + 1)
    
    if subtract != 0:
        IJ.run(image, "Subtract Background...", "rolling={:d} disable stack".format(subtract))
    if blur != 0:
        IJ.run(image, "Gaussian Blur...", "sigma={:d} stack".format(blur))
                    
    masks = oncochrome.getMasker().apply(image, image.getTitle() + " Masks", order)
    save_image(masks, savedir)
    
    volumes = Helper.extractVolumes(masks, channelNumbers)
    for i, label in enumerate(channelNames):
        results.addValue("Vol_{}".format(label), volumes[i])
    
    if process_fr_channel:
        masked = Util.applyMasks(masks, image.getTitle() + " Masked")
        if fr_threshold == 'nuclei':
            segmenter = NucleiSegmenter(2.0)
            masked = segmenter.segment(masked, channelNumbers)
        save_image(masked, savedir)
            
        foci = Util.countParticles(masked, sizes[0], sizes[1], channelNumbers, masked, 0)
        for i, label in enumerate(channelNames):
            results.addValue("Foc_{}".format(label), foci[i])
            
        masked.close()
        
    masks.close()


def run_script():
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None
    results = ResultsTable()
    
    oncochrome = OncoChrome.getOncoChrome("brainv1");
    oncochrome.setControlMask(True)
    if process_non_oc_channel:
        if non_oc_threshold == 'nuclei':
            oncochrome.setExtraChannel('F', None)
        else:
            oncochrome.setExtraChannel('F', non_oc_threshold)
    
    batch = BatchReader(pathname)
    while batch.next():
        img = batch.getImage()
        # Sanity check: don't try to process image with not enough channels
        if ( oncochrome.checkImage(img) ):
            batch.fillResultsTable(results)
            process_image(img, batch.getCell("Channel Order"), oncochrome, process_non_oc_channel, non_oc_threshold, (minimum_size, maximum_size), results, savedir, subtract_radius, blur_radius)
            results.show("Batch OC Counter Results")
        img.close()        

run_script()