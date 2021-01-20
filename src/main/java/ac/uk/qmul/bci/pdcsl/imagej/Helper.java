/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat
 */

package ac.uk.qmul.bci.pdcsl.imagej;

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
     * @param image    the hyperstack to analyze
     * @param minSize  the minimum size of particles to look for
     * @param maxSize  the maximum size of particles to look for
     * @param channels a list of 1-based channel indexes to analyze
     * @return an array containing the count of detected particles in each analyzed
     *         channel
     */
    public static int[] countParticles(ImagePlus image, double minSize, double maxSize, int[] channels) {
        int[] particles = new int[channels.length];
        int nslices = image.getNSlices();

        ResultsTable results = new ResultsTable();
        ParticleAnalyzer analyzer = new ParticleAnalyzer(0, 0, results, minSize, maxSize, 0.0, 1.0);

        for ( int i = 0; i < channels.length; i++ ) {
            for ( int j = 0; j < nslices; j++ ) {
                image.setPosition(channels[i], j + 1, 1);
                analyzer.analyze(image);
            }

            particles[i] = results.getCounter();
            results.reset();
        }

        return particles;
    }
}
