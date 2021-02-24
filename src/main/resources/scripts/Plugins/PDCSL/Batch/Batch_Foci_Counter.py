# @ File(label='Choose a CSV file', style='file') input_file
# @ String(label='Thresholding method for area', value='Huang') area_thresholder
# @ String(label='Thresholding method for foci', value='MaxEntropy') foci_thresholder
# @ Boolean(label='Project Z-stack', value=false) project_stack
# @ Float(label='Minimum size', value=3.0, min=0, max=500) minimum_size
# @ Float(label='Maximum size', value=50.0, min=0, max=500) maximum_size
# @ Boolean(label='Save mask images', value=false, persist=false) save_masks
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
from ij.plugin import ZProjector
from ij.measure import ResultsTable

from org.incenp.imagej.ChannelMasker import createMasker
from org.incenp.imagej import Masking
from org.incenp.imagej import BatchReader
from org.incenp.imagej.Helper import extractVolumes
from uk.ac.qmul.bci.pdcsl.imagej.Util import countParticles


masker = createMasker('M:MASK({}),S:COPY()'.format(area_thresholder)).chain(
         createMasker('1:COPY(),2:MASK({}),2:COPY()'.format(foci_thresholder)).chain(
         createMasker('2:APPLY(1),1:COPY(),3:COPY()')))


def process_image(image, order, project, sizes, results, savedir=None):
    if project:
       image = ZProjector.run(image, "max")
    
    mask = masker.apply(image, image.getTitle(), order)
    
    volumes = extractVolumes(mask, [1])
    foci = countParticles(mask, sizes[0], sizes[1], [1], mask, 0)
    
    results.addValue("Foci", foci[0])
    results.addValue("Volume", volumes[0])
        
    if savedir:
        outname = os.path.join(savedir, os.path.splitext(mask.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(mask, outname)
        
    mask.close()
    
    
def run_script():
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None
    results = ResultsTable()
    
    batch = BatchReader(pathname)
    while batch.next():
        img = batch.getImage()
        batch.fillResultsTable(results)
        process_image(img, batch.getCell("Channel Order"), project_stack, (minimum_size, maximum_size), results, savedir=savedir)
        results.show("Batch Foci Counter Results")
        img.close()
        
        
run_script()