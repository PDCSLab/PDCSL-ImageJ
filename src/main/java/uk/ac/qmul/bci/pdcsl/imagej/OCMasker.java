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

import java.util.ArrayList;

import org.incenp.imagej.ThresholdingMethod;
import org.scijava.Initializable;
import org.scijava.command.Command;
import org.scijava.command.DynamicCommand;
import org.scijava.module.MutableModuleItem;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

import ij.ImagePlus;

@Plugin(type = Command.class, menuPath = "Plugins>PDCSL>OC Masker")
public class OCMasker extends DynamicCommand implements Initializable {

    @Parameter
    private ImagePlus image;

    @Parameter(label = "OncoChrome setup")
    private String oncoChromeSetup;

    @Parameter(label = "Custom OncoChrome setup", required = false)
    private String customOncoChromeSetup;

    @Parameter(label = "Order of channels")
    private String channelOrder;

    @Parameter(label = "Thresholding algorithm for non-OC channel ('F')")
    private String nonOCThreshold;

    @Parameter(label = "Compute control mask")
    private boolean withControlMask;

    @Parameter(label = "Apply the masks")
    private boolean applyMasks;

    @Parameter
    private UIService uiService;

    @Override
    public void run() {
        if ( customOncoChromeSetup != null && !customOncoChromeSetup.isEmpty() ) {
            oncoChromeSetup = customOncoChromeSetup;
        }

        OncoChrome oncoChrome = OncoChrome.getOncoChrome(oncoChromeSetup);
        oncoChrome.setControlMask(withControlMask);

        if ( image.getNChannels() > oncoChrome.getNSourceChannels() ) {
            if ( nonOCThreshold == "NONE" )
                nonOCThreshold = null;
            oncoChrome.setExtraChannel('F', nonOCThreshold);
        }

        ImagePlus masks = oncoChrome.getMasker().apply(image, image.getTitle() + " Masks", channelOrder);
        uiService.show(masks);

        if ( applyMasks ) {
            ImagePlus masked = Util.applyMasks(masks, image.getTitle() + " Masked");
            uiService.show(masked);
        }
    }

    @Override
    public void initialize() {
        final MutableModuleItem<String> setupItem = getInfo().getMutableInput("oncoChromeSetup", String.class);
        setupItem.setChoices(OncoChrome.getPredefinedSetups());

        ArrayList<String> algos = new ArrayList<String>();
        algos.add("NONE");
        for ( ThresholdingMethod m : ThresholdingMethod.values() ) {
            if ( m == ThresholdingMethod.FIXED )
                continue;
            algos.add(m.toString());
        }

        final MutableModuleItem<String> nonOCThresholdItem = getInfo().getMutableInput("nonOCThreshold", String.class);
        nonOCThresholdItem.setChoices(algos);
    }
}
