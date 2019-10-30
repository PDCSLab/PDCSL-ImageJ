/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
 */

package ac.uk.qmul.bci.pdcsl.imagej;

import org.incenp.imagej.ChannelMasker;
import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

import ij.ImagePlus;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>OC Masker")
public class OCMasker implements Command {

    private static String maskCommand = "C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy),F:COPY()";
    private static String applyCommand = "5:APPLY(1),5:APPLY(2),5:APPLY(3),5:APPLY(4),5:COPY()";

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Order of channels:")
    private String channelOrder;

    @Parameter
    private UIService uiService;

    @Override
    public void run() {
        ImagePlus masks = ChannelMasker.applyMasker(image, maskCommand, image.getTitle() + " Masks", channelOrder);
        uiService.show(masks);

        ImagePlus masked = ChannelMasker.applyMasker(masks, applyCommand, image.getTitle() + " Masked", null);
        uiService.show(masked);
    }

}
