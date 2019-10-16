# -*- coding: utf-8 -*-
# batch.py - Helper functions for batch processing
# Copyright © 2019 Damien Goutte-Gattat

"""Helper functions for batch processing."""

import os

from ij import IJ
from loci.plugins import BF

from qmul.pdcsl.helper import parse_csv_batch, get_bioformats_extensions


def _format_header(fields, result_info):
    fmt = "Image" + ",{}" * len(fields) + ",{}" * len(result_info)
    items = fields + [a for a, b in result_info]
    return fmt.format(*items)


def _format_result(title, fields, result_info, results):
    fmt = "{}" + ",{}" * len(fields) + "," + ",".join([b for a, b in result_info])
    items = [title] + fields + results
    return fmt.format(*items)


def _process_file(pathname, func, result_info, fields, options):
    images = BF.openImagePlus(pathname)
    for image in images:
        results = func(image, fields=fields, **options)
        if results:
            result = _format_result(image.getTitle(), fields, result_info, results)
            IJ.log(result)

        image.close()


def run_batch(pathname, func, result_info, options={}, default_fields=[]):
    """Run a batch analysis.

    This function opens the image(s) specified by the `pathname`
    argument and calls the `func` analysis procedure on each image.

    The pathname can point to: a folder containing the image files to
    process; an image file (which may itself contain several images);
    or a CSV file which is then expected to contain a list of image
    filenames. Here is an example CSV file:

    ```
    #HDR:Image,Field1,Field2
    file1.lsm,value1,value2
    file2.nd,value1,value2
    ```

    The image filenames should always be in the first column. If there
    are more columns, they will be copied verbatim in the output.

    The `func` argument is a function to be called on each image. That
    function should have the following signature:

    ```
    func(image, fields, [options])
    ```

    where `image` is the ij.ImagePlus object to process, `fields` is a
    list containing all the extra fields from the CSV file (or from the
    `default_fields` argument is the image does not come from a CSV
    file). The function may accept any other keyword argument. The
    values from the `options` dictionary will be passed to the function
    as keyword arguments.

    The `result_info` argument is a list of tuples describing the
    values returned by the processing function. Each tuple should
    contain a header name and a format string. The processing function
    should return a list containing as many values as there are tuples
    in the `result_info` argument.

    The `default_fields` argument is used when `pathname` does not
    point to a CSV file. It is a list of tuples containing a header name
    and a default value.

    All output will be written to the ImageJ's log.

    Example usage:

    ```
    def process_image(image, fields, foobar=False):
        val1 = extract_value_from_image(image)
        val2 = extract_another_value(image)
        if foorbar:
            val2 *= 2
        return [val1, val2]

    run_batch("file.csv",
              process_image,
              [('Value 1', '{}'), ('Value 2', '{:.2f}')],
              options={'foobar': True})
    ```
    """
    if os.path.isdir(pathname):
        header = _format_header([a for a, b in default_fields], result_info)
        IJ.log(header)
        extensions = get_bioformats_extensions()
        filenames = [os.path.join(pathname, fn) for fn in os.listdir() if os.path.splitext(fn)[1] in extensions]
        for filename in filenames:
            _process_file(filename, func, result_info, [b for a, b in default_fields], options)
    elif not pathname.endswith('.csv'):
        header = _format_header([a for a, b in default_fields], result_info)
        IJ.log(header)
        _process_file(pathname, func, result_info, [b for a, b in default_fields], options)
    else:
        batch, headers = parse_csv_batch(pathname)
        header = _format_header(headers[1:], result_info)
        IJ.log(header)
        for task in batch:
            _process_file(task[0], func, result_info, task[1:], options)
