from athena_read import athdf
import numpy as np

# A list of all the values of bsq/rho we want to use
bsq_values = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

# Load in the first data set so we can get the dimensions of the r and v arrays
sample_data = athdf("../data/ba-bsq0/gr_bondi.out1.00001.athdf")
r_array_size = len(sample_data['x1v'])

# Initialize an empty array with the right dimensions to store our data
# (number of bsq values x number of r data points)
data = np.zeros((len(bsq_values), r_array_size))

gamma = 1.333333333333333
c_light = 3e10
n = 1 / (gamma - 1)


def get_local_velocity(r, press, rho):
    '''Returns the velocity of the gas in the lab frame, given the radius, pressure and density. Can be used for either a single value or an array of values.'''
    Tn = (press / rho)**n
    c1 = -0.00675
    u1 = c1 / r**2 / Tn
    y = np.sqrt(1 - 2/r + u1**2)
    local_vel = u1/y
    return -local_vel


# Loop over every value of magnetic field strength
for i, bsq in enumerate(bsq_values):

    # Load the relevant file for this value of bsq
    simdata = athdf("../data/ba-bsq{:1d}/gr_bondi.out1.00001.athdf".format(bsq))

    # Get the density, pressure, and radius from the file
    rho = simdata['rho'][0][0]
    press = simdata['press'][0][0]
    r = simdata['x1v']

    # Use our function defined above to calculate velocities at each radius
    v = get_local_velocity(r, press, rho)

    # Put the velocity as a function of radius for this value of bsq into our 2d array
    data[i, :] = v

# After going through the loop above, our data array will be filled with values
# Now we can export it to a .csv file

np.savetxt("infall_velocities.csv", data.T, delimiter=',')
np.savetxt("radii.csv", r, delimiter=',')
np.savetxt("bsq.csv", np.array(bsq_values).T, delimiter=',')
