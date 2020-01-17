#@ File (label='Choose a CSV file', style='file') input_file
#@ Boolean (label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin import ZProjector
from ij.process import ImageProcessor, ImageStatistics

from org.incenp.imagej.ChannelMasker import applyMasker
from org.incenp.imagej import BatchReader


def mask_image(image, order, title):
    # Create a mask from the DAPI channel covering the entire wing discs,
    # and a mask from the "Mark" channel covering the marked region
    mask1 = applyMasker(image,  'D:MASK(Minimum),M:MASK(Huang),S:COPY()', "Mask1", order)

    # Exclude the marked region from the wing discs mask
    mask2 = applyMasker(mask1,  '1:COMBINE(2;XNOR),2:COPY(),3:COPY()', "Mask2", None)

    # Apply both masks to the signal channel
    masked = applyMasker(mask2, '3:APPLY(1),3:APPLY(2)', title, None)
    return masked


def analyze_image(image, results):
    # Channel 1 contains the "control" (un-marked) region,
    # Channel 2 contains the marked region
    for i,label in [(1, "Control"), (2, "Marked")]:
        # Select the channel
        image.setC(i)
        # Exclude black pixels (resulting from applying the masks)
        image.getProcessor().setThreshold(1, 255, ImageProcessor.NO_LUT_UPDATE)
        # Extract mean intensity and area from the thresholded region
        stats = ImageStatistics.getStatistics(image.getProcessor(), ImageStatistics.AREA | ImageStatistics.MEAN | ImageStatistics.LIMIT, image.getCalibration())
        # Append the results to the results table
        results.incrementCounter()
        results.addValue("Image", image.getTitle())
        results.addValue("Side", label)
        results.addValue("Area", stats.area)
        results.addValue("Mean", stats.mean)


def process_image(image, order, results, savedir=None):
    # Step 1: Max-project the stack
    projected = ZProjector.run(image, "max")
    # Step 2: Masking
    masked = mask_image(projected, order, image.getTitle())

    # Optionally save the masked images for a-posteriori check
    if savedir:
        outname = os.path.join(savedir, os.path.splitext(masked.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(masked, outname)

    # Quantify the signal on the masked image
    analyze_image(masked, results)


def run_script():
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None

    batch = BatchReader(pathname)
    results = ResultsTable()

    while batch.next():
        img = batch.getImage()
        process_image(img, batch.getCell(1), results, savedir=savedir)
        results.show("Wing Disc Signal")

        img.close()


run_script()
