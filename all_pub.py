
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties
import pickle


def add_word(ax, px, py, xlim, ylim, word):
    ax.text(xlim[0] * (1 - px) + xlim[1] * px, ylim[0] * (1 - py) + ylim[1] * py, 
            word)

def first_two_maxima(x, y):
    l = []
    for i in range(2, len(y) - 2):
        if y[i] > 0.01 and y[i - 1] <= y[i] > y[i + 1]:
            l.append([x[i], y[i]])
    print(l)
    print(l[0][1] / l[1][1])

def import_and_plot(name, ax):
    """
    paths = ['/path/to/exp.dat', '/path/to/spec0_f.dat', 
             '/path/to/maxfn_1/spec_xas.dat', 
             '/path/to/maxfn_2/spec_xas.dat']

    es: energy shift for the calculated spectra
    """
    spec = []
    mf = info[name]

    ## Read raw data
    for p in mf.path:
        spec.append(np.loadtxt(p))

    ## Scale spectra
    for i in range(1, 4):
        spec[i][:, 0] += mf.es
        spec[i][:, 0] = (spec[i][:, 0] - mf.es0) * mf.dilation + mf.es0
        spec[i][:, 1 : ] *= mf.fac
    spec[1][:, 1 : ] *= mf.fac_f

    ## Plot spectra
    # experiment
    ax.plot(spec[0][:, 0], spec[0][:, 1] * mf.fac_exp + mf.offset_exp,
            label = 'exp',
            color = 'black')
    #first_two_maxima(spec[0][:, 0], spec[0][:, 1] * mf.fac_exp)

    spec0_f = np.zeros(spec[1][:, 1].shape)
    spec_xas_f1 = np.zeros(spec[2][:, 1].shape)
    spec_xas_f2 = np.zeros(spec[3][:, 1].shape)
    for c in mf.cols:
        spec0_f += spec[1][:, c]
        spec_xas_f1 += spec[2][:, c]
        spec_xas_f2 += spec[3][:, c]

    # one-body final-state
    ax.plot(spec[1][:, 0], spec0_f + mf.offset_f, 
            label = 'one-body',
            color = 'blue')
    #first_two_maxima(spec[1][:, 0], spec0_f)
    
    # many-body
    ax.plot(spec[2][:, 0], spec_xas_f1,
            label = '$f^{(1)}$', 
            color = 'orange', linestyle = 'dashed', linewidth = mf.f1lw)
    ax.plot(spec[3][:, 0], spec_xas_f2,
            label = '$f^{(1)} + f^{(2)}$',
            color = 'red')
    first_two_maxima(spec[3][:, 0], spec_xas_f2)

    # old core hole for diamond
    if name == 'diamond':
        ax.plot(spec[4][:, 0], spec[4][:, 1] + 0.6,
                color = 'green')
        add_word(ax, 0.4, 0.5, mf.xlim, mf.ylim, 'prev. calc.')

    ## format
    # limits
    ax.set_xlim(mf.xlim)
    ax.set_ylim(mf.ylim)

    # ticks
    dx = 5.0
    xticks = np.arange(mf.xlim[0] - mf.xlim[0] % dx + dx, mf.xlim[1], dx)
    ax.set_xticks(xticks)

    dy = 0.5
    yticks = np.arange(mf.ylim[0] - mf.ylim[0] % dy + dy, mf.ylim[1], dy)
    ax.set_yticks(yticks)

    # text
    word = '$\mathregular{' + pnames[name] + '}$'
    add_word(ax, 0.8, 0.9, mf.xlim, mf.ylim, word)


names = ['tio2', 'srtio3', 'fe2o3', 'vo2', 'cro2', 'mno2', 'nio', 'cuo', 'diamond']
pnames = {'tio2' : 'TiO_2', 'srtio3' : 'SrTiO_3', 'fe2o3' : 'Fe_2O_3', 'vo2' : 'VO_2', 
          'cro2' : 'CrO_2',  'mno2' : 'MnO_2', 'nio' : 'NiO', 'cuo' : 'CuO', 
          'diamond' : 'diamond'}
overall_path = '../../examples'
info = {}

figs, axes = plt.subplots(3, 3, figsize = (13, 9))

class info_type:
    pass

ind = 0
for n in names:
    info[n] = info_type()
    # paths
    path = overall_path + '/'
    if n == 'diamond': path += 'carbon'
    else: path += 'tmos'
    path += '/' + n
    # initialization
    info[n].path = []
    info[n].fac_f = 1.0
    info[n].fac_exp = 1.0
    info[n].xlim = [526.0, 549.0]
    info[n].ylim = [-0.02, 1.65]
    info[n].dilation = 1.0
    info[n].es0 = 0.0
    info[n].f1lw = 1.5
    print('working with ' + n + ': ' + path)
    i = 0
    with open(path + '/test.py') as f:
        for l in f:
            l = l.split('#')[0]
            if '=' in l and 'loadtxt' in l:
                spec_file = l.split("'")[1]
                print('file {}: {}'.format(i, spec_file))
                info[n].path.append(path + '/' + spec_file)
                i += 1
            if 'es = ' in l:
                info[n].es = float(l.split('=')[1])
            if 'fac = ' in l:
                info[n].fac = float(l.split('=')[1])
            if 'spec0_f' in l and '*= fac' in l:
                if l.split()[-1] != 'fac':
                    info[n].fac_f = float(l.split()[-1])
            if 'ax.plot' in l and 'spec_exp' in l:
                info[n].offset_exp = float(l.split('+')[-1].split(',')[0])
                
            if 'ax.plot' in l and 'spec0_f' in l:
                info[n].offset_f = float(l.split('+')[-1].split(',')[0])
    info[n].cols = [1, 2]
    ind += 1

# special cases
info['diamond'].cols = [1]
info['diamond'].fac_exp = 5.0
info['diamond'].xlim = [0.0, 25.0]
info['diamond'].ylim[1] = 2.0
info['diamond'].f1lw = 3.0
info['diamond'].fac = 20
info['cro2'].cols = [3, 4]
info['nio'].xlim = [0.0, 20.0]
info['srtio3'].es0 = 531.5
info['srtio3'].dilation = 1.08

# save information if needed
with open('plot_info.pkl', 'wb') as output:
    pickle.dump(info, output, pickle.HIGHEST_PROTOCOL)

# load information
with open('plot_info.pkl', 'rb') as inp:
    info = pickle.load(inp)

# print(info['tio2'])

# Now we plot the whole figure
ind = int(0)
for n in names:
    ax = axes[int(ind / 3), int(ind % 3)]
    import_and_plot(name = n,
                    ax = ax)
    # xlabels
    if ind > 5: ax.set_xlabel('Energy (eV)')
    # ylabels
    if ind % 3 == 0: ax.set_ylabel('Intensity (a.u.)')
    if ind == 4:
        legend = ax.legend(bbox_to_anchor=(0.45, 0.60, 0.15, .3), frameon=False)
    ind += 1

# format
plt.tight_layout()

#plt.show()
plt.savefig('all_pub.png', format = 'png')
plt.savefig('all_pub.eps', format = 'eps')
plt.close()
