import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties
import pickle

overall_path = '../../../examples/tmos/cro2/calc'
xps_file = overall_path + '/maxfn_2_k_sigma_0.5/spec_xps.dat'
stick_file = overall_path + '/maxfn_2_k_sigma_0.5/xps_sticks.dat'
# load data
xps = sp.loadtxt(xps_file)
sticks = sp.loadtxt(stick_file)
s = sticks[:, -2 : ]
fac = 3
s[:, 1] = s[:, 1] * s[:, 1] * fac

fig, ax = plt.subplots(figsize = (4.4, 3.6))

ax.plot(-xps[:, 0], xps[:, 1])
ax.stem(-s[:, 0], s[:, 1], markerfmt = ' ', basefmt = ' ')

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

find_max(-s[:, 0], s[:, 1], -0.2, 0.1, ax, sticks[:, : -2])
find_max(-s[:, 0], s[:, 1], -5.0, -1.5, ax, sticks[:, : -2])
find_max(-s[:, 0], s[:, 1], -9, -6, ax, sticks[:, : -2])

ax.set_xlim([-20, 2.0])
ax.set_ylim([0, 0.6])
#plt.show()
plt.savefig('xps.png', format = 'png', dpi = 250)
plt.close()

