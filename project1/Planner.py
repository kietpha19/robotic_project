from input import *
from math import *
from collections import deque

class PathPlanner:
    def __init__(self):
        self.grid = [[-2 for _ in range(cols+1)] for _ in range(rows+1)]

        # init obstacle on grid
        for x, y in obstacle:
            j = round(x/u)
            i = rows-round(y/u)
            self.grid[i][j] = -1
        
        # init goal on grid
        gj = round(goal[0]/u)
        gi = round(goal[1]/u)
        self.goal = [gi, gj]
        self.grid[gi][gj] = 0
       
        # init start
        sj = round(start[0]/u)
        si = round(start[1]/u)
        self.start = [si, sj]
        #self.grid[si][sj] = 5 # for debugging

    def print_grid(self):
        for row in self.grid:
            for value in row:   
                print(f"{int(value):4d}", end="")
            print()

    def compute_distant_potential(self):
        directions = [[0,1], [1,0], [0,-1], [-1,0]]
        queue = deque()
        queue.append(self.goal)
        distance = 1

        while queue:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr = r+dr
                    nc = c+dc
                    if 0<=nr<=rows and 0<=nc<=cols and self.grid[nr][nc] == -2:
                        queue.append([nr, nc])
                        self.grid[nr][nc] = distance
            distance +=1

    # note that: cases when going straight are equal, the diagonal is always found first
    def generate_path(self):
        self.compute_distant_potential()
        path = []
        r, c = self.start
        path.append([r,c])

        straight_dir = [[0,1], [0,-1], [-1,0], [1,0]]
        diagonal_dir = [[-1,-1], [-1,1], [1,-1], [1,1]]
        
        while [r,c] != self.goal:
            found_next_step = False
            for dr, dc in diagonal_dir:
                nr = r+dr
                nc = c+dc
                if 0<=nr<=rows and 0<=nc<=cols \
                    and self.grid[nr][nc] == self.grid[r][c] - 2 \
                    and self.grid[r+dr][c] != -1 and self.grid[r][c+dc] !=-1:
                    path.append([nr,nc])
                    r,c = nr, nc
                    found_next_step = True
                    break
            
            # if found next step, skip searching in straight direction part
            if found_next_step:
                continue

            for dr, dc in straight_dir:
                nr = r+dr
                nc = c+dc
                if 0<=nr<=rows and 0<=nc<=cols and self.grid[nr][nc] == self.grid[r][c]-1:
                    path.append([nr,nc])
                    r,c = nr,nc
                    break
        # print(path) for debugging
        return path

'''
# testing 
planner = PathPlanner()
path = planner.generate_path()
planner.print_grid()
# print(planner.start)
# print(planner.goal)
'''