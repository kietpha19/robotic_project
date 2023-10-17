from input import curr_dir
from Planner import PathPlanner

class Controller:
    def __init__(self):
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

    def get_instruction(self, path, curr_dir):
        instruction = []
        for i in range(len(path)-1):
            r = path[i+1][0] - path[i][0]
            c = path[i+1][1] = path[i][1]
            # excluding the last element (the updated orientation)
            for action in self.control[(curr_dir, (r,c))][:-1]:
                instruction.append(action)
            
            # updating the current orientation of the robot
            curr_dir = self.control[(curr_dir, (r,c))][-1]
        
        return instruction

planner = PathPlanner()
path = planner.generate_path()
print(path)
planner.print_grid()

controller = Controller()
ins = controller.get_instruction(path, curr_dir)
print(ins)





