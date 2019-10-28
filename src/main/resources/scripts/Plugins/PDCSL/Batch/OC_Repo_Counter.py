#@ File (label='Choose a CSV file', style='file') input_file
#@ Boolean (label='Save mask images', value=false, persist=false) save_masks

import os

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin.filter import ParticleAnalyzer

from org.incenp.imagej.ChannelMasker import applyMasker
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


def count_cell_nuclei(image):
    nslices = image.getNSlices()
    nchannels = image.getNChannels()

    rt = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE, 0, rt, 0.0, 500.0, 0.0, 1.0)
    counter = 0
    values = [0,0,0,0,0]

    for i in range(nchannels):
        for j in range(nslices):
            image.setPosition(i + 1, j + 1, 1)

            if analyzer.analyze(image):
                n = rt.getCounter() - counter
                counter = rt.getCounter()
                values[i] += n

    return values


def process_image(image, fields, savedir=None):
    masks = applyMasker(image, create_masks_command, image.getTitle(), fields[0])
    volumes = extractVolumes(masks, [1,2,3,4,5])

    segmenter = NucleiSegmenter(2.0)
    masked = applyMasker(masks, apply_masks_command, masks.getTitle(), None)
    segmented = segmenter.segment(masked, [1,2,3,4,5])
    nuclei = count_cell_nuclei(segmented)

    if savedir:
        outname = os.path.join(savedir, os.path.splitext(masks.getTitle())[0]) + '.tiff'
        IJ.saveAsTiff(masks, outname)

    masks.close()
    masked.close()

    return list(volumes) + nuclei


def run_script():
    pathname = input_file.getAbsolutePath()
    savedir = os.path.dirname(pathname) if save_masks else None
    batch = BatchReader(pathname)
    batch.readCSV()

    IJ.log(",".join(batch.getHeaders()) + ",Volume,mTurquoise,EGFP,Citrine,mCherry,N_Total,N_mTurquoise,N_EGFP,N_Citrine,N_mCherry")
    fmt = ",{:.2f}" * 5 + ",{}" * 5

    while batch.next():
        img = batch.getImage()
        values = process_image(img, batch.getFields(), savedir=savedir)

        IJ.log(batch.getCSVRow() + fmt.format(*values))

        img.close()


run_script()