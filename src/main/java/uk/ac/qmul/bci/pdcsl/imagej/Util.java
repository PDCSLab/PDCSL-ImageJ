/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat
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

import org.incenp.imagej.BinaryOperator;
import org.incenp.imagej.Helper;
import org.incenp.imagej.Masking;

import ij.IJ;
import ij.ImagePlus;
import ij.measure.ResultsTable;
import ij.plugin.filter.ParticleAnalyzer;
import ij.process.ImageProcessor;

/**
 * A class of static helper methods.
 */
public class Util {

    /**
     * Counts particles in all slices in the specified channels of an image. Given a
     * hyperstack, this method runs the Particle Analyzer on the specified channels,
     * returning a count of particles by channel.
     * 
     * The outline images generated by the analyzer will be stored in the @c output
     * ImagePlus object, which is expected to already contain at least as many
     * channels as needed (one for each analyzed channel in the source image).
     * 
     * As a convenience, if the @c output image is the same as the source image, the
     * outlines will be stored in new channels that will be added to the source
     * image.
     * 
     * @param image               the hyperstack to analyze
     * @param minSize             the minimum size of particles to look for
     * @param maxSize             the maximum size of particles to look for
     * @param channels            a list of 1-based channel indexes to analyze
     * @param output              if non-null, outline images generated by the
     *                            particle analyzer will be stored into that
     *                            ImagePlus object
     * @param outputChannelOffset index of the first channel in the output image
     *                            where to store the outline images
     * @return an array containing the count of detected particles in each analyzed
     *         channel
     */
    public static int[] countParticles(ImagePlus image, double minSize, double maxSize, int[] channels,
            ImagePlus output, int outputChannelOffset) {
        int[] particles = new int[channels.length];
        int nslices = image.getNSlices();
        int options = output != null ? ParticleAnalyzer.SHOW_OUTLINES : 0;
        int maxThreshold = (1 << image.getBitDepth()) - 1;

        ResultsTable results = new ResultsTable();
        ParticleAnalyzer analyzer = new ParticleAnalyzer(options, 0, results, minSize, maxSize, 0.0, 1.0);
        analyzer.setHideOutputImage(true);

        if ( output == image ) {
            outputChannelOffset = image.getNChannels() + 1;
            Helper.augmentHyperstack(image, channels.length);
        }

        for ( int i = 0; i < channels.length; i++ ) {
            for ( int j = 0; j < nslices; j++ ) {
                image.setPosition(channels[i], j + 1, 1);
                image.getProcessor().setThreshold(1, maxThreshold, ImageProcessor.NO_LUT_UPDATE);
                analyzer.analyze(image);

                if ( output != null ) {
                    output.setPosition(outputChannelOffset + i, j + 1, 1);
                    output.setProcessor(analyzer.getOutputImage().getProcessor());
                }
            }

            particles[i] = results.getCounter();
            results.reset();
        }

        return particles;
    }

    /**
     * Counts particles in all slices in the specified channels of an image. This
     * method is similar to
     * {@link #countParticles(ImagePlus, double, double, int[], ImagePlus, int)} but
     * does not allow to extract the outline images generated by the Particle
     * Analyzer.
     * 
     * @param image    the hyperstack to analyze
     * @param minSize  the minimum size of particles to look for
     * @param maxSize  the maximum size of particles to look for
     * @param channels a list of 1-based channel indexes to analyze
     * @return an array containing the count of detected particles in each analyzed
     *         channel
     */
    public static int[] countParticles(ImagePlus image, double minSize, double maxSize, int[] channels) {
        return countParticles(image, minSize, maxSize, channels, null, 0);
    }

    /**
     * Apply masks found in an image. This method assumes a source hyperstack
     * containing binary masks in all its channels except the last one. It produces
     * a new hyperstack where all masks have been applied to the last channel.
     * 
     * @param image the source hyperstack
     * @param title the title of the new hyperstack
     * @return the resulting hyperstack
     */
    public static ImagePlus applyMasks(ImagePlus image, String title) {
        int nchannels = image.getNChannels();
        int nslices = image.getNSlices();
        int nframes = image.getNFrames();
        ImagePlus masked = IJ.createHyperStack(title, image.getWidth(), image.getHeight(), nchannels - 1, nslices,
                nframes, 8);

        for ( int i = 0; i < nchannels - 1; i++ ) {
            for ( int j = 0; j < nslices; j++ ) {
                for ( int k = 0; k < nframes; k++ ) {
                    image.setPosition(nchannels, j + 1, k + 1);
                    ImageProcessor src = image.getProcessor().duplicate();
                    image.setPosition(i + 1, j + 1, k + 1);
                    masked.setPosition(i + 1, j + 1, k + 1);

                    masked.setProcessor(
                            Masking.applyMask(src, image.getProcessor(), BinaryOperator.AND, Masking.NO_DUPLICATE));
                }
            }
        }

        return masked;
    }

    /**
     * Apply masks found in an image. This method is similar
     * {@link #applyMasks(ImagePlus, String)} but gives the resulting image a
     * default title.
     * 
     * @param image the source hyperstack
     * @return the resulting hyperstack
     */
    public static ImagePlus applyMasks(ImagePlus image) {
        return applyMasks(image, image.getTitle() + " Masked");
    }

    /**
     * Parse a string into a list of channel indexes. The string can contain space-,
     * comma-, or semicolon-separated channel indexes, the keyword "current" (or
     * "selected") to indicate the currently selected channel, or the keyword "all"
     * to indicate all channels in the image. An empty string (or @c null) is
     * treated the same as the "current" keyword.
     * 
     * @param image the image the channel indexes refer to
     * @param spec  the string to parse
     * @return the list of channel indexes
     */
    public static int[] parseChannels(ImagePlus image, String spec) {
        int nSourceChannels = image.getNChannels();
        int channels[];

        if ( spec == null || spec.isEmpty() || spec.equalsIgnoreCase("current") || spec.equalsIgnoreCase("selected") ) {
            channels = new int[1];
            channels[0] = image.getC();
        } else if ( spec.equalsIgnoreCase("all") ) {
            channels = new int[nSourceChannels];
            for ( int i = 0; i < nSourceChannels; i++ ) {
                channels[i] = i + 1;
            }
        } else {
            String tokens[] = spec.split(" +|, *|; *");
            channels = new int[tokens.length];
            for ( int i = 0; i < tokens.length; i++ ) {
                try {
                    channels[i] = Integer.parseInt(tokens[i]);
                } catch ( NumberFormatException nfe ) {
                    throw new IllegalArgumentException(String.format("Invalid channel specification: %s", tokens[i]));
                }

                if ( channels[i] < 1 || channels[i] > nSourceChannels ) {
                    throw new IllegalArgumentException(String.format("Channel index out of scope: %d", channels[i]));
                }
            }
        }

        return channels;
    }
}
