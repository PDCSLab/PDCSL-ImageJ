PDCSL-ImageJ
============

This package provides a collection of ImageJ scripts from the Protein
Dynamics and Cell Signalling Laboratory (PDCSL) at the Barts Cancer
Institute (BCI), Queen Mary University of London.


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
