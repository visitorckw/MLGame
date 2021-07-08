"""
The template of the main script of the machine learning process
"""
import random
import os.path
import pickle

his = []
def feature():
    if len(his) <= 1:
        return 100
    vx = his[-1]['ball'][0] - his[-2]['ball'][0]
    vy = his[-1]['ball'][1] - his[-2]['ball'][1]
    if vy <= 0:
        return 100
    t = (400 - his[-1]['ball'][1]) / vy
    px = his[-1]['ball'][0] + vx * t
    while 0 > px or px > 200:
        if 0 > px:
            px = -px
        else:
            px = 400 - px
    return px

def low(b1, b2):
    ans = -1
    for b in b1:
        if b[1] > ans:
            ans = b[1]
    for b in b2:
        if b[1] > ans:
            ans = b[1]
    return ans

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        filename = 'arkanoid_n3_20210309_knn_model.pickle'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.ball_served = False

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"
            return command
        else:
            global his
            his.append(scene_info)
            if len(his) <= 1:
                return 'NONE'
            nx = scene_info["ball"][0]
            ny = scene_info["ball"][1]
            px = scene_info["platform"][0]
            vx = his[-1]["ball"][0] - his[-2]['ball'][0]
            vy = his[-1]['ball'][1] - his[-1]['ball'][1]
            f = feature()
            lowest = low(scene_info['bricks'], scene_info['hard_bricks'])
            command = self.model.predict([[nx, ny, px, vx, vy, f, scene_info['frame'], lowest ]])

        if command == 0: return "NONE"
        elif command == 1: return "MOVE_LEFT"
        else: return "MOVE_RIGHT"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
