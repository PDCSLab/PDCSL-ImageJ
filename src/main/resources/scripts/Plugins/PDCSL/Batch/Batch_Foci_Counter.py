# @ File(label='Choose a CSV file', style='file') input_file
# @ String(label='Thresholding method', value='MaxEntropy') method
# @ Boolean(label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin import ZProjector
from ij.plugin.filter import ParticleAnalyzer
from ij.process import ImageProcessor
from ij.process import ImageStatistics

from org.incenp.imagej.ChannelMasker import createMasker
from org.incenp.imagej import Masking
from org.incenp.imagej import BatchReader

masker = createMasker('G:MASK(Huang),F:COPY()').chain(
         createMasker('1:COPY(),2:MASK({}),2:COPY()'.format(method)).chain(
         createMasker('2:APPLY(1),1:COPY(),3:COPY()')))


def process_image(image, order, results, savedir=None):
    projected = ZProjector.run(image, "max")
    mask = masker.apply(projected, image.getTitle(), order)
    
    rt = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE, 0, rt, 3.0, 50.0, 0.0, 1.0)
    mask.setC(1)
    if analyzer.analyze(mask):
        results.addValue("Foci", rt.getCounter())
        
        mask.setC(2)
        mask.getProcessor().setThreshold(1, 255, ImageProcessor.NO_LUT_UPDATE)
        stats = ImageStatistics.getStatistics(mask.getProcessor(), ImageStatistics.LIMIT, mask.getCalibration())
        results.addValue("Area", stats.area)
        
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
        process_image(img, batch.getCell("Channel Order"), results, savedir=savedir)
        results.show("Batch Foci Counter Results")
        img.close()
        
        
run_script()