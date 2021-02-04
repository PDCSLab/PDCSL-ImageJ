/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat 
 */

package uk.ac.qmul.bci.pdcsl.imagej;

import org.incenp.imagej.Helper;
import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;

import ij.ImagePlus;
import ij.measure.ResultsTable;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>Volume Counter")
public class VolumeCounter implements Command {

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Channels to process (comma-separated):", required = false)
    private String channels;

    @Override
    public void run() {
        double[] volumes;

        if ( channels.isEmpty() ) {
            volumes = Helper.extractVolumes(image);
        } else {
            String[] channelSpecs = channels.split(",");
            int[] channelIndexes = new int[channelSpecs.length];

            for ( int i = 0; i < channelSpecs.length; i++ ) {
                try {
                    channelIndexes[i] = Integer.parseInt(channelSpecs[i]);
                } catch ( NumberFormatException nfe ) {
                    throw new IllegalArgumentException(
                            String.format("Invalid channels specification:", channelSpecs[i]));
                }
            }
            volumes = Helper.extractVolumes(image, channelIndexes);
        }

        ResultsTable rt = Helper.getResultsTable("Volume Counter");
        rt.incrementCounter();
        rt.addLabel(image.getTitle());
        for ( int i = 0; i < volumes.length; i++ ) {
            rt.addValue(String.format("Channel %d", i + 1), volumes[i]);
        }
        rt.show("Volume Counter");
    }
}
