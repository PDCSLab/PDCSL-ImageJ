/*
 * Merge_C5 - Merge 5th channel to 4-channel images
 * Copyright © 2019 Damien Goutte-Gattat
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

macro "Merge C5" {

    if ( nImages > 0 ) {
        exit("Please close all opened images before running this macro.")
    }

    setBatchMode(true);

    src_dir = getDirectory("Choose source directory");
    process_files(src_dir);
}

function process_files(dir) {
    file_list = getFileList(dir);

    for ( i = 0; i < file_list.length; i++ ) {
    	print("Processing ", file_list[i]);
        if ( endsWith(file_list[i], "/") ) {
            /* Process subdirectories. */
            process_files(dir+file_list[i]);
        }
        else {
            if ( matches(file_list[i], ".*_[0-9][0-9][a-z]?.lsm") ) {
                img_file = dir + File.separator + file_list[i];
                base = replace(file_list[i], "\.lsm", "");

                c5_file = get_fifth_channel_file(dir, base);
                if ( c5_file != "" ) {
                    process_image(img_file, c5_file);
                }
            }
        }
    }
}

function get_fifth_channel_file(dir, base) {
    file_list = getFileList(dir);

    for ( i = 0; i < file_list.length; i++ ) {
        if ( matches(file_list[i], base + "_([^_]+).lsm") ) {
            return dir + File.separator + file_list[i];
        }
    }

    return "";
}

function process_image(img_file, c5_file) {
    print("Opening ", img_file);
    run("Bio-Formats Importer", "open='" + img_file + "' use_virtual_stack color_mode=Composite open_all_series view=Hyperstack");
    dir_name = File.directory;
    base_name = File.nameWithoutExtension;
    c14_name = File.name;

    run("Split Channels");

    print("Opening ", c5_file);
    run("Bio-Formats Importer", "open='" + c5_file + "' color_mode=Composite open_all_series view=Hyperstack");
    c5_name = File.name;

    run("Merge Channels...", "c1=C1-" + c14_name + " c2=C3-" + c14_name + " c3=C4-" + c14_name + " c4=C2-" + c14_name + " c5=" + c5_name + " create");

    saveAs("Tiff", dir_name + File.separator + base_name + ".tif");
    close();
}
