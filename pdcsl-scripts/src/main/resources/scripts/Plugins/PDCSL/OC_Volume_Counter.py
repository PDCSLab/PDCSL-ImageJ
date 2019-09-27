# OCMasker - Create masks for OncoChrome-positive regions
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ
from qmul.pdcsl.oncochrome import create_masks

def get_black_pixels_count(ip):
    width = ip.getWidth()
    height = ip.getHeight()
    pixels = ip.getIntArray()
    n = 0

    for x in range(width):
        for y in range(height):
            if pixels[x][y] == 0:
                n += 1
    return n

def run_script():
    img = IJ.getImage()
    info = img.getFileInfo()
    voxel = info.pixelWidth * info.pixelHeight * info.pixelDepth

    masks = create_masks(img)
    masks.show()
    values = [0.0, 0.0, 0.0, 0.0]

    for i in range(4):
        for j in range(img.getNSlices()):
            masks.setPosition(i+1, j+1, 1)
            n = get_black_pixels_count(masks.getProcessor())
            values[i] = values[i] + (n * voxel)

    IJ.log("{},{:.2f},{:.2f},{:.2f},{:.2f}".format(img.getTitle(),values[0], values[1], values[2], values[3]))

run_script()
