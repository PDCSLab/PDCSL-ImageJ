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
        int[] channels = Util.parseChannels(image, channelList);

        ImagePlus segmented = ns.segment(image, channels);
        int[] results = Util.countParticles(segmented, 0, 500.0, channels);

        ResultsTable rt = Helper.getResultsTable("Nuclei Counter");
        rt.incrementCounter();
        rt.addLabel(image.getTitle());
        for ( int i = 0; i < channels.length; i++ )
            rt.addValue(String.format("Channel %d", i + 1), results[i]);
        rt.show("Nuclei Counter");

        if ( showSegmentedImage )
            uiService.show(segmented);
        else
            segmented.close();
    }

}
