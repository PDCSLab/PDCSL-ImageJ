# OCMasker - Create masks for OncoChrome-positive regions
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ, ImagePlus
from ij.process import AutoThresholder, ImageProcessor

from qmul.pdcsl.helper import apply_binary_filters

def do_threshold(proc, method, name):
    thresholder = AutoThresholder()
    threshold = thresholder.getThreshold(method, proc.getHistogram())
    proc.setThreshold(threshold, 255, ImageProcessor.NO_LUT_UPDATE)
    mask = ImagePlus("{}_mask".format(name), proc.createMask())
    mask.getProcessor().invert()
    apply_binary_filters(['close', 'open'], mask)
    return mask.getProcessor()

img = IJ.getImage()
nslices = img.getNSlices()
nchannels = img.getNChannels()
new = IJ.createHyperStack("Masked", img.getWidth(), img.getHeight(),
                          nchannels, nslices, 1, 8)

CHANNEL_NAMES = ['EGFP', 'mTurquoise', 'mCherry', 'mCitrine', 'Cy5']
THRESHOLD_METHODS = [
        AutoThresholder.Method.Otsu,
        AutoThresholder.Method.Otsu,
        AutoThresholder.Method.Otsu,
        AutoThresholder.Method.MaxEntropy,
        AutoThresholder.Method.MaxEntropy
        ]

for i in range(nslices):
    for j in range(nchannels):
        img.setPosition(j+1, i+1, 1)
        if j < 4:
            mask = do_threshold(img.getProcessor(),
                                THRESHOLD_METHODS[j], CHANNEL_NAMES[j])
        else:
            mask = img.getProcessor().duplicate()
        new.setPosition(j+1, i+1, 1)
        new.setProcessor(mask)

new.show()
