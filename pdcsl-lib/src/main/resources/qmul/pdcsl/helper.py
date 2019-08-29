# -*- coding: utf-8 -*-

from ij.plugin.filter import Binary

def apply_binary_filters(filters, image):
    """Apply the named binary filters sequentially to the image."""
    bf = Binary()
    for name in filters:
        bf.setup(name, image)
        bf.run(image.getProcessor())
