#@ File (label='Choose a CSV file', style='file') input_file
#@ Boolean (label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin import ZProjector
from ij.process import ImageProcessor, ImageStatistics

from org.incenp.imagej.ChannelMasker import createMasker
from org.incenp.imagej import BatchReader


# The operations to perform in the masking step
masker_pipeline = [
    # Create a mask from the DAPI channel covering the entire wing disc,
    # and a mask from the "Mark" channel covering the marked region
    createMasker('D:MASK(Minimum),M:MASK(Huang),S:COPY()', None, True),

    # Exclude the marked region from the wing discs mask
    createMasker('1:COMBINE(2;XOR),2:COPY(),3:COPY()', None, True),

    # Apply both masks to the signal channel
    createMasker('3:APPLY(1),3:APPLY(2)', None, True)
    ]


def process_image(image, order, results, savedir=None):
    # Step 1: Max-project the stack
    projected = ZProjector.run(image, "max")
    # Step 2: Masking
    masked = projected
    for masker in masker_pipeline:
        masked = masker.apply(masked, image.getTitle(), order)

    # Optionally save the masked images for a-posteriori check
    if savedir:
        outname = os.path.join(savedir, os.path.splitext(masked.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(masked, outname)

    # Quantify the signal on the masked image
    for i,label in [(1, "Control"), (2, "Marked")]:
        # Select the channel
        masked.setC(i)
        # Exclude black pixels (resulting from applying the masks)
        masked.getProcessor().setThreshold(1, 255, ImageProcessor.NO_LUT_UPDATE)
        # Extract mean intensity and area from the thresholded region
        stats = ImageStatistics.getStatistics(masked.getProcessor(), ImageStatistics.AREA | ImageStatistics.MEAN | ImageStatistics.LIMIT, masked.getCalibration())
        # Append the results to the results table
        results.incrementCounter()
        results.addValue("Image", image.getTitle())
        results.addValue("Side", label)
        results.addValue("Area", stats.area)
        results.addValue("Mean", stats.mean)


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
