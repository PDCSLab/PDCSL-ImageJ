/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat
 */

package uk.ac.qmul.bci.pdcsl.imagej;

public class Info {

    public static String getVersion() {
        return Info.class.getPackage().getImplementationVersion();
    }

    public static String getPackageInfo() {
        return "PDCSLab ImageJ Plugins " + Info.class.getPackage().getImplementationVersion()
                + "\nCopyright © 2019–2021 Damien Goutte-Gattat";
    }
}
