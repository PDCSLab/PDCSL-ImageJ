/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
 */

package uk.ac.qmul.bci.pdcsl.imagej;

import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

import ij.ImagePlus;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>OC Masker")
public class OCMasker implements Command {

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Order of channels:")
    private String channelOrder;

    @Parameter(label = "Compute extra masks:")
    private boolean withExtraMasks;

    @Parameter(label = "Apply the masks:")
    private boolean applyMasks;

    @Parameter
    private UIService uiService;

    @Override
    public void run() {
        ImagePlus masks = OncoChrome.createMask(image, channelOrder, withExtraMasks);
        uiService.show(masks);

        if ( applyMasks ) {
            ImagePlus masked = Helper.applyMasks(masks, image.getTitle() + " Masked");
            uiService.show(masked);
        }
    }
}
