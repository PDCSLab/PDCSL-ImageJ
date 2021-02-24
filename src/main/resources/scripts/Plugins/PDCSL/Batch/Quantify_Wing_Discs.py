#@ File (label='Choose a CSV file', style='file') input_file
#@ Boolean (label='Save mask images', value=false, persist=false) save_masks
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

import os

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin import ZProjector
from ij.process import ImageProcessor, ImageStatistics

from org.incenp.imagej.ChannelMasker import createMasker
from org.incenp.imagej import BatchReader


# The operations to perform in the masking step
# 1. Create a mask from the DAPI channel covering the entire wing disc,
#    and a mask from the "Mark" channel covering the marked region
# 2. Exclude the marked region from the wing disc mask
# 3. Apply both masks to the signal channel
masker = createMasker('D:MASK(Minimum),M:MASK(Huang),S:COPY()').chain(
    createMasker('1:APPLY(2,XOR),2:COPY(),3:COPY()').chain(
    createMasker('3:APPLY(1),3:APPLY(2)')))


def process_image(image, order, results, savedir=None):
    # Step 1: Max-project the stack
    projected = ZProjector.run(image, "max")
    # Step 2: Masking
    masked = masker.apply(projected, image.getTitle(), order)

    # Optionally save the masked images for a-posteriori check
    if savedir:
        outname = os.path.join(savedir, os.path.splitext(masked.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(masked, outname)

    # Quantify the signal on the masked image
    for i,label in enumerate(["Control", "Marked"]):
        # Select the channel
        masked.setC(i + 1)
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
        process_image(img, batch.getCell("Channel Order"), results, savedir=savedir)
        results.show("Wing Disc Signal")

        img.close()


run_script()
