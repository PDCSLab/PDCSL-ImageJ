package ac.uk.qmul.bci.pdcsl.imagej;

import net.imagej.ImageJ;

public class Launcher {

    public static void main(String[] args) {
        ImageJ ij = new ImageJ();
        ij.ui().showUI();
    }

}
