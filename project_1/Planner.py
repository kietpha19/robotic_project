from input import *
#from math import round
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
        
        move = {
            "right": (0,1),
            "left": (0,-1),
            "up": (-1, 0),
            "down": (1,0),
            "up_right": (-1, 1),
            "up_left": (-1, -1),
            "down_right": (1, 1),
            "down_left": (1, -1),
        }
        # the last element will be the new orientation
        self.control = {
            ("R", move["right"]): ["fw", "R"],
            ("R", move["left"]): ["bw", "R"],
            ("R", move["up"]): ["turn_pos_90", "fw", "U"],
            ("R", move["down"]): ["turn_neg_90", "fw", "D"],
            ("R", move["up_right"]): ["turn_pos_45", "fw_d", "UR"],
            ("R", move["up_left"]): ["turn_neg_45", "bw_d", "DR"],
            ("R", move["down_right"]): ["turn_neg_45", "fw_d", "DR"],
            ("R", move["down_left"]): ["turn_pos_45", "bw_d", "UR"],

            ("L", move["right"]): ["bw", "L"],
            ("L", move["left"]): ["fw", "L"],
            ("L", move["up"]): ["turn_neg_90", "fw", "U"],
            ("L", move["down"]): ["turn_pos_90", "fw", "D"],
            ("L", move["up_right"]): ["turn_pos_45", "bw_d", "DL"],
            ("L", move["up_left"]): ["turn_neg_45", "fw_d", "UL"],
            ("L", move["down_right"]): ["turn_neg_45", "bw_d", "UL"],
            ("L", move["down_left"]): ["turn_pos_45", "fw_d", "DL"],

            ("U", move["right"]): ["turn_neg_90", "fw", "R"],
            ("U", move["left"]): ["turn_pos_90", "fw", "L"],
            ("U", move["up"]): ["fw", "U"],
            ("U", move["down"]): ["bw", "U"],
            ("U", move["up_right"]): ["turn_neg_45", "fw_d", "UR"],
            ("U", move["up_left"]): ["turn_pos_45", "fw_d", "UL"],
            ("U", move["down_right"]): ["turn_pos_45", "bw_d", "UL"],
            ("U", move["down_left"]): ["turn_neg_45", "bw_d", "UR"],

            ("D", move["right"]): ["turn_pos_90", "fw", "R"],
            ("D", move["left"]): ["turn_neg_90", "fw", "L"],
            ("D", move["up"]): ["bw", "D"],
            ("D", move["down"]): ["fw", "D"],
            ("D", move["up_right"]): ["turn_neg_45", "bw_d", "DL"],
            ("D", move["up_left"]): ["turn_pos_45", "bw_d", "DR"],
            ("D", move["down_right"]): ["turn_pos_45", "fw_d", "DR"],
            ("D", move["down_left"]): ["turn_neg_45", "fw_d", "DL"],

            ("UR", move["right"]): ["turn_neg_45", "fw", "R"],
            ("UR", move["left"]): ["turn_neg_45", "bw", "R"],
            ("UR", move["up"]): ["turn_pos_45", "fw", "U"],
            ("UR", move["down"]): ["turn_pos_45", "bw", "U"],
            ("UR", move["up_right"]): ["fw_d", "UR"],
            ("UR", move["up_left"]): ["turn_pos_90", "fw_d", "UL"],
            ("UR", move["down_right"]): ["turn_neg_90", "fw_d", "DR"],
            ("UR", move["down_left"]): ["bw_d", "UR"],

            ("UL", move["right"]): ["turn_pos_45", "bw", "L"],
            ("UL", move["left"]): ["turn_pos_45", "fw", "L"],
            ("UL", move["up"]): ["turn_neg_45", "fw", "U"],
            ("UL", move["down"]): ["turn_neg_45", "bw", "U"],
            ("UL", move["up_right"]): ["turn_neg_90", "fw_d", "UR"],
            ("UL", move["up_left"]): ["fw_d", "UL"],
            ("UL", move["down_right"]): ["bw_d", "UL"],
            ("UL", move["down_left"]): ["turn_pos_90", "fw_d", "DL"],

            ("DR", move["right"]): ["turn_pos_45", "fw", "R"],
            ("DR", move["left"]): ["turn_pos_45", "bw", "R"],
            ("DR", move["up"]): ["turn_neg_45", "bw", "D"],
            ("DR", move["down"]): ["turn_neg_45", "fw", "D"],
            ("DR", move["up_right"]): ["turn_pos_90", "fw_d", "UR"],
            ("DR", move["up_left"]): ["bw_d", "DR"],
            ("DR", move["down_right"]): ["fw_d", "DR"],
            ("DR", move["down_left"]): ["turn_neg_90", "fw_d", "DL"],

            ("DL", move["right"]): ["turn_neg_45", "bw", "L"],
            ("DL", move["left"]): ["turn_neg_45", "fw", "L"],
            ("DL", move["up"]): ["turn_pos_45", "bw", "D"],
            ("DL", move["down"]): ["turn_pos_45", "fw", "D"],
            ("DL", move["up_right"]): ["bw_d", "DL"],
            ("DL", move["up_left"]): ["turn_neg_90", "fw_d", "UL"],
            ("DL", move["down_right"]): ["turn_pos_90", "fw_d", "DR"],
            ("DL", move["down_left"]): ["fw_d", "DL"],
        }

    def print_grid(self):
        for row in self.grid:
            for value in row:
                print("{:4}".format(value), end="")
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
    def generate_path_8d(self):
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

    def generate_path_4d(self):
        self.compute_distant_potential()
        path = []
        r, c = self.start
        path.append([r,c])
        curr_dir = init_orientation

        while [r,c] != self.goal:
            dir = {'R': [0,1], 'L': [0,-1], 'U': [-1,0], 'D': [1,0]}
            nr = r + dir[curr_dir][0]
            nc = c+ dir[curr_dir][1]
            if self.grid[nr][nc] == self.grid[r][c]-1:
                path.append([nr, nc])
                r,c = nr, nc
            else:
                for d in dir.keys():
                    nr = r+dir[d][0]
                    nc = c+dir[d][1]
                    if self.grid[nr][nc] == self.grid[r][c]-1:
                        path.append([nr,nc])
                        curr_dir = d
                        r, c = nr, nc
                        break # break thr for loop
        
        return path

    def compress_instruction(self, instruction):
        if len(instruction) == 0:
            return []
        compressed = []
        ins = instruction[0]
        count = 1

        for i in range(1, len(instruction)):
            if instruction[i] == ins:
                count += 1
            else:
                compressed.append(str(count) + " " + ins)
                ins = instruction[i]
                count = 1

        compressed.append(str(count) + " " + ins)

        return compressed

    def get_instruction(self, d="4d"):
        if d == "8d":
            path = self.generate_path_8d()
        else:
            path = self.generate_path_4d()
            
        curr_dir = init_orientation
        instruction = []
        for i in range(len(path)-1):
            r = path[i+1][0] - path[i][0]
            c = path[i+1][1] - path[i][1]
            # excluding the last element (the updated orientation)
            for action in self.control[(curr_dir, (r,c))][:-1]:
                instruction.append(action)
            
            # updating the current orientation of the robot
            curr_dir = self.control[(curr_dir, (r,c))][-1]
        
        return self.compress_instruction(instruction)


# testing 
# planner = PathPlanner()
# ins = planner.get_instruction()
# planner.print_grid()
# print(ins)
# print(planner.start)
# print(planner.goal)
