# @ File (label='Choose a CSV file', style='file') input_file
# @ Boolean (label='Save mask images', value=false, persist=false) save_masks
# @ Boolean (label='Analyse non-OC channel', value=false) process_non_oc_channel
# @ String (label='Threshold for non-OC channel', value='MaxEntropy') non_oc_threshold
# @ Float (label='Minimum size', value=3.0, min=0, max=500) minimum_size
# @ Float (label='Maximum size', value=50.0, min=0, max=500) maximum_size

import os

from ij import IJ
from ij.measure import ResultsTable

from org.incenp.imagej import BatchReader
from org.incenp.imagej import Helper
from org.incenp.imagej import NucleiSegmenter
from uk.ac.qmul.bci.pdcsl.imagej import OncoChrome
from uk.ac.qmul.bci.pdcsl.imagej import Util


def save_image(image, savedir):
    if savedir:
        outname = os.path.join(savedir, image.getTitle()) + '.tiff'
        IJ.saveAsTiff(image, outname)


def process_image(image, order, process_fr_channel, fr_threshold, sizes, results, savedir):
    extra_threshold = None
    if process_fr_channel and fr_threshold != 'nuclei':
        extra_threshold = fr_threshold
                    
    masks = OncoChrome.createMask(image, order, True, extra_threshold)
    save_image(masks, savedir)
    
    volumes = Helper.extractVolumes(masks, [1, 2, 3, 4, 5, 6])
    for i, label in enumerate(["Total", "mTurquoise", "GFP", "Citrine", "mCherry", "Control"]):
        results.addValue("Vol_{}".format(label), volumes[i])
    
    if process_fr_channel:
        masked = Util.applyMasks(masks, image.getTitle() + " Masked")
        if fr_threshold == 'nuclei':
            segmenter = NucleiSegmenter(2.0)
            masked = segmenter.segment(masked, [1, 2, 3, 4, 5])
        save_image(masked, savedir)
            
        foci = Util.countParticles(masked, sizes[0], sizes[1], [1, 2, 3, 4, 5], masked, 0)
        for i, label in enumerate(["Total", "mTurquoise", "GFP", "Citrine", "mCherry"]):
            results.addValue("Foc_{}".format(label), foci[i])
            
        masked.close()
        
    masks.close()


def run_script():
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None
    results = ResultsTable()
    
    batch = BatchReader(pathname)
    while batch.next():
        img = batch.getImage()
        # Sanity check: don't try to process image with not enough channels
        if ( process_non_oc_channel and img.getNChannels() >= 5 ) or ( not process_non_oc_channel and img.getNChannels() >= 4 ):
            batch.fillResultsTable(results)
            process_image(img, batch.getCell("Channel Order"), process_non_oc_channel, non_oc_threshold, (minimum_size, maximum_size), results, savedir)
            results.show("Batch OC Counter Results")
        img.close()        

run_script()