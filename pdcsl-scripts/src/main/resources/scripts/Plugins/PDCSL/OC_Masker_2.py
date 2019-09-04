from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator

def run_script():
	img = IJ.getImage()
	nslices = img.getNSlices()
	nchannels = img.getNChannels()
	if nchannels != 5:
		return

	new = IJ.createHyperStack("Masked", img.getWidth(), img.getHeight(),
							  5, nslices, 1, 8)
	calc = ImageCalculator()

	for i in range(nslices):
		for j in range(4):
			img.setPosition(5, i+1, 1)
			src = ImagePlus("src", img.getProcessor().duplicate())
			new.setPosition(5, i+1, 1)
			new.setProcessor(img.getProcessor().duplicate())

			img.setPosition(j+1, i+1, 1)
			maskp = img.getProcessor().duplicate()
			maskp.invert()
			maskp.subtract(254)
			mask = ImagePlus("mask", maskp)

			masked = calc.run("Multiply create", src, mask)

			new.setPosition(j+1, i+1, 1)
			new.setProcessor(masked.getProcessor())

	new.show()

run_script()