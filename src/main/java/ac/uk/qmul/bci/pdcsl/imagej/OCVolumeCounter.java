/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
 */

package ac.uk.qmul.bci.pdcsl.imagej;

import org.incenp.imagej.ChannelMasker;
import org.incenp.imagej.Helper;
import org.scijava.command.Command;
import org.scijava.log.LogService;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

import ij.ImagePlus;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>OC Volume Counter")
public class OCVolumeCounter implements Command {

    private static String maskCommand = "G:MASK(Huang),C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy)";

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Order of channels:")
    private String channelOrder;

    @Parameter
    private UIService uiService;

    @Parameter
    private LogService logService;

    @Override
    public void run() {
        ImagePlus masks = ChannelMasker.applyMasker(image, maskCommand, image.getTitle() + " Masks", channelOrder);
        uiService.show(masks);

        double[] volumes = Helper.extractVolumes(masks);
        StringBuilder fmt = new StringBuilder();
        fmt.append(image.getTitle());
        for ( double volume : volumes )
            fmt.append(String.format(",%.2f", volume));
        logService.info(fmt.toString());
    }

}
