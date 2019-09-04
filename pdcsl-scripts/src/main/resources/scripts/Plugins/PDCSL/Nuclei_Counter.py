from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.filter import EDM, GaussianBlur, ParticleAnalyzer
from ij.process import AutoThresholder, ImageProcessor


def run_script():
	img = IJ.getImage()
	gb = GaussianBlur()
	thresholder = AutoThresholder()
	edm = EDM()

	t1 = img.getProcessor().duplicate()
	gb.blurGaussian(t1, 2.0)
	threshold = thresholder.getThreshold(AutoThresholder.Method.Moments, t1.getHistogram())
	t1.setThreshold(threshold, 255, ImageProcessor.NO_LUT_UPDATE)
	binary = ImagePlus("binary", t1.createMask())

	edm.toWatershed(binary.getProcessor())
	binary.getProcessor().invert()

	binary.show()

	rt = ResultsTable()
	analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_OUTLINES | ParticleAnalyzer.DISPLAY_SUMMARY, 0, rt, 0.0, 500.0, 0.0, 1.0)
	if analyzer.analyze(binary):
		output = analyzer.getOutputImage()
		#output.show()

run_script()