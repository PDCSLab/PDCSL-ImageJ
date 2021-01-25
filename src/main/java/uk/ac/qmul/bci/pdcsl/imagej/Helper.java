/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat
 */

package uk.ac.qmul.bci.pdcsl.imagej;

import ij.ImagePlus;
import ij.measure.ResultsTable;
import ij.plugin.filter.ParticleAnalyzer;

/**
 * A class of static helper methods.
 */
public class Helper {

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

        ResultsTable results = new ResultsTable();
        ParticleAnalyzer analyzer = new ParticleAnalyzer(options, 0, results, minSize, maxSize, 0.0, 1.0);
        analyzer.setHideOutputImage(true);

        if ( output == image ) {
            outputChannelOffset = image.getNChannels() + 1;
            org.incenp.imagej.Helper.augmentHyperstack(image, channels.length);
        }

        for ( int i = 0; i < channels.length; i++ ) {
            for ( int j = 0; j < nslices; j++ ) {
                image.setPosition(channels[i], j + 1, 1);
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
}