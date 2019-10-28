#@ File(label='Choose a CSV file', style='file') input_file
#@ Boolean (label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ

from org.incenp.imagej.ChannelMasker import applyMasker
from org.incenp.imagej.Helper import extractVolumes
from org.incenp.imagej import BatchReader


create_masks_command = '''
    G:MASK(Huang),
    C:MASK(Moments),
    G:MASK(Moments),
    Y:MASK(Moments),
    R:MASK(MaxEntropy)
    '''
    

def process_image(image, fields, savedir=None):
    masks = applyMasker(image, create_masks_command, image.getTitle(), fields[0])
    volumes = extractVolumes(masks)
    
    if savedir:
        outname = os.path.join(savedir, os.path.splitext(masks.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(masks, outname)
        
    masks.close()
    
    return volumes


def run_script():
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None
    
    batch = BatchReader(pathname)
    batch.readCSV()
    
    IJ.log(",".join(batch.getHeaders()) + ",Volume,mTurquoise,EGFP,Citrine,mCherry")
    fmt = ",{:.2f}" * 5
    
    while batch.next():
        img = batch.getImage()
        volumes = process_image(img, batch.getFields(), savedir=savedir)
        
        IJ.log(batch.getCSVRow() + fmt.format(*volumes))
        img.close()
        
        
run_script()