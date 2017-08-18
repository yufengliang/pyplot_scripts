import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties
import pickle

overall_path = '../../../examples/tmos/fe2o3/'
spec_xas = sp.loadtxt(overall_path + '/calc/maxfn_2_k/spec_xas.dat')
spec_exp = sp.loadtxt(overall_path + 'exp/fe2o3.dat')
spec_bse = sp.loadtxt('fe2o3.bse_u0_b0.3eV_das.dat')

fig, ax = plt.subplots(figsize = (6, 3))

fac = 100
ax.plot(spec_exp[:, 0] + 0.0, spec_exp[:, 1])
ax.plot(spec_xas[:, 0] - 0.8, (spec_xas[:, 1] + spec_xas[:, 2]) * fac * 1.03)
ax.plot(spec_bse[:, 0] + 529.0, (spec_bse[:, 1] + spec_bse[:, 9] + spec_bse[:, 17]) * fac * 2.7)
ax.set_xlim([526, 549])

plt.tight_layout()

plt.savefig('mbxas_vs_bse.png', format = 'png', dpi = 250)
plt.close()


