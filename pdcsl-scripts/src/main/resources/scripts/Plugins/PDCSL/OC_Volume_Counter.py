# OC_Volume_Counter - Compute volume occupied by OncoChrome fluorophores
# Copyright © 2019 Damien Goutte-Gattat

#@ String (label="Channel order", default="GCRYF") channel_order

from ij import IJ
from qmul.pdcsl.helper import extract_volumes
from qmul.pdcsl.channelop import apply_channel_opstring


def run_script():
    img = IJ.getImage()

    ops = 'G:MASK(Huang),C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy)'
    masks = apply_channel_opstring(img, ops, channel_order=channel_order)
    masks.show()

    values = extract_volumes(masks, range(5))

    fmt = "{}" + ",{:2f}" * 5
    IJ.log(fmt.format(img.getTitle(), *values))


run_script()
