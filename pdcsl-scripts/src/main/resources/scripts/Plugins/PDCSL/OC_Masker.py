# OCMasker - Create masks for OncoChrome-positive regions
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ
from qmul.pdcsl.channelop import apply_channel_op


def run_script():
    img = IJ.getImage()

    ops = [
            [2, 'MASK(Moments)'],
            [1, 'MASK(Moments)'],
            [4, 'MASK(Moments)'],
            [3, 'MASK(MaxEntropy)'],
            [5, 'COPY()']
            ]
    masks = apply_channel_op(img, ops)
    masks.show()

    ops = [
            [5, 'APPLY(1)'],
            [5, 'APPLY(2)'],
            [5, 'APPLY(3)'],
            [5, 'APPLY(4)'],
            [5, 'COPY()']
            ]
    masked = apply_channel_op(masks, ops)
    masked.show()


run_script()
