from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.filter import ParticleAnalyzer

from qmul.pdcsl.features import NucleiSegmenter


def run_script():
    img = IJ.getImage()
    segmenter = NucleiSegmenter()
    results = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE | ParticleAnalyzer.DISPLAY_SUMMARY,
                                0, results, 0.0, 500.0, 0.0, 1.0)

    segmented = segmenter.segment_hyperstack(img, channels='all')
    counter = 0
    values = [0 for n in segmented.getNChannels()]

    for i in range(segmented.getNChannels()):
        for j in range(segmented.getNSlices()):
            segmented.setPosition(i + 1, j + 1, 1)

            if analyzer.analyze(segmented):
                n = rt.getCounter() - counter
                counter = rt.getCounter()
                values[i] += n

    fmt = "{}" + ",{}" * len(values)
    IJ.log(fmt.format(img.getTitle(), *values))


run_script()
