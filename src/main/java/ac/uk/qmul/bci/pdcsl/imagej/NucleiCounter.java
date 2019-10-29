/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
 */

package ac.uk.qmul.bci.pdcsl.imagej;

import org.incenp.imagej.NucleiSegmenter;
import org.scijava.command.Command;
import org.scijava.log.LogService;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

import ij.ImagePlus;
import ij.measure.ResultsTable;
import ij.plugin.filter.ParticleAnalyzer;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>Nuclei Counter")
public class NucleiCounter implements Command {

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Process all channels?")
    private boolean allChannels;

    @Parameter(label = "Show the segmented image?")
    private boolean showSegmentedImage;

    @Parameter
    private UIService uiService;

    @Parameter
    private LogService logService;

    @Override
    public void run() {
        NucleiSegmenter ns = new NucleiSegmenter(2.0);
        ResultsTable rt = new ResultsTable();
        ParticleAnalyzer pa = new ParticleAnalyzer(ParticleAnalyzer.DISPLAY_SUMMARY, 0, rt, 0.0, 500.0, 0.0, 1.0);

        int[] channels;
        if ( allChannels ) {
            channels = new int[image.getNChannels()];
            for ( int i = 0; i < image.getNChannels(); i++ )
                channels[i] = i + 1;
        } else {
            channels = new int[1];
            channels[0] = image.getC();
        }

        ImagePlus segmented = ns.segment(image, channels);

        int counter = 0;
        int[] values = new int[channels.length];

        for ( int i = 0; i < channels.length; i++ ) {
            for ( int j = 0; j < segmented.getNSlices(); j++ ) {
                segmented.setPosition(i + 1, j + 1, 1);

                if ( pa.analyze(segmented) ) {
                    int n = rt.getCounter() - counter;
                    counter = rt.getCounter();
                    values[i] += n;
                }
            }
        }

        if ( showSegmentedImage )
            uiService.show(segmented);
        else
            segmented.close();

        StringBuilder fmt = new StringBuilder();
        fmt.append(image.getTitle());
        for ( int value : values )
            fmt.append(String.format(",%d", value));
        logService.info(fmt.toString());
    }

}
