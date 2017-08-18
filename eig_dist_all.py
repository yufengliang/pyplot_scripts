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


name = ['fe2o3', 'cro2']

class info_type:
    pass

info = {}
for n in name:
    info[n] = info_type()

info['fe2o3'].f = 'fe2o3/calc/maxfn_1_k/xi_eig_spin_0.dat'
info['cro2'].f = 'cro2/calc/mbxaspy_ana/xi_eig_spin_0.dat'
info['fe2o3'].pname = 'Fe_2O_3 (1000)'
info['cro2'].pname = 'CrO_2 (1200)'

path = '../../examples/tmos'
for n in name:
    info[n].f = path + '/' + info[n].f

fig = plt.figure(1, figsize=(4.8,3.4))
# initialize grid spec
gs = gridspec.GridSpec(len(name), 2, width_ratios = [1, 3]) # gs is a linear array, not 2d

#fig, axes = plt.subplots(nrows = len(name), ncols = 2, sharex = True, sharey = True, 
#                  gridspec_kw = {'width_ratios': [1, 3]}, figsize = (6, 3))

# plotting parameters
ymin, ymax = 0.5, 1200
ec = 'black'
alpha = 0.8
facecolor = 'blue'

for i, n in enumerate(name):
    eigs = sp.loadtxt(info[n].f)
    ax = [plt.subplot(gs[2 * i + j]) for j in range(2)]
    #ax = axes[i]

    ax[0].hist(eigs, 15,
            range = [0.6, 0.99],
            histtype='bar',
            ec = ec,
            alpha = alpha,
            facecolor = facecolor,
            linestyle=('solid'))

    ax[1].hist(eigs, 15,
            range = [0.99, 1.0],
            histtype='bar',
            ec = ec,
            alpha = alpha,
            facecolor = facecolor,
            linestyle=('solid'))

    # formatting
    for j in range(2):
        ax[j].set_yscale("log")
        ax[j].set_ylim([ymin, ymax])
        ax[j].set_yticks([1, 10, 100, 1000])

    ax[0].set_xlim([0.6, 0.99])
    ax[1].set_xlim([0.9901, 1.0])
    ax[1].yaxis.set_ticks_position("right")

    ax[0].set_xticks([0.79, 0.99])
    ax[1].set_xticks([0.992, 0.996, 1.00])
    
    if i < len(name) - 1:
        for j in range(2): kill_ticklabels(ax[j])

    # text
    word = '$\mathregular{' + info[n].pname + '}$'
    add_word(ax[1], 0.4, 0.1, word)

fig.text(0.45, 0.0, 'Eigenvalues')
fig.text(0.0, 0.7, 'Count of Eigenvalues', rotation = 'vertical')
#fig.xlabel('Eigenvalues')
#fig.ylabel('Count of Eigenvalues')
fig.tight_layout()

plt.savefig('eig_dist.png', format = 'png', bbox_inches='tight', dpi = 600)
plt.savefig('eig_dist.eps', format = 'eps', bbox_inches='tight')

#plt.show()
plt.close()
    
