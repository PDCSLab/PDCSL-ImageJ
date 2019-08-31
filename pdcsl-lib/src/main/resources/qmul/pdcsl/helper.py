# -*- coding: utf-8 -*-
# Helper.py - Common helper functions
# Copyright © 2019 Damien Goutte-Gattat

from ij.plugin.filter import Binary


def apply_binary_filters(filters, image):
    """Apply the named binary filters sequentially to the image."""
    bf = Binary()
    for name in filters:
        bf.setup(name, image)
        bf.run(image.getProcessor())
