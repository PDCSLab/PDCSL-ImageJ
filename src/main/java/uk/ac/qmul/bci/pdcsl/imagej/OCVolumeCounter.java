/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
 */

package uk.ac.qmul.bci.pdcsl.imagej;

import org.incenp.imagej.ChannelMasker;
import org.incenp.imagej.Helper;
import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

import ij.ImagePlus;
import ij.measure.ResultsTable;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>OC Volume Counter")
public class OCVolumeCounter implements Command {

	private static ChannelMasker masker = ChannelMasker.createMasker("G:MASK(Huang),C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy)");

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Order of channels:")
    private String channelOrder;

    @Parameter
    private UIService uiService;

    @Override
    public void run() {
        ImagePlus masks = masker.apply(image, image.getTitle() + " Masks", channelOrder);
        uiService.show(masks);

        ResultsTable rt = Helper.getResultsTable("OC Volume Counter");
        rt.incrementCounter();
        rt.addLabel(image.getTitle());

        double[] volumes = Helper.extractVolumes(masks);
        for ( int i = 0; i < volumes.length; i++ ) {
            rt.addValue(String.format("Channel %d", i + 1), volumes[i]);
        }
        rt.show("OC Volume Counter");
    }

}
