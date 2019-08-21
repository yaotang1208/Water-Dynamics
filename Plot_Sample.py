import datetime

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib import mlab

from mpl_toolkits.axes_grid1 import make_axes_locatable

def main():
    #-- Make a series of dates
    start = datetime.datetime(2010,9,15,8,0)
    end = datetime.datetime(2010,9,15,18,0)
    delta = datetime.timedelta(seconds=1)

    # Note: "time" is now an array of floats, where 1.0 corresponds
    # to one day, and 0.0 corresponds to 1900 (I think...)
    # It's _not_ an array of datetime objects!
    time = mpl.dates.drange(start, end, delta)

    num = time.size

    #-- Generate some data
    x = brownian_noise(num)
    y = brownian_noise(num)
    z = brownian_noise(num)

    plot(x, y, z, time)
    plt.show()

def plot(x, y, z, time):
    fig = plt.figure()

    #-- Panel 1
    ax1 = fig.add_subplot(311)
    im, cbar = specgram(x, time, ax1, fig)
    ax1.set_ylabel('X Freq. (Hz)')
    ax1.set_title('Fake Analysis of Something')

    #-- Panel 2
    ax2 = fig.add_subplot(312, sharex=ax1)
    im, cbar = specgram(y, time, ax2, fig)
    ax2.set_ylabel('Y Freq. (Hz)')

    #-- Panel 3
    ax3 = fig.add_subplot(313, sharex=ax1)
    # Plot the 3 source datasets
    xline = ax3.plot_date(time, x, 'r-')
    yline = ax3.plot_date(time, y, 'b-')
    zline = ax3.plot_date(time, z, 'g-')
    ax3.set_ylabel(r'Units $(\mu \phi)$')

    # Make an invisible spacer...
    cax = make_legend_axes(ax3)
    plt.setp(cax, visible=False)

    # Make a legend
    ax3.legend((xline, yline, zline), ('X', 'Y', 'Z'), loc='center left',
            bbox_to_anchor=(1.0, 0.5), frameon=False)

    # Set the labels to be rotated at 20 deg and aligned left to use less space
    plt.setp(ax3.get_xticklabels(), rotation=-20, horizontalalignment='left')

    # Remove space between subplots
    plt.subplots_adjust(hspace=0.0)

def specgram(x, time, ax, fig):
    """Make and plot a log-scaled spectrogram"""
    dt = np.diff(time)[0] # In days...
    fs = dt * (3600 * 24) # Samples per second

    spec_img, freq, _ = mlab.specgram(x, Fs=fs, noverlap=200)
    t = np.linspace(time.min(), time.max(), spec_img.shape[1])

    # Log scaling for amplitude values
    spec_img = np.log10(spec_img)

    # Log scaling for frequency values (y-axis)
    ax.set_yscale('log')

    # Plot amplitudes
    im = ax.pcolormesh(t, freq, spec_img)

    # Add the colorbar in a seperate axis
    cax = make_legend_axes(ax)
    cbar = fig.colorbar(im, cax=cax, format=r'$10^{%0.1f}$')
    cbar.set_label('Amplitude', rotation=-90)

    ax.set_ylim([freq[1], freq.max()])

    # Hide x-axis tick labels
    plt.setp(ax.get_xticklabels(), visible=False)

    return im, cbar

def make_legend_axes(ax):
    divider = make_axes_locatable(ax)
    legend_ax = divider.append_axes('right', 0.4, pad=0.2)
    return legend_ax

def brownian_noise(num):
    x = np.random.random(num) - 0.5
    x = np.cumsum(x)
    return x


if __name__ == '__main__':
    main()
