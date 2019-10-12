from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.filter import ParticleAnalyzer

from qmul.pdcsl.features import NucleiSegmenter


def run_script():
    img = IJ.getImage()
    segmenter = NucleiSegmenter()
    results = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_OUTLINES | ParticleAnalyzer.DISPLAY_SUMMARY,
                                0, results, 0.0, 500.0, 0.0, 1.0)

    segmented = ImagePlus("binary", segmenter.segment(img.getProcessor()))
    segmented.show()
    if analyzer.analyze(segmented):
        output = analyzer.getOutputImage()
        output.show()

run_script()
