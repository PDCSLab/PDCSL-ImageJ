# Foci_Counter - Count H2A.X foci
# Copyright © 2019 Damien Goutte-Gattat

from ij import IJ
from ij.measure import ResultsTable
from ij.plugin import ChannelSplitter, ZProjector
from ij.plugin.filter import ParticleAnalyzer
from ij.process import ImageProcessor


def get_channel(img, fluorophore):
    """Get the number of the channel for the specified fluorophore."""
    info = img.getInfoProperty()
    if not info:
        return -1

    for line in info.split('\n'):
        if line.startswith('Information|Image|Channel|Fluor'):
            key, value = line.split(' = ')
            if value == fluorophore:
                return int(key[-1]) - 1

    return -1


def run_script():
    img = IJ.getImage()
    ch = get_channel(img, 'Cy5')
    if ch == -1:
        # Cannot identify correct channel, assume last
        ch = img.getNChannels() - 1

    # Save any existing ROI
    roi = img.getRoi()
    if roi:
        mask = img.getMask()

    # Save existing thresholds
    mint = img.getProcessor().getMinThreshold()
    maxt = img.getProcessor().getMaxThreshold()

    # Max project the image if needed and split the channels
    if img.getNSlices() > 1:
        channels = ChannelSplitter.split(ZProjector.run(img, 'max'))
    else:
        channels = ChannelSplitter.split(img)
    channel = channels[ch]

    if mint > 0 and maxt > 0:
        # Reapply original threshold
        channel.getProcessor().setThreshold(mint, maxt, ImageProcessor.NO_LUT_UPDATE)
    else:
        # Or apply arbitrary threshold
        depth = channel.getBitDepth()
        if depth == 16:
            channel.getProcessor().setThreshold(4000, 65535, ImageProcessor.NO_LUT_UPDATE)
        elif depth == 8:
            channel.getProcessor().setThreshold(250, 255, ImageProcessor.NO_LUT_UPDATE)
        else:
            IJ.log("Unexpected bit depth ({}-bit), aborting".format(depth))
            return


    # If a ROI was active on the original image, apply it to the projection
    if roi:
        channel.setRoi(roi)
        channel.getProcessor().setMask(mask)

    channel.show()

    # Run the particle analyzer
    rt = ResultsTable()
    analyzer = ParticleAnalyzer(ParticleAnalyzer.SHOW_OUTLINES | ParticleAnalyzer.DISPLAY_SUMMARY, 0, rt, 0.0, 500.0, 0.0, 1.0)
    if analyzer.analyze(channel):
        output = analyzer.getOutputImage()
        output.show()


run_script()