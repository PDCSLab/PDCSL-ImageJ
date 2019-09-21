from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.filter import EDM, GaussianBlur, ParticleAnalyzer
from ij.process import AutoThresholder, ImageProcessor

channel_names = ['EGFP', 'mCitrine', 'mCherry', 'mTurquoise', 'Total']

def run_script():
	img = IJ.getImage()
	nslices = img.getNSlices()
	nchannels = img.getNChannels()
	if nchannels != 5:
		return

	gb = GaussianBlur()
	thresholder = AutoThresholder()
	edm = EDM()

	rt = ResultsTable()
	analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE | ParticleAnalyzer.DISPLAY_SUMMARY, 0, rt, 0.0, 500.0, 0.0, 1.0)

	counter = 0

	values = [0,0,0,0,0]

	for i in range(nchannels):
		for j in range(nslices):
			img.setPosition(i+1, j+1, 1)

			t1 = img.getProcessor().duplicate()
			gb.blurGaussian(t1, 2.0)
			threshold = thresholder.getThreshold(AutoThresholder.Method.Moments, t1.getHistogram())
			t1.setThreshold(threshold, 255, ImageProcessor.NO_LUT_UPDATE)
			binary = ImagePlus("binary", t1.createMask())

			edm.toWatershed(binary.getProcessor())
			binary.getProcessor().invert()

			if analyzer.analyze(binary):
				n = rt.getCounter() - counter
				counter = rt.getCounter()
				values[i] += n

	IJ.log("{},{},{},{},{}".format(values[0], values[1], values[2], values[3], values[4]))


run_script()