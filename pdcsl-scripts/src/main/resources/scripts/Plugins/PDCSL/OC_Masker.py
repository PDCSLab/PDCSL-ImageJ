# OCMasker - Create masks for OncoChrome-positive regions
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ
from qmul.pdcsl.oncochrome import create_masks, apply_masks


def run_script():
    img = IJ.getImage()

    masks = create_masks(img)
    masks.show()

    masked = apply_masks(masks)
    masked.show()


run_script()
