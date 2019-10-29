# PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
# Copyright © 2019 Damien Goutte-Gattat
#
# OC_Volume_Counter: Compute volume occuped by OncoChrome fluorophores

#@ String (label="Channel order", default="GCRYF") channel_order

from ij import IJ
from org.incenp.imagej.Helper import extractVolumes
from org.incenp.imagej.ChannelMasker import applyMasker


def run_script():
    img = IJ.getImage()

    ops = 'G:MASK(Huang),C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy)'
    masks = applyMasker(img, ops, img.getTitle() + " Masks", channel_order)
    masks.show()

    values = extractVolumes(masks)

    fmt = "{}" + ",{:2f}" * 5
    IJ.log(fmt.format(img.getTitle(), *values))


run_script()
