###### environment configuration #####################################
width = 3.05 # y-axis
length = 4.88 # x-axis
rows = 10 # number of floor tiles in the workspace's width (y-axis)
cols = 16 # number of floor tiles in the workspace's length (x-axis)
u = 0.305 # size of 1 floor tile

start = [u, 5*u]  # start location
goal = [9*u, 5*u]   # goal location

obstacle = [ 
    [1*u, 1*u], [2*u, 1*u], [1*u, 2*u], [2*u, 2*u],
    [8*u, 2*u], [9*u, 2*u], [10*u, 2*u],
    [2*u, 7*u], [2*u, 8*u],
    [5*u, 4*u], [5*u, 5*u], [5*u, 6*u],
    [8*u, 8*u]
]
#####################################################################

####### robot configuration #########################################
init_orientation = 'R' # current orientation of the robot

