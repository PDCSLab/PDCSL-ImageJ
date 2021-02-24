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

public class Info {

    public static String getVersion() {
        return Info.class.getPackage().getImplementationVersion();
    }

    public static String getPackageInfo() {
        return "PDCSLab ImageJ Plugins " + Info.class.getPackage().getImplementationVersion()
                + "\nCopyright © 2019–2021 Damien Goutte-Gattat\n \n"
                + "These plugins are released under the GNU General Public License.";
    }
}
