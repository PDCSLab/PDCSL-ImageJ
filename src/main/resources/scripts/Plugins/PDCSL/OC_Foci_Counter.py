# @ ImagePlus img
# @ String(label='Tresholding method', value='MaxEntropy') method
# @ String(label='Channel order', value='GCRYF') order

import os

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin.filter import ParticleAnalyzer
from ij.process import ImageProcessor
from ij.process import ImageStatistics

from org.incenp.imagej.ChannelMasker import createMasker
from org.incenp.imagej.Helper import getResultsTable

volumeMasker = createMasker('C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy),F:MASK({})'.format(method))
fociMasker = createMasker('5:APPLY(1),5:APPLY(2),5:APPLY(3),5:APPLY(4)')


def process_image(image, channel_order):
    masks = volumeMasker.apply(image, "Masks - " + image.getTitle(), channel_order)
    foci = fociMasker.apply(masks, "Foci - " + image.getTitle())
    
    masks.show()
    foci.show()
    
    results = getResultsTable("OC Foci Counter Results")
    results.incrementCounter()
    results.addValue("Image", image.getTitle())
    
    rt = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE, 0, rt, 3.0, 50.0, 0.0, 1.0)
    
    for i, channel in enumerate(['mTurquoise', 'GFP', 'Citrine', 'mCherry']):
        foci.setC(i + 1)
        masks.setC(i + 1)
        
        area = 0
        
        for j in range(foci.getNSlices()):
            foci.setZ(j + 1)            
            analyzer.analyze(foci)
            
            masks.setZ(j + 1)
            masks.getProcessor().setThreshold(1, 255, ImageProcessor.NO_LUT_UPDATE)
            stats = ImageStatistics.getStatistics(masks.getProcessor(), ImageStatistics.LIMIT, masks.getCalibration())
            area += stats.area
            
        results.addValue("Foci_{}".format(channel), rt.getCounter())
        results.addValue("Area_{}".format(channel), area)
        results.show("OC Foci Counter Results")
        rt.reset()
        
        
process_image(img, order)