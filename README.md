PDCSL-ImageJ
============

This package provides a collection of ImageJ scripts from the Protein
Dynamics and Cell Signalling Laboratory (PDCSL) at the Barts Cancer
Institute (BCI), Queen Mary University of London.


Modules
-------

This package provides the following modules, to be used in scripts:

* `qmul.pdcsl.helper`: Miscellaneous helper functions

* `qmul.pdcsl.channelop`: High-level functions to manipulate channels

* `qmul.pdcsl.features`: Helper module to analyze object features

Refer to the built-in documentation in the module themselves for
informations about how to use those modules.


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

If necessary, explicitly specify the Java version, e.g. for Java 10::

```
$ mvn -Dscijava.jvm.build.version=10 package
```

Install the helper library `pdcsl-lib/target/pdcsl-lib-x.y.z.jar` in the
`$IMAGEJ/jars/Lib` folder of your ImageJ/Fiji installation; then install
the scripts library `pdcsl-scripts/target/pdcsl-scripts-x.y.z.jar` in
the `$IMAGEJ/plugins` folder.


Copying
-------

PDCSL-ImageJ is distributed under the terms of the GNU General Public
License, version 3 or higher. The full license is included in the
[COPYING file](COPYING) of the source distribution.
