# OC_Volume_Counter - Compute volume occupied by OncoChrome fluorophores
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ
from qmul.pdcsl.helper import extract_volumes
from qmul.pdcsl.oncochrome import create_masks


def run_script():
    img = IJ.getImage()

    masks = create_masks(img)
    masks.setCalibration(img.getCalibration())
    masks.show()

    values = extract_volumes(masks, range(4))

    IJ.log("{},{:.2f},{:.2f},{:.2f},{:.2f}".format(img.getTitle(), *values))


run_script()
