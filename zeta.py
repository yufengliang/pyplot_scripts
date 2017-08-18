import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import gca
import matplotlib.colors as colors
from matplotlib import gridspec
from matplotlib.font_manager import FontProperties
import pickle
from utils import *
import matplotlib.patches as patches
import matplotlib.lines as mlines

name = ['tio2', 'cro2']

class info_type:
    pass

info = {}
for n in name:
    info[n] = info_type()

info['tio2'].f = 'tio2/calc/mbxaspy_ana/zeta_x.npy'
info['cro2'].f = 'cro2/calc/mbxaspy_ana/zeta_x_spin0.npy'
info['tio2'].pname = 'TiO_2'
info['cro2'].pname = 'CrO_2'

path = '../../examples/tmos'
for n in name:
    info[n].f = path + '/' + info[n].f

fig = plt.figure(1, figsize=(7, 7))
ns = len(name)
gs = gridspec.GridSpec(ns, ns + 1, width_ratios = [0.4] * ns + [1])
gs.update(wspace = 0.05, hspace = 0.1, right = 0.85)


cmap = 'seismic'
cmap = 'coolwarm'
cmap = 'Blues'
for i, n in enumerate(name):

    # load data
    zeta = sp.load(info[n].f)
    zeta_max = abs(zeta).max()
    
    # layout
    ax = plt.subplot(gs[:, i]), plt.subplot(gs[i, ns])

    for j in range(2):
        pcm = ax[j].imshow(
                            abs(zeta),
                            norm = colors.LogNorm(vmax = zeta_max, vmin = zeta_max * 10 ** (-4)),
                            alpha = 1.0, 
                            cmap = cmap, interpolation='none', aspect = None 
                          )

    r = 20
    setticks(ax[0], zeta.shape[1] - r, r - 1, axis = 'x', offset = 1, all_int = True)
    setticks(ax[0], 0, 40, axis = 'y', offset = 1, all_int = True)
    ax[0].set_xlim([zeta.shape[1] - r - 0.5, zeta.shape[1] - 0.5])
    ax[0].set_ylim([150 - 0.5, 0 - 0.5])

    # text
    word = '$\mathregular{' + info[n].pname + '}$'
    add_word(ax[0], 0.2, 0.62, word, fontsize = 16)

    r = 12
    ax[0].add_patch(
        patches.Rectangle(
        (zeta.shape[1] - r - 0.5, -0.5),
        r,
        r,
        linewidth = 2,
        fill=False      # remove background
        )
    )

    d = 4
    setticks(ax[1], zeta.shape[1] - 1 - r / d * d, d, axis = 'x', offset = 1, all_int = True)
    setticks(ax[1], 0, d, axis = 'y', offset = 1, all_int = True)

    ax[1].set_xlim([zeta.shape[1] - r - 0.5, zeta.shape[1] - 0.5])
    ax[1].set_ylim([r - 0.5, 0 - 0.5])

    # text
    word = '$\mathregular{' + info[n].pname + '}$'
    add_word(ax[1], 0.4, 0.6, word, fontsize = 16)

cbar_ax = fig.add_axes([0.88, 0.11, 0.03, 0.76])
fig.colorbar(pcm, cax=cbar_ax)

#plt.tight_layout() # not compatible with gridspec udpate
#plt.show()

plt.savefig('zeta.png', format = 'png', bbox_inches='tight', dpi = 100)
plt.close()

