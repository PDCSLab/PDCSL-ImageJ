/*
 * PDCSL-ImageJ - PDCS Lab’s ImageJ Collection
 * Copyright © 2021 Damien Goutte-Gattat
 */

package uk.ac.qmul.bci.pdcsl.imagej;

import org.incenp.imagej.ChannelMasker;

import ij.ImagePlus;

public class OncoChrome {

    /**
     * Create masks for all OncoChrome fluorophores in a OncoChrome image. This
     * method assumes a typical source image from an OncoChrome experiment,
     * containing at least 4 channels (one for each OncoChrome fluorophore) plus an
     * optional non-OncoChrome channel. It generates a new image containing binary
     * masks for all fluorophores.
     * <p>
     * The resulting image will containing the following channels:
     * <ul>
     * <li>a mask of the entire brain (as obtained my wide thresholding of GFP);
     * <li>a mask of all OncoChrome fluorophores together (if @c withExtra is @c
     * true);
     * <li>the complement of the previous mask (if @c withExtra is @c true);
     * <li>a mask of the mTurquoise signal;
     * <li>a mask of the GFP signal;
     * <li>a mask of the Citrine signal;
     * <li>a mask of the mCherry signal;
     * <li>an untouched copy of the non-OncoChrome channel, if any.
     * </ul>
     * 
     * @param source       the source hyperstack
     * @param channelOrder the channel order specification, where 'C' is mTurquoise,
     *                     'G' is GFP, 'Y' is Citrine, 'R' is mCherry, and 'F' is
     *                     any far-red channel
     * @param withExtra    if @c true, generates 'all OncoChrome' and 'no
     *                     OncoChrome' masks
     * @return the resulting masked image
     */
    public static ImagePlus createMask(ImagePlus source, String channelOrder, boolean withExtra) {
        boolean withNonOCData = source.getNChannels() == 5;

        /* Create the initial masks. */
        String maskCommand = "G:MASK(Huang),C:MASK(Moments),G:MASK(Moments),Y:MASK(Moments),R:MASK(MaxEntropy)";
        if ( withNonOCData ) { /* Include the non-OncoChrome channel. */
            maskCommand += ",F:COPY()";
        }
        ChannelMasker masker = ChannelMasker.createMasker(maskCommand, channelOrder);

        if ( withExtra ) {
            /* Create a combined mask of all OncoChrome channels (2nd channel). */
            String step2 = "1:COPY(),2:APPLY(3,4,5,OR),2:COPY(),3:COPY(),4:COPY(),5:COPY()";

            /*
             * Apply that mask to the entire brain mask, first to get only the part of the
             * brain expressing the OncoChrome (2nd channel), then to get the complement
             * part (3rd channel).
             */
            String step3 = "1:COPY(),1:APPLY(2,AND),1:APPLY(2,XOR),3:COPY(),4:COPY(),5:COPY(),6:COPY()";
            if ( withNonOCData ) { /* Include the non-OncoChrome channel. */
                step2 += ",6:COPY()";
                step3 += ",7:COPY()";
            }

            masker.chain(ChannelMasker.createMasker(step2).chain(ChannelMasker.createMasker(step3)));
        }

        return masker.apply(source, source.getTitle() + " Masks");
    }
}
