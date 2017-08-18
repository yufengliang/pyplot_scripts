
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties
import pickle

overall_path = '../../../examples/tmos/cro2/calc'

fn = [1, 2]
class info_type: pass
info = {}
for n in fn: info[n] = info_type()
info[1].path = 'maxfn_1_k_sigma_0.5'
info[2].path = 'maxfn_2_k_sigma_0.5'
# below are actually the xps peak height / no, i just tune it to match the calculated spectra
# they are extracted from xps stick statistics
info[1].stick0_fac = sp.sqrt(0.718)
info[1].stick1_fac = sp.sqrt(0.115)
info[2].stick0_fac = sp.sqrt(0.718)
#info[2].stick1_fac = sp.sqrt(0.554)
info[2].stick1_fac = 1.0# split them up later

# initialize figs
figs, axes = plt.subplots(len(fn), 1, figsize = (4, len(fn) * 3))


# find the maximum with a certain energy range and outline the stick
def find_max(ener, sticks, elo, ehi, ax, info, sign = 1.0):
    maxi, emax, smax = None, None, -1
    for ii, (e, s) in enumerate(zip(ener, sticks)):
        if elo <= e < ehi:
            if s > smax: maxi, emax, smax = ii, e, s
    if emax is not None:
        sinfo = ''
        for ind in info[maxi]: sinfo += str(int(ind + 1)) + ' '
        print('[{}, {}]: ({}) energy = {:12.5}, stick = {:12.5}'.format(elo, ehi, sinfo, emax, smax))
        markerline, stemlines, baseline = ax.stem([emax], [smax * sign], linefmt='black', markerfmt = ' ', basefmt = ' ')
        plt.setp(stemlines, 'linewidth', 3)
        
spec_xas_last = None

for i, n in enumerate(fn):

    # load data
    path = overall_path + '/' + info[n].path

    spec_xas = sp.loadtxt(path + '/spec_xas.dat')
    spec_xas[:, 1 : ] *= 10 ** 3

    sticks0 = sp.loadtxt(path + '/sticks_ispin0.dat')
    s0 = sticks0[:, -2 : ]
    sticks1 = sp.loadtxt(path + '/sticks_ispin1.dat')
    s1 = sticks1[:, -2 : ]
    if i == 0: 
        s1_manual = sp.array(s1)
        sticks1_manual = sp.array(sticks1)

    # find the difference spectrum
    dspec = spec_xas
    if spec_xas_last is not None:
        dspec[:, 1 : ] -= spec_xas_last[:, 1 : ]
    spec_xas_last = spec_xas

    # plot it
    ax = axes[i]
    
    x0, x1 = 526, 549
    ax.plot(dspec[:, 0], dspec[:, 3])
    ax.plot(dspec[:, 0], -dspec[:, 4])
    ax.plot([x0, x1], [0, 0], color = 'black', linewidth = 1)

    # alignment for the sticks
    eshift = 517.976 + 10.6860
    global_emin = 10.6860
    spin0_emin = 10.6860
    spin1_emin = 13.2878
    es0 = eshift + (spin0_emin - global_emin)
    es1 = eshift + (spin1_emin - global_emin)

    fac = 5 * 10 ** 4
    # spin up
    s0[:, 0] += es0
    s0[:, 1] = s0[:, 1] * s0[:, 1] * fac * info[n].stick0_fac
    ax.stem(s0[:, 0], s0[:, 1],
            markerfmt = ' ',
            basefmt = ' ')

    # label major sticks
    print('f({}), spin {}'.format(n, 0))
    if i == 0:
        find_max(s0[:, 0], s0[:, 1], 527, 530, ax, sticks0[:, : -2])
        find_max(s0[:, 0], s0[:, 1], 530, 535, ax, sticks0[:, : -2])
        find_max(s0[:, 0], s0[:, 1], 540, 548, ax, sticks0[:, : -2])
    if i == 1:
        find_max(s0[:, 0], s0[:, 1], 527, 530, ax, sticks0[:, : -2])
        find_max(s0[:, 0], s0[:, 1], 530, 535, ax, sticks0[:, : -2])
        find_max(s0[:, 0], s0[:, 1], 540, 548, ax, sticks0[:, : -2])
        

    # spin down
    if i == 1:
        # manually convoluted with xps
        s1 = sp.array(s1_manual) # because xas^{(2)}_{spin_down} is ~ 0, so the contribution is actually from xps^{(1)}_{spin_up} 
        toy_xps = {0.327 : 0.259, 2.300 : 0.109, 2.333 : 0.102, 
                   0.361 : 0.245, 0.193 : 0.224, 0.184 : 0.200,
                   0.353 : 0.207, 0.160 : 0.235} # extracted from spin0 xps sticks of maxfn = 2 mbxaspy.out
        #toy_xps = {0 : sp.sqrt(0.544)}
        #toy_xps = {0.33 : 0.24}
        #toy_xps = {2.300 : 0.109, 0.327 : 0.259}
        for j, t in enumerate(toy_xps):
            if j == 0: 
                s1[:, 0] += t
                s1[:, 1 : ] *= toy_xps[t]
            else:
                st = sp.array(s1_manual)
                st[:, 0] += t
                st[:, 1 : ] *= toy_xps[t]
                s1 = sp.vstack((s1, st))
        sticks1 = sp.array(sticks1_manual)
            
    s1[:, 0] += es1
    s1[:, 1] = s1[:, 1] * s1[:, 1] * fac * info[n].stick1_fac
    ax.stem(s1[:, 0], -s1[:, 1],
            linefmt='C1',
            markerfmt = ' ',
            basefmt = ' ')

    # label major sticks
    print('f({}), spin {}'.format(n, 1))
    if i == 0:
        find_max(s1[:, 0], s1[:, 1], 527, 530, ax, sticks1[:, : -2], -1)
        find_max(s1[:, 0], s1[:, 1], 530, 535, ax, sticks1[:, : -2], -1)
        #find_max(s1[:, 0], s1[:, 1], 540, 548, ax, sticks1[:, : -2], -1)
    if i == 1:
        find_max(s1[:, 0], s1[:, 1], 527, 530, ax, sticks1[:, : -2], -1)
        find_max(s1[:, 0], s1[:, 1], 530, 535, ax, sticks1[:, : -2], -1)
        #find_max(s1[:, 0], s1[:, 1], 540, 548, ax, sticks1[:, : -2], -1)

    # format
    ax.set_xlim([x0, x1])
    ax.set_ylabel('Intensity (a.u.)')
    if i < len(fn) - 1:
        ax.set_xticklabels([])

axes[1].set_yticks([-1, 0, 1])
axes[1].set_ylim([-1.4, 1.8])
axes[1].set_xlabel('Energy (eV)')

#figs.text(0.03, 0.65, 'Intensity (a.u.)', rotation = 'vertical')

figs.tight_layout()
#plt.show()
plt.savefig('f1f2.png', format = 'png', dpi = 250)
plt.close()
    

    



