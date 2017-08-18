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

info['tio2'].f = 'tio2/calc/mbxaspy_ana/xi.npy'
info['cro2'].f = 'cro2/calc/mbxaspy_ana/xi0.npy'
info['tio2'].pname = 'TiO_2'
info['cro2'].pname = 'CrO_2'
info['tio2'].ef = 288
info['tio2'].r = 40
info['cro2'].ef = 336
info['cro2'].r = 40
info['tio2'].d = 200
info['cro2'].d = 300
info['tio2'].d1 = 20
info['cro2'].d1 = 20


path = '../../examples/tmos'
for n in name:
    info[n].f = path + '/' + info[n].f

# subplots
figs, axes = plt.subplots(len(name), 2, figsize=(8.8,8))

cmap = 'Oranges'

for i, n in enumerate(name):

    xi = sp.load(info[n].f)
    xi_max = abs(xi).max()
    xi_max = 1
    ef, r = info[n].ef, info[n].r
    
    ax = axes[i]

    for j in range(2):
        pcm = ax[j].imshow(abs(xi), cmap = cmap, interpolation='none',
            norm = colors.LogNorm(vmax = xi_max, vmin = xi_max * 10 ** (-4)))

    # formatting
    setticks(ax[0], 0, info[n].d, axis = 'x', all_int = True)
    setticks(ax[0], 0, info[n].d, axis = 'y', all_int = True)
    my_ls = {'linewidth' : 1, 'color' : 'black', 'ls' : '--'}
    lh = mlines.Line2D([0, xi.shape[1]], [ef,ef], ** my_ls)
    ll = mlines.Line2D([ef, ef], [0, xi.shape[0]], ** my_ls)
    ax[0].add_line(lh)
    ax[0].add_line(ll)

    ax[0].set_aspect('equal')
    ax[0].set_xlim([0, xi.shape[1]])
    ax[0].set_ylim([0, xi.shape[0]])

    # text
    word = '$\mathregular{' + info[n].pname + '}$'
    add_word(ax[0], 0.1, 0.8, word, fontsize = 18)

    ax[0].add_patch(
        patches.Rectangle(
        (ef - r, ef - r),
        2 * r,
        2 * r,
        linewidth = 2,
        fill=False      # remove background
        )
    )

    setticks(ax[1], 0, info[n].d1, axis = 'x', all_int = True)
    setticks(ax[1], 0, info[n].d1, axis = 'y', all_int = True)

    my_ls = {'linewidth' : 3, 'color' : 'black', 'ls' : '--'}    
    lh = mlines.Line2D([0, xi.shape[1]], [ef,ef], ** my_ls)
    ll = mlines.Line2D([ef, ef], [0, xi.shape[0]], ** my_ls)
    ax[1].add_line(lh)
    ax[1].add_line(ll)

    ax[1].set_aspect('equal')
    ax[1].set_xlim([ef - r, ef + r])
    ax[1].set_ylim([ef - r, ef + r])


figs.subplots_adjust(wspace = 0.1, hspace = 0.1, right = 0.85)
cbar_ax = figs.add_axes([0.88, 0.11, 0.02, 0.75])
figs.colorbar(pcm, cax=cbar_ax)

plt.savefig('xi.png', format = 'png', bbox_inches='tight', dpi = 100)
# plt.savefig('xi.eps', format = 'eps', bbox_inches='tight') #

#plt.show()
plt.close()

    


