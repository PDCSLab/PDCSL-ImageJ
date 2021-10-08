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

import java.util.ArrayList;

import org.incenp.imagej.ChannelMasker;

import ij.ImagePlus;

/**
 * A helper class to automatize masking operations on images from OncoChrome and
 * OncoChrome-related systems.
 */
public class OncoChrome {

    private ArrayList<Channel> channels;
    private Channel extraChannel;
    private int nSourceChannels;
    private boolean withControl;
    private ChannelMasker masker;
    private String[] names;

    /**
     * Creates a new instance. This constructor is private, as the intended
     * interface to get an OncoChrome object is through the
     * {@link #getOncoChrome(String)} static method.
     */
    private OncoChrome() {
        channels = new ArrayList<Channel>();
        extraChannel = null;
        nSourceChannels = 0;
        withControl = false;
        masker = null;
        names = null;
    }

    /**
     * Sets a supplementary, non-OncoChrome channel.
     * 
     * @param code one-letter code identifying the extra channel
     * @param mask thresholding algorithm to use for that channel when creating a
     *             mask (may be null or an empty string, in which case the channel
     *             will be simply copied over)
     */
    public void setExtraChannel(char code, String mask) {
        if ( mask != null && mask.isEmpty() ) {
            mask = null;
        }
        extraChannel = new Channel(code, "Extra", mask);
        masker = null;
    }

    /**
     * Enables the production of a control mask. When set to true, when creating
     * masks a supplementary channel will be created, corresponding to the region of
     * the sample not marked by any OncoChrome fluorophore. This assumes that the
     * first mask in the image is designed to represent the entire sample.
     * 
     * @param controlMask true to enable generation of a control mask
     */
    public void setControlMask(boolean controlMask) {
        withControl = controlMask;
        masker = null;
        names = null;
    }

    /**
     * Gets the names of all mask channels. This includes the control channel, if
     * the production of such a channel is enabled; this does not include the extra
     * channel, if any.
     * 
     * @return an array of channel names
     */
    public String[] getChannelNames() {
        if ( names == null ) {
            if ( withControl ) {
                names = new String[channels.size() + 1];
                names[channels.size()] = "Control";
            } else {
                names = new String[channels.size()];
            }

            for ( int i = 0; i < channels.size(); i++ ) {
                names[i] = channels.get(i).name;
            }
        }

        return names;
    }

    /**
     * Gets the number of mask channels. This includes the control channel, if the
     * production of such a channel is enabled; this does not include the extra
     * channel, if any.
     * 
     * @return the number of mask channels
     */
    public int getNChannels() {
        int n = channels.size();
        if ( withControl ) {
            n += 1;
        }

        return n;
    }

    /**
     * Gets the number of source channels. This is the number of channels an image
     * is expected to have (at least) to be compatible with this OncoChrome setup.
     * 
     * @return the number of source channels
     */
    public int getNSourceChannels() {
        return nSourceChannels;
    }

    /**
     * Checks whether an image is compatible with this OncoChrome object. An image
     * is deemed compatible if it contains enough channels (at least one for each
     * OncoChrome fluorophore and optionally one for the extra channel).
     * 
     * @param image the image to check
     * @return true if the image is compatible, false otherwise
     */
    public boolean checkImage(ImagePlus image) {
        int neededChannels = nSourceChannels;

        if ( extraChannel != null )
            neededChannels += 1;

        return image.getNChannels() >= neededChannels;
    }

    /**
     * Gets a ChannelMasker object adapted to this OncoChrome setup. The
     * ChannelMasker will create a new image containing masks for each OncoChrome
     * channel, an optional control mask, and the optional extra channel.
     * 
     * @return a ChannelMasker for this OncoChrome
     */
    public ChannelMasker getMasker() {
        if ( masker == null ) {
            masker = makeMasker();
        }

        return masker;
    }

    /*
     * Creates a ChannelMasker object adapted to this OncoChrome setup. This is the
     * implementation behind the getMasker() method.
     */
    private ChannelMasker makeMasker() {
        StringBuilder builder = new StringBuilder();
        int nChannels = channels.size();

        /*
         * Step 1. Apply the specified mask channels.
         */

        /* First the OncoChrome channels. */
        for ( int i = 0; i < nChannels; i++ ) {
            Channel channel = channels.get(i);
            builder.append(String.format("%c:MASK(%s)", channel.code, channel.mask));
            if ( i < nChannels - 1 ) {
                builder.append(',');
            }
        }

        /* Then the extra, non-OC channel, if any. */
        if ( extraChannel != null ) {
            if ( extraChannel.mask != null ) {
                builder.append(String.format(",%c:MASK(%s)", extraChannel.code, extraChannel.mask));
            } else {
                builder.append(String.format(",%c:COPY()", extraChannel.code));
            }
        }

        /* Create the masker for step 1. */
        ChannelMasker masker = ChannelMasker.createMasker(builder.toString());

        if ( withControl ) {
            /*
             * Step 2. Create an extra channel with the OncoChrome channels combined.
             */
            builder = new StringBuilder();

            /* First copy the OC channels as they are. */
            for ( int i = 0; i < nChannels; i++ ) {
                builder.append(String.format("%d:COPY(),", i + 1));
            }
            /* Then create the combined mask. */
            builder.append("2:APPLY(");
            for ( int i = 2; i < nChannels; i++ ) {
                builder.append(String.format("%d,", i + 1));
            }
            builder.append("OR)");
            /* Carry over the non-OC channel if any. */
            if ( extraChannel != null ) {
                builder.append(String.format(",%d:COPY()", nChannels + 1));
            }
            String step2 = builder.toString();

            /*
             * Step 3. Apply the combined channel to the "total" channel.
             */
            builder = new StringBuilder();
            /* First copy the OC channels as they are. */
            for ( int i = 0; i < nChannels; i++ ) {
                builder.append(String.format("%d:COPY(),", i + 1));
            }
            /* Then apply the combined mask. */
            builder.append(String.format("1:APPLY(%d, XOR)", nChannels + 1));
            /* Carry over the non-OC channel if any. */
            if ( extraChannel != null ) {
                builder.append(String.format(",%d:COPY()", nChannels + 2));
            }
            String step3 = builder.toString();

            /* Create and chain the maskers for steps 2 and 3. */
            masker.chain(ChannelMasker.createMasker(step2).chain(ChannelMasker.createMasker(step3)));
        }

        return masker;
    }

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
     * <li>a mask of the mTurquoise signal;
     * <li>a mask of the GFP signal;
     * <li>a mask of the Citrine signal;
     * <li>a mask of the mCherry signal;
     * <li>a mask of the non-OncoChrome-expressing part of the brain (if @c
     * withControl is @c true);
     * <li>an untouched copy of the non-OncoChrome channel, if any.
     * </ul>
     * 
     * @param source         the source hyperstack
     * @param channelOrder   the channel order specification, where 'C' is
     *                       mTurquoise, 'G' is GFP, 'Y' is Citrine, 'R' is mCherry,
     *                       and 'F' is any far-red channel
     * @param withControl    if @c true, generates the control mask (excluding all
     *                       OncoChrome fluorophores)
     * @param nonOCThreshold the thresholding method to optionally apply to the
     *                       non-OncoChrome channel (if @c null, no thresholding
     *                       will be applied and the non-OncoChrome channel will be
     *                       copied as is)
     * @return the resulting masked image
     */
    public static ImagePlus createMask(ImagePlus source, String channelOrder, boolean withControl,
            String nonOCThreshold) {
        OncoChrome onc = OncoChrome.getOncoChrome("brainv1");
        onc.setControlMask(withControl);
        if ( source.getNChannels() == 5 ) {
            onc.setExtraChannel('F', nonOCThreshold);
        }

        ChannelMasker masker = onc.makeMasker();
        return masker.apply(source, source.getTitle() + " Masks", channelOrder);
    }

    /**
     * Gets an OncoChrome instance for a given OncoChrome setup. This is the
     * intended public interface to get an OncoChrome object. It accepts a string
     * identifier for pre-defined OncoChrome setups.
     * <p>
     * Only one identifier is currently defined:
     * <ul>
     * <li>"brainv1": a setup suitable for use with the OncoChrome v0/v1p on third
     * instar larval brains.
     * </ul>
     * <p>
     * Future versions will add more identifiers, and will also accept a formal
     * description of an arbitrary setup.
     * 
     * @param spec an OncoChrome setup identifier
     * @return an OncoChrome object
     */
    public static OncoChrome getOncoChrome(String spec) {
        if ( spec.equalsIgnoreCase("brainv1") ) {
            OncoChrome onc = new OncoChrome();

            onc.channels.add(new Channel('G', "Total", "Huang"));
            onc.channels.add(new Channel('C', "mTurquoise", "Moments"));
            onc.channels.add(new Channel('G', "GFP", "Moments"));
            onc.channels.add(new Channel('Y', "Citrine", "Moments"));
            onc.channels.add(new Channel('R', "mCherry", "MaxEntropy"));
            onc.nSourceChannels = 4;

            return onc;
        }

        return null;
    }

    /*
     * Helper class representing an OncoChrome channel.
     */
    private static class Channel {
        /* The one-letter code for the channel. */
        private char code;

        /* The publicly-displayed name for the channel. */
        private String name;

        /* The thresholding algorithm to use for masking this channel. */
        private String mask;

        public Channel(char code, String name, String mask) {
            this.code = code;
            this.name = name;
            this.mask = mask;
        }
    }
}
