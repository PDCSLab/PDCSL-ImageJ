# NucleiCounter - Count cell nuclei
# Copyright © 2019 Damien Goutte-Gattat

#@ Boolean (label="Process entire stack", default=true) do_stack

from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.filter import ParticleAnalyzer

from org.incenp.imagej import NucleiSegmenter


def run_script(do_stack):
    image = IJ.getImage()
    segmenter = NucleiSegmenter(2.0)
    results = ResultsTable()
    flags = ParticleAnalyzer.DISPLAY_SUMMARY
    if not do_stack:
        flags |= ParticleAnalyzer.SHOW_OUTLINES
    analyzer = ParticleAnalyzer(flags, 0, results, 0.0, 500.0, 0.0, 1.0)

    if do_stack:
        segmented = segmenter.segment(image, [i + 1 for i in range(image.getNChannels())])
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
