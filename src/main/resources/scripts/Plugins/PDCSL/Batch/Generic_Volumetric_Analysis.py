#@ File(label='Choose a CSV file', style='file') input_file
#@ Boolean(label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ

from org.incenp.imagej.ChannelMasker import applyMasker
from org.incenp.imagej.Helper import extractVolumes
from org.incenp.imagej import BatchReader

def process_image(image, mask_command, savedir=None):
    masks = applyMasker(image, mask_command, image.getTitle(), None)
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
    while batch.next():
        img = batch.getImage()
        fields = batch.getFields()
        volumes = process_image(img, fields[0], savedir=savedir)
        
        str_volumes = ["{:.2f}".format(v) for v in volumes]
        line = img.getTitle()
        if len(fields) > 1:
            line += "," + ",".join(fields[1:])
        line += "," + ",".join(str_volumes)
        IJ.log(line)
        
        img.close()
        
        
run_script()
    