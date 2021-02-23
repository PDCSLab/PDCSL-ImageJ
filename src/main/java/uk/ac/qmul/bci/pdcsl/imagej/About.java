/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat
 */

package uk.ac.qmul.bci.pdcsl.imagej;

import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;
import org.scijava.ui.UIService;

@Plugin(type = Command.class, menuPath = "Help>About Plugins>PDCSL Plugins...")
public class About implements Command {

    @Parameter
    private UIService uiService;

    @Override
    public void run() {
        uiService.showDialog(Info.getPackageInfo(), "About PDCSLab Plugins");
    }

}
