###### environment configuration #####################################
width = 3.05 # y-axis
length = 4.88 # x-axis
rows = 10 # number of floor tiles in the workspace's width (y-axis)
cols = 16 # number of floor tiles in the workspace's length (x-axis)
u = 0.305 # size of 1 floor tile

start = [u, 8*u]  # start location
goal = [12*u, 3*u]   # goal location

obstacle = [ 
    [3*u, 1*u], [3*u, 2*u], [3*u, 3*u], [3*u, 4*u],[3*u, 5*u], [3*u, 6*u],
    [6*u, 3*u], [6*u, 4*u], [6*u, 5*u], [6*u, 6*u], [6*u, 7*u], [6*u, 8*u],[6*u, 9*u], [6*u, 10*u],
    [9*u, 3*u], [9*u, 4*u], [9*u, 5*u], [9*u, 6*u],[9*u, 7*u], 
    [10*u, 3*u],
    [11*u, 3*u], [11*u, 4*u], [12*u, 3*u], [12*u, 4*u],
    [1*u,0], [2*u,0], [3*u,0], [4*u,0], [5*u,0], [6*u,0], [7*u,0], [8*u,0], [9*u,0], [10*u,0], [11*u,0], [12*u,0]
    
]
#####################################################################

####### robot configuration #########################################
init_orientation = 'U' # current orientation of the robot

