# GFPMasker - Mask GFP-positive regions from a RFP channel
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ, ImagePlus
from ij.plugin import ChannelSplitter
from ij.process import ImageProcessor

from org.incenp.imagej.helper import applyMask

def run_script():
    imp = IJ.getImage()
    imps = ChannelSplitter.split(imp)
    rfp = imps[0]
    gfp = imps[1]

    # Apply arbitrary threshold
    gfp.getProcessor().setThreshold(49, 255, ImageProcessor.NO_LUT_UPDATE)

    # Create mask for the GFP area
    mask = ImagePlus("gfp_mask", gfp.getProcessor().createMask())
    mask.getProcessor().invert()
    mask.getProcessor().dilate(1, 255)
    mask.getProcessor().erode(1, 255)
    mask.getProcessor().erode(1, 255)
    mask.getProcessor().dilate(1, 255)

    # Create the image corresponding to the RFP channel
    # with the GFP region excluded
    rfp_excl_gfp = ImagePlus("{} - RFP outside GFP areas".format(imp.getTitle()),
                             applyMask(rfp.getProcessor(),
                                        mask.getProcessor()))
    rfp_excl_gfp.show()

    # Invert the nask and create opposite image
    mask.getProcessor().invert()
    rfp_incl_gfp = ImagePlus("{} - RFP inside GFP area".format(imp.getTitle()),
                             applyMask(rfp.getProcessor(),
                                        mask.getProcessor()))
    rfp_incl_gfp.show()


run_script()
