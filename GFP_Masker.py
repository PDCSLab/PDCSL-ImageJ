 # -*- coding: utf-8 -*
# GFPMasker - Mask GFP-positive regions from a RFP channel
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ, ImagePlus
from ij.plugin import ChannelSplitter, ImageCalculator
from ij.plugin.filter import Binary
from ij.process import ImageProcessor

def apply_binary_filters(filters, imp):
	"""Apply the named binary filters sequentially to the image."""
	bf = Binary()
	for filter_name in filters:
		bf.setup(filter_name, imp)
		bf.run(imp.getProcessor())

imp = IJ.getImage()
imps = ChannelSplitter.split(imp)
rfp = imps[0]
gfp = imps[1]

# Apply arbitrary threshold
gfp.getProcessor().setThreshold(49, 255, ImageProcessor.NO_LUT_UPDATE)

# Create mask for the GFP area
mask = ImagePlus("gfp_mask", gfp.getProcessor().createMask())
mask.getProcessor().invert()
# Smooth binary mask
apply_binary_filters(["close", "open"], mask)
# Set all positive pixels in the mask to 1
mask.getProcessor().subtract(254)

# Create the image corresponding to the RFP channel
# with the GFP region excluded
calc = ImageCalculator()
rfp_excl_gfp = calc.run("Multiply create", rfp, mask)
rfp_excl_gfp.setTitle("{} - {}".format(imp.getTitle(), "RFP outside GFP areas"))
rfp_excl_gfp.show()

# Invert the mask and create opposite image
mask.getProcessor().invert()
mask.getProcessor().subtract(254)
rfp_incl_gfp = calc.run("Multiply create", rfp, mask)
rfp_incl_gfp.setTitle("{} - {}".format(imp.getTitle(), "RFP inside GFP areas"))
rfp_incl_gfp.show()