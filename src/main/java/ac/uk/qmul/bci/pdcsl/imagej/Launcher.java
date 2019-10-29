/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
 */

package ac.uk.qmul.bci.pdcsl.imagej;

import net.imagej.ImageJ;

/**
 * ImageJ Launcher.
 * 
 * The purpose of this class is solely to start ImageJ from within the IDE to
 * ease development and debugging.
 */
public class Launcher {

    public static void main(String[] args) {
        ImageJ ij = new ImageJ();
        ij.ui().showUI();
    }

}
