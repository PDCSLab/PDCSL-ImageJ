PDCSL-ImageJ
============

This package provides a collection of ImageJ scripts and plugins from
the Protein Dynamics and Cell Signalling Laboratory (PDCSL) at the Barts
Cancer Institute (BCI), Queen Mary University of London.


Scripts & Plugins
-----------------

Once installed (see next section), scripts and plugins in this package
will be available from ImageJ’s `Plugins>PDCSL` menu.

* `Foci Counter`: Intended for counting counting ɣH2A.X foci.

* `Nuclei Counter`: Intended for counting cell nuclei in fly tissues.

* `OC Masker`: Create masks for OncoChrome-positive regions.

* `OC Volume Counter`: Extract volume of OncoChrome-positive regions.


Batch Scripts
-------------

Scripts intended to be run on a lot of images in batch mode (instead of
a single, already opened image) will be available in the
`Plugins>PDCSL>Batch` menu.

* `Generic Volumetric Analysis`: Extract the volumes of regions
  resulting from applying user-defined masks.
  
* `OC Repo Counter`: Extract the number of Repo-positive nuclei in
  OncoChrome-positive regions.
  
* `OC Volumetric Analysis`: Extract volume of OncoChrome-positive
  regions.
  
* `Quantify Wing Discs`: Intended to quantify fluorescence signal in
  anterior and posterior compartments of fly wing discs.


Dependencies
------------

Beyond the packages that should be part of any Fiji installation, this
package also depends on the
[incenp-plugins](https://incenp.org/dvlpt/imagej-plugins/) package,
which is available at
<https://git.incenp.org/damien/imagej-plugins/releases>.


Build and Install
-----------------

Build the JAR files by running `mvn`::

```
$ mvn package
```

Install the generated jar file `target/pdcsl-imagej-x.y.z.jar` in the
`$IMAGEJ/plugins` folder.


Copying
-------

PDCSL-ImageJ is distributed under the terms of the GNU General Public
License, version 3 or higher. The full license is included in the
[COPYING file](COPYING) of the source distribution.
