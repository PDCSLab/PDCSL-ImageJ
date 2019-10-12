# OC_Volume_Counter - Compute volume occupied by OncoChrome fluorophores
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ
from qmul.pdcsl.helper import extract_volumes
from qmul.pdcsl.channelop import apply_channel_op


def run_script():
    img = IJ.getImage()

    ops = [
            [2, 'MASK(Moments)'],
            [1, 'MASK(Moments)'],
            [4, 'MASK(Moments)'],
            [3, 'MASK(MaxEntropy)']
            ]
    masks = apply_channel_op(img, ops)
    masks.show()

    values = extract_volumes(masks, range(4))

    IJ.log("{},{:.2f},{:.2f},{:.2f},{:.2f}".format(img.getTitle(), *values))


run_script()
