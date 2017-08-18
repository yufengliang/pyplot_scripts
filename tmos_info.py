import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties
import matplotlib.cm as cm
import pickle

info = []

with open('tmos_info.txt', 'r') as f:
    for l in f:
        e = l.split()
        info.append([e[0]] + [float(_) for _ in e[1 :]])

print(info)

pnames = {'tio2' : 'TiO_2', 'srtio3' : 'SrTiO_3', 'fe2o3' : 'Fe_2O_3', 'vo2' : 'VO_2', 
          'cro2' : 'CrO_2',  'mno2' : 'MnO_2', 'nio' : 'NiO', 'cuo' : 'CuO', 
          'diamond' : 'diamond'}

fig, ax = plt.subplots(figsize = (4, 4))

equal = True
if equal:
    ax.plot([0.0, 3.0], [0.0, 3.0], color = 'black', linewidth = 1, zorder = -1)

x = range(len(info))
x =  [i[1] for i in info]
if equal:
    x = [i[3] for i in info]

colors = cm.rainbow(np.linspace(0, 1, len(info)))
if not equal:
    ax.scatter(x, [i[3] for i in info])
alpha = 0.5
size = 8 ** 2
ax.scatter(x, [i[4] for i in info],
           label = ' one-body', 
           marker = 'o', alpha = alpha, color = colors, s = size)
ax.scatter(x, [i[5] for i in info],
           label = 'many-body',
           marker = '^', alpha = alpha, color = colors, s = size)

if equal:
    for i in info:
        x0, y0 = i[3] - 0.15, i[5] + 0.1
        if i[0] == 'srtio3':
            x0 += 0.1; y0 += -0.25
        if i[0] == 'tio2':
            x0 += 0.2; y0 += -0.15
        ax.text(x0, y0, '$\mathregular{' + pnames[i[0]] + '}$')
    ax.set_xlabel('Exp. Ratio')
    ax.set_ylabel('Calc. Ratio')
    ax.set_xlim([0, 2.2])
    ax.set_ylim([0, 2.2])
    ax.set_aspect('equal')
    legend = ax.legend(bbox_to_anchor=(0.25, 0.75, 0.2, .2), frameon=False)
    
# format
plt.tight_layout()

#plt.show()
plt.savefig('tmos_info.png', format = 'png', dpi = 1000)
plt.savefig('tmos_info.eps', format = 'eps')
plt.close()
