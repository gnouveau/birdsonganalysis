"""Plotting function for birdsonganalysis."""

import numpy as np


import seaborn as sns

import matplotlib.patches as p
import matplotlib.pyplot as plt

from .songfeatures import spectral_derivs
from .constants import FREQ_RANGE


def spectral_derivs_plot(spec_der, contrast=0.1, ax=None, freq_range=None,
                         fft_step=None, fft_size=None):
    """
    Plot the spectral derivatives of a song in a grey scale.

    spec_der - The spectral derivatives of the song (computed with
               `spectral_derivs`) or the song itself
    contrast - The contrast of the plot
    ax - The matplotlib axis where the plot must be drawn, if None, a new axis
         is created
    freq_range - The amount of frequency to plot, usefull only if `spec_der` is
                 a song. Given to `spectral_derivs`
    ov_params - The Parameters to override, passed to `spectral_derivs`
    """
    if spec_der.ndim == 1:
        spec_der = spectral_derivs(spec_der, freq_range, fft_step, fft_size)
    ax = sns.heatmap(spec_der.T, yticklabels=50, xticklabels=50,
                     vmin=-contrast, vmax=contrast, ax=ax, cmap='Greys',
                     cbar=False)
    ax.invert_yaxis()
    return ax


def plot_over_spec(data, ax, freq_range=FREQ_RANGE, zoom=1, **plot_params):
    """
    Plot the feature over a spectral derivatives plot.

    The data are first normalized then rescale to fit the ylim of the axis.
    """
    # Normalize the data so that they fit in the graph
    ndata = (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))
    # We take for abscisse axis the line corresponding to 5% of freq_range
    # We rescale the data so that they take 75% of the graph
    ax.plot(zoom * (5/100 * freq_range + 75/100 * freq_range * ndata),
            **plot_params)
    return ax


def similarity_plot(sim, song, refsong):
    """Do a similarity plot with the result of `bsa.similarity`."""
    fig, ax = plt.subplots(2, 2, figsize=(13, 13),
                           gridspec_kw={'width_ratios': [1, 4],
                                        'height_ratios': [1, 4]})
    ax[0, 0].axis('off')
    sds = spectral_derivs(song)
    sdr = spectral_derivs(refsong)
    ax[0, 1] = spectral_derivs_plot(sds, 0.05, ax[0, 1])
    ax[0, 1].set_title('Song')
    ax[1, 0] = spectral_derivs_plot(np.flip(sdr.T, 1), 0.05,
                                    ax[1, 0])
    ax[1, 0].set_title('Reference Song')
    ax[1, 1] = sns.heatmap(sim['glob_matrix'], ax=ax[1, 1], cbar=False,
                           vmin=0, vmax=1)
    for section in sim['sections']:
        xy = (section['beg'][0],
              sim['glob_matrix'].shape[1] - section['end'][1])
        width = section['end'][0] - section['beg'][0]
        height = section['end'][1] - section['beg'][1]
        ax[1, 1].add_patch(p.Rectangle(xy, width, height, fill=False,
                                       edgecolor='y', linewidth=3))
    return fig
