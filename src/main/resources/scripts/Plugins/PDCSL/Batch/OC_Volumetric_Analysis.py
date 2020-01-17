#@ File(label='Choose a CSV file', style='file') input_file
#@ Boolean (label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ
from ij.measure import ResultsTable

from org.incenp.imagej.ChannelMasker import createMasker
from org.incenp.imagej.Helper import extractVolumes
from org.incenp.imagej import BatchReader


create_masks_command = '''
    G:MASK(Huang),
    C:MASK(Moments),
    G:MASK(Moments),
    Y:MASK(Moments),
    R:MASK(MaxEntropy)
    '''

masker = createMasker(create_masks_command)


def process_image(image, order, results, savedir=None):
    masks = masker.apply(image, image.getTitle(), order)
    volumes = extractVolumes(masks)
    for i, label in enumerate(["Volume", "mTurquoise", "EGFP", "Citrine", "mCherry"]):
        results.addValue(label, volumes[i])
    
    if savedir:
        outname = os.path.join(savedir, os.path.splitext(masks.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(masks, outname)
        
    masks.close()


def run_script():
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None
    results = ResultsTable()
    
    batch = BatchReader(pathname)
    while batch.next():
        img = batch.getImage()
        batch.fillResultsTable(results)
        process_image(img, batch.getCell("ChannelOrder"), results, savedir=savedir)
        img.close()
        results.show("OC Volumetric Analysis Results")
        
        
run_script()