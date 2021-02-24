/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019, 2021 Damien Goutte-Gattat
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

import org.incenp.imagej.Helper;
import org.incenp.imagej.NucleiSegmenter;
import org.scijava.command.Command;
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

    @Parameter(label = "Channel(s) to process", required = false)
    private String channelList;

    @Parameter(label = "Show the segmented image")
    private boolean showSegmentedImage;

    @Parameter
    private UIService uiService;

    @Override
    public void run() {
        NucleiSegmenter ns = new NucleiSegmenter(2.0);
        ResultsTable rt = new ResultsTable();
        ParticleAnalyzer pa = new ParticleAnalyzer(ParticleAnalyzer.DISPLAY_SUMMARY, 0, rt, 0.0, 500.0, 0.0, 1.0);

        int[] channels = Util.parseChannels(image, channelList);
        ImagePlus segmented = ns.segment(image, channels);

        ResultsTable rt2 = Helper.getResultsTable("Nuclei Counter");
        rt2.incrementCounter();
        rt2.addLabel(image.getTitle());

        int counter = 0;

        for ( int i = 0; i < channels.length; i++ ) {
            int value = 0;
            for ( int j = 0; j < segmented.getNSlices(); j++ ) {
                segmented.setPosition(i + 1, j + 1, 1);

                if ( pa.analyze(segmented) ) {
                    int n = rt.getCounter() - counter;
                    counter = rt.getCounter();
                    value += n;
                }
            }
            rt2.addValue(String.format("Channel %d", i + 1), value);
        }

        rt2.show("Nuclei Counter");

        if ( showSegmentedImage )
            uiService.show(segmented);
        else
            segmented.close();
    }

}
