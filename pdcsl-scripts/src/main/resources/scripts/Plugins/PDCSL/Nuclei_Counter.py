# NucleiCounter - Count cell nuclei
# Copyright © 2019 Damien Goutte-Gattat

#@ Boolean (label="Process entire stack", default=true) do_stack

from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.filter import ParticleAnalyzer

from qmul.pdcsl.features import NucleiSegmenter


def run_script(do_stack):
    image = IJ.getImage()
    segmenter = NucleiSegmenter()
    results = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_OUTLINES | ParticleAnalyzer.DISPLAY_SUMMARY,
                                0, results, 0.0, 500.0, 0.0, 1.0)

    if do_stack:
        segmented = segmenter.segment_hyperstack(image, channels='all')
        counter = 0
        values = [0 for n in range(segmented.getNChannels())]

        for i in range(segmented.getNChannels()):
            for j in range(segmented.getNSlices()):
                segmented.setPosition(i + 1, j + 1, 1)

                if analyzer.analyze(segmented):
                    n = results.getCounter() - counter
                    counter = results.getCounter()
                    values[i] += n

        fmt = "{}" + ",{}" * len(values)
        IJ.log(fmt.format(image.getTitle(), *values))
    else:
        segmented = ImagePlus("binary", segmenter.segment(image.getProcessor()))
        segmented.show()
        if analyzer.analyze(segmented):
            output = analyzer.getOutputImage()
            output.show()


run_script(do_stack)
