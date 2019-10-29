# PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
# Copyright © 2019 Damien Goutte-Gattat
#
# OC_Masker: Create masks for OncoChrome-positive regions

#@ String (label="Channel order", default="GCRYF") channel_order

from ij import IJ
from org.incenp.imagej import ChannelMasker


def run_script():
    img = IJ.getImage()

    ops = 'C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy),F:COPY()'
    masks = applyMasker(img, ops, img.getTitle() + " Masks", channel_order)
    masks.show()

    ops = '5:APPLY(1),5:APPLY(2),5:APPLY(3),5:APPLY(4),5:COPY()'
    masked = applyMasker(masks, ops, img.getTitle() + " Masked", None)
    masked.show()


run_script()
