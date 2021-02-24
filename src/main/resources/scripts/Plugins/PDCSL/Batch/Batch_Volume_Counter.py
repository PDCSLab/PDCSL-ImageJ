#@ File(label='Choose a CSV file', style='file') input_file
#@ Boolean(label='Save mask images', value=false, persist=false) save_masks
#@ Boolean(label='Exclude frames with black masks', value=true, persist=true) exclude_blacks
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

from org.incenp.imagej.ChannelMasker import applyMasker
from org.incenp.imagej.Helper import extractVolumes
from org.incenp.imagej import BatchReader
from uk.ac.qmul.bci.pdcsl.imagej.Hacks import removeBlackSlices

def process_image(image, mask_command, results, savedir=None, remove_black_slices=False):
    masks = applyMasker(image, mask_command, image.getTitle(), None)
    if remove_black_slices:
        masks = removeBlackSlices(masks)
    volumes = extractVolumes(masks)
    for i, volume in enumerate(volumes):
        results.addValue("Channel {}".format(i + 1), volume)
    
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
        process_image(img, batch.getCell('MaskCommand'), results, savedir=savedir, remove_black_slices=exclude_blacks)
        img.close()
        results.show("Batch Volume Counter Results")
        
        
run_script()
    