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

import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

import ij.ImagePlus;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>OC Masker")
public class OCMasker implements Command {

    @Parameter
    private ImagePlus image;

    @Parameter(label = "Order of channels")
    private String channelOrder;

    @Parameter(label = "Thresholding algorithm for non-OC channel", required = false)
    private String nonOCThreshold;

    @Parameter(label = "Compute control mask")
    private boolean withControlMask;

    @Parameter(label = "Apply the masks")
    private boolean applyMasks;

    @Parameter
    private UIService uiService;

    @Override
    public void run() {
        ImagePlus masks = OncoChrome.createMask(image, channelOrder, withControlMask,
                nonOCThreshold.isEmpty() ? null : nonOCThreshold);
        uiService.show(masks);

        if ( applyMasks ) {
            ImagePlus masked = Util.applyMasks(masks, image.getTitle() + " Masked");
            uiService.show(masked);
        }
    }
}
