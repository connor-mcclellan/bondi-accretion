from athena_read import athdf
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np

simulation_data = []
for i, bsq in enumerate([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]):
    simulation_data.append(athdf("../data/ba-bsq{:1d}/gr_bondi.out1.00001.athdf".format(bsq)))

gamma = 1.333333333333333
c_light = 3e10
n = 1 / (gamma - 1)

vel_nomag = simulation_data[0]['vel1'][0,0]

bsq_values = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
colors = pl.cm.viridis(np.linspace(0, 1, len(bsq_values)))

fig = plt.figure()
sm = plt.cm.ScalarMappable(cmap=pl.cm.viridis, norm=plt.Normalize(vmin=0,vmax=50))
cbar = fig.colorbar(sm)
cbar.ax.set_ylabel(r'magnetic field strength ($B^2/\rho$)', rotation=90)

for i, bsq in enumerate(bsq_values):
    rho = simulation_data[i]['rho'][0,0]
    ur = simulation_data[i]['vel1'][0,0]
    press = simulation_data[i]['press'][0][0]
    r = simulation_data[i]['x1v']

    Tn = (press / rho)**n
    c1 = -0.00675
    u1 = c1 / r**2 / Tn
    y = np.sqrt(1 - 2/r + u1**2)
    local_vel = u1/y
    if i==0:
        vel_nomag = local_vel
    plt.plot(r, local_vel/vel_nomag, marker='o', ms=2, c=colors[i])
    plt.text(r[0]-0.35, local_vel[0]/vel_nomag[0]-0.0005, "{:.3f}c".format(-local_vel[0]), color=colors[i], size=7)

plt.xlabel('gravitational radius [r / (2GM/c2)]')
plt.xlim((2.6, 10))
plt.ylabel('infall velocity / non-magnetized infall velocity')
plt.xscale('log')
#plt.yscale('log')
plt.show()
