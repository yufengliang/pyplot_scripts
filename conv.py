import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties
import pickle

# show the effects of convolution

overall_path = '../../../examples/tmos/cro2/calc/maxfn_2_k_sigma_0.5'

spec_xas = sp.loadtxt(overall_path + '/spec_xas.dat')
spec0_i = sp.loadtxt(overall_path + '/spec0_i.dat')
spec_g_up = sp.loadtxt(overall_path + '/spec_xas_ispin0.dat')
spec_g_down = sp.loadtxt(overall_path + '/spec_xas_ispin1.dat')

fig, ax = plt.subplots(figsize = (4.25, 3.6))

fac = 100
ax.plot(spec0_i[:, 0], (spec0_i[:, 3] + spec0_i[:, 4]) * fac * 0.93, 
        label = 'initial.',
        color = 'black', linestyle = 'dashdot', linewidth = 2)
ax.plot(spec_xas[:, 0], (spec_xas[:, 3] + spec_xas[:, 4]) * fac * 1.37,
        label = 'conv.', 
        color = 'red', linestyle = 'solid', linewidth = 2)
ax.plot(spec_g_up[:, 0], (spec_g_up[:, 2] + spec_g_down[:, 2]) * 125 * fac, 
        label = 'no conv.', 
        color = 'blue', linestyle = 'dashed', linewidth = 2)

legend = ax.legend(bbox_to_anchor=(0.6, 0.7, 0.15, .3), frameon=False)

ax.set_xticks([528, 531, 534, 537])
ax.set_xlim([526, 538])
ax.set_ylim([0, 1.1])

ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Intensity (a.u.)')
plt.tight_layout()

plt.savefig('conv.png', format = 'png', dpi = 250)
plt.close()

