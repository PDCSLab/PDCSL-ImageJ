# -*- coding: utf-8 -*-
# channelop.py - High-level interface to manipulate channels
# Copyright © 2019 Damien Goutte-Gattat

"""High-level interface to manipulate channels in hyperstacks."""

from ij import IJ, ImagePlus
from ij.process import AutoThresholder

from qmul.pdcsl.helper import auto_threshold, apply_mask


def _do_copy_op(image, arg):
    return image.getProcessor().duplicate()


def _do_mask_op(image, arg):
    thresholder = AutoThresholder.Method.valueOf(arg)
    return auto_threshold(image, thresholder).getProcessor()


def _do_apply_op(image,arg):
    src = image.getProcessor().duplicate()
    mask_index = int(arg)
    image.setC(mask_index)
    mask = image.getProcessor().duplicate()

    return apply_mask(src, mask)


def _do_channel_operation(image, op):
    name,arg = op[:-1].split('(')

    if name == 'COPY':
        return _do_copy_op(image, arg)
    elif name == 'MASK':
        return _do_mask_op(image, arg)
    elif name == 'APPLY':
        return _do_apply_op(image, arg)

    return None


def apply_channel_op(image, operations, name=None):
    """Apply an operation set to a hyperstack.

    The `operations` parameter is a list of (idx,op) tuples describing
    how to generate the result image. `idx` is the 1-based index of a
    channel in the source image, and `op` is a string indicating the
    operation to perform on that channel.

    Available operations:
    - COPY(): Copy the channel to the final image as is.
    - MASK(thresholder): Create a binary mask from the source channel,
      using the specified thresholding algorithm (see
      ij.process.AutoThresholder.Method for available algorithms).
    - APPLY(x): Apply the binary mask found in channel `x`.

    The resulting images will contain as many channels as there are
    tuples in the `operations` list, in the same order as they appear
    in that list. Slices and frames are kept unchanged.
    """
    nchannels = image.getNChannels()
    nslices = image.getNSlices()
    nframes = image.getNFrames()

    if not name:
        name = image.getTitle()

    result = IJ.createHyperStack(name, image.getWidth(), image.getHeight(),
                                 len(operations), nslices, nframes, 8)
    result.setCalibration(image.getCalibration())

    for i in range(nframes):
        for j in range(nslices):
            for k in range(len(operations)):
                index, op = operations[k]
                image.setPosition(index, j + 1, i + 1)

                ip = _do_channel_operation(image, op)
                result.setPosition(k + 1, j + 1, i + 1)
                result.setProcessor(ip)

    return result


def apply_channel_opstring(image, opstring, name=None, channel_order='BCGYRF'):
    """Apply an operation set specified as a string.

    This function is a wrapper around the `apply_channel_op` function
    allowing to specify the operations to perform as a single string.

    The `opstring` parameter is a comma-separated list of channel
    operations, each operation being itself a colon-separated pair
    indicating the 1-based index of the source channel and the
    operation to perform.

    Examples `opstring` values:
    - "1:COPY(),1:MASK(MinError),2:MASK(MaxEntropy)"
      The resulting image will have three channels: a direct copy of the
      source image's first channel, then that same channel converted to
      a binary image by the MinError algorithm, then the source image's
      second channel converted to a binary image by the MaxEntropy
      algorithm.
    - "1:APPLY(2),1:APPLY(3)"
      Assuming the source image contains three channels and that the
      last two are binary masks, the resulting image will contain two
      channels, each being the result of the application of one of the
      binary masks on the first channel.

    In addition, the function accepts an optional parameter
    `channel_order` whose purpose is to allow to use a letter code in
    the opstring to identify source channels. For example, if
    `channel_order` is 'RGB', the first example above could be written
    like this:
    - "R:COPY(),R:MASK(MinError),G:MASK(MaxEntropy)"

    The rationale behind this feature is to be able to write opstrings
    that are independent of the order of channels in the source images.
    """
    order = {}
    for i, letter in enumerate(channel_order):
        order[letter] = i + 1

    operations = []
    for operation in opstring.split(','):
        channel,opcode = operation.split(':')
        try:
            index = int(channel)
        except:
            index = order[channel]
        operations.append([index, opcode])

    return apply_channel_op(image, operations, name)
