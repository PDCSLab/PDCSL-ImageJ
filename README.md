PDCSL-ImageJ
============

This package provides a collection of ImageJ scripts from the Protein
Dynamics and Cell Signalling Laboratory (PDCSL) at the Barts Cancer
Institute (BCI), Queen Mary University of London.


Scripts
-------

Once installed (see next section), scripts in this package will be
available from ImageJ’s `Plugins>PDCSL` menu.

* `Foci Counter`: Intended for counting counting ɣH2A.X foci

* `Nuclei Counter`: Intended for counting cell nuclei in fly tissues

* `OC Masker`: Create masks for OncoChrome-positive regions

* `OC Volume Counter`: Extract volume of OncoChrome-positive regions


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
