import matplotlib.pyplot as plt

mag_field_strength = [0, 5, 10, 15]
infall_velocities = [.701, .697, .693, .689]

plt.plot(mag_field_strength, infall_velocities, marker='o', c='c')
plt.xlabel('magnetic field strength (bsq/rho)')
plt.ylabel('infall velocity at Schwarzchild radius')
plt.show()
