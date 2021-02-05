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

    @Parameter(label = "Channels to process:", required = false)
    private String channels;

    @Override
    public void run() {
        double[] volumes = Helper.extractVolumes(image, Util.parseChannels(image, channels));

        ResultsTable rt = Helper.getResultsTable("Volume Counter");
        rt.incrementCounter();
        rt.addLabel(image.getTitle());
        for ( int i = 0; i < volumes.length; i++ ) {
            rt.addValue(String.format("Channel %d", i + 1), volumes[i]);
        }
        rt.show("Volume Counter");
    }
}
