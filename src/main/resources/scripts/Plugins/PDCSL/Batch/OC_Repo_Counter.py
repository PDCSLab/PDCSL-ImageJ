# @ File (label='Choose a CSV file', style='file') input_file
# @ Boolean (label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ, Prefs
from ij.measure import ResultsTable
from ij.plugin.filter import ParticleAnalyzer

from org.incenp.imagej.ChannelMasker import createMasker
from org.incenp.imagej import NucleiSegmenter
from org.incenp.imagej.Helper import extractVolumes
from org.incenp.imagej import BatchReader

create_masks_command = '''
    G:MASK(Huang),
    C:MASK(Moments),
    G:MASK(Moments),
    Y:MASK(Moments),
    R:MASK(MaxEntropy),
    F:COPY()
    '''

apply_masks_command = '''
    6:APPLY(1),
    6:APPLY(2),
    6:APPLY(3),
    6:APPLY(4),
    6:APPLY(5)
    '''

masker = createMasker(create_masks_command)
applier = createMasker(apply_masks_command)


def count_cell_nuclei(image):
    nslices = image.getNSlices()
    nchannels = image.getNChannels()

    rt = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE, 0, rt, 0.0, 500.0, 0.0, 1.0)
    counter = 0
    values = [0, 0, 0, 0, 0]

    for i in range(nchannels):
        for j in range(nslices):
            image.setPosition(i + 1, j + 1, 1)

            if analyzer.analyze(image):
                n = rt.getCounter() - counter
                counter = rt.getCounter()
                values[i] += n

    return values


def process_image(image, order, results, savedir=None):
    masks = masker.apply(image, image.getTitle(), order)
    volumes = extractVolumes(masks, [1, 2, 3, 4, 5])
    for i, label in enumerate(["Total", "mTurquoise", "GFP", "Citrine", "mCherry"]):
        results.addValue("Vol_{}".format(label), volumes[i])

    segmenter = NucleiSegmenter(2.0)
    masked = applier.apply(masks, masks.getTitle(), None)
    segmented = segmenter.segment(masked, [1, 2, 3, 4, 5])
    nuclei = count_cell_nuclei(segmented)
    for i, label in enumerate(["Total", "mTurquoise", "GFP", "Citrine", "mCherry"]):
        results.addValue("Nuc_{}".format(label), nuclei[i])

    if savedir:
        outname = os.path.join(savedir, os.path.splitext(masks.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(masks, outname)

    masks.close()
    masked.close()


def run_script():
    savedBackgroundPref = Prefs.blackBackground
    Prefs.blackBackground = True
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None
    batch = BatchReader(pathname)
    results = ResultsTable()

    while batch.next():
        img = batch.getImage()
        if img.getNChannels() >= 5:
            batch.fillResultsTable(results)
            process_image(img, batch.getCell("Channel Order"), results, savedir=savedir)
            results.show("OC Repo Counter Results")
        img.close()
        
    Prefs.blackBackground = savedBackgroundPref


run_script()
