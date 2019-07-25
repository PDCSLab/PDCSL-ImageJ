# Foci_Counter - Count H2A.X foci
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin import ChannelSplitter, ZProjector
from ij.plugin.filter import ParticleAnalyzer
from ij.process import ImageProcessor
import sys


def get_channel(img, fluorophore):
	"""Get the number of the channel for the specified fluorophore."""

	info = img.getInfoProperty()
	channel = -1

	for line in info.split('\n'):
		if line.startswith('Information|Image|Channel|Fluor'):
			key, value = line.split(' = ')
			if value == fluorophore:
				channel = int(key[-1]) - 1

	return channel


def run_script():
	img = IJ.getImage()
	ch = get_channel(img, 'Cy5')
	if ch == -1:
		IJ.log("Cannot identify far-red channel")
		return

	# Save any existing ROI
	roi = img.getRoi()

	# Max project the image and split the channels
	channels = ChannelSplitter.split(ZProjector.run(img, 'max'))
	channel = channels[ch]

	# Apply arbitrary threshold to get the foci
	channel.getProcessor().setThreshold(4000, 65535, ImageProcessor.NO_LUT_UPDATE)

	# If a ROI was active on the original image, apply it to the projection
	if roi:
		channel.setRoi(roi)

	channel.show()

	# Run the particle analyzer
	rt = ResultsTable()
	analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_OUTLINES | ParticleAnalyzer.DISPLAY_SUMMARY, 0, rt, 0.0, 500.0, 0.0, 1.0)
	if analyzer.analyze(channel):
		output = analyzer.getOutputImage()
		output.show()

run_script()
