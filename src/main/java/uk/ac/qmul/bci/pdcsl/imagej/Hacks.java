/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the Gnu General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

package uk.ac.qmul.bci.pdcsl.imagej;

import ij.IJ;
import ij.ImagePlus;
import ij.process.ImageProcessor;

/**
 * Hacks collection.
 * 
 * This class is intended to host all kinds of hacks or dubious methods.
 */
public class Hacks {

    /**
     * Checks if a given image is entirely black.
     * 
     * @param processor the image to check
     * @return true if the image only contains black pixels, false otherwise
     */
    public static boolean isBlackImage(ImageProcessor processor) {
        int[][] pixels = processor.getIntArray();
        int width = processor.getWidth();
        int height = processor.getHeight();

        /*
         * XXX Some thresholding algorithms, when unable to threshold an image properly,
         * would give a completely black image save for a 1-pixel wide white border. We
         * need to exclude that border here.
         */
        for ( int i = 1; i < width - 1; i++ )
            for ( int j = 1; j < height - 1; j++ )
                if ( pixels[i][j] > 0 )
                    return false;

        return true;
    }

    /**
     * Removes all Z-slices for which at least one channel contains only a black
     * image.
     * 
     * @param image the hyperstack to process
     * @return a new hyperstack with the Z-slices removed
     */
    public static ImagePlus removeBlackSlices(ImagePlus image) {
        int[] slices = new int[image.getNSlices()];
        int nslice = 0;

        for ( int j = 0; j < image.getNSlices(); j++ ) {
            boolean hasBlackChannel = false;

            for ( int i = 0; i < image.getNChannels(); i++ ) {
                image.setPosition(i + 1, j + 1, 1);
                if ( isBlackImage(image.getProcessor()) )
                    hasBlackChannel = true;
            }

            if ( !hasBlackChannel )
                slices[nslice++] = j + 1;
        }

        ImagePlus result = IJ.createHyperStack(image.getTitle(), image.getWidth(), image.getHeight(),
                image.getNChannels(), nslice, 1, image.getBitDepth());
        result.setCalibration(image.getCalibration());

        for ( int j = 0; j < nslice; j++ ) {
            for ( int i = 0; i < image.getNChannels(); i++ ) {
                image.setPosition(i + 1, slices[j], 1);
                result.setPosition(i + 1, j + 1, 1);
                result.setProcessor(image.getProcessor().duplicate());
            }
        }

        return result;
    }
}
