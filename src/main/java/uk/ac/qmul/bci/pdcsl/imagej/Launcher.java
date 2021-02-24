/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2019 Damien Goutte-Gattat
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
