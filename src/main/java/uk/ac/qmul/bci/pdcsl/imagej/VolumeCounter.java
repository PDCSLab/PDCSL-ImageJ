/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat
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
import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;

import ij.ImagePlus;
import ij.measure.ResultsTable;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>Volume Counter")
public class VolumeCounter implements Command {

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Channels to process", required = false)
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
