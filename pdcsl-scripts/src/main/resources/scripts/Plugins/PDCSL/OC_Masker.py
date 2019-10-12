# OCMasker - Create masks for OncoChrome-positive regions
# Copyright © 2019 Damien Goutte-Gattat

#@ String (label="Channel order", default="GCRYF") channel_order

from ij import IJ
from qmul.pdcsl.channelop import apply_channel_opstring


def run_script():
    img = IJ.getImage()

    ops = 'C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy),F:COPY()'
    masks = apply_channel_opstring(img, ops, channel_order=channel_order)
    masks.show()

    ops = '5:APPLY(1),5:APPLY(2),5:APPLY(3),5:APPLY(4),5:COPY()'
    masked = apply_channel_opstring(masks, ops)
    masked.show()


run_script()
