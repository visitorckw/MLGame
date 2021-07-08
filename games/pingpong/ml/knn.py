"""
The template of the main script of the machine learning process
"""
import random
import os.path
import pickle

# his = []

class MLPlay:
    def __init__(self, side):
        """
        Constructor
        """
        self.side = side
        filename = 'model_1P.pickle' if self.side == '1P' else 'model_2P.pickle'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.ball_served = False
        self.his = []

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"
        if (scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS"):
            return "RESET"
        if not self.ball_served:
            if not len(self.his):
                self.his.append(scene_info)
                return 'NONE'
            if scene_info['ball'][1] == 415 and (scene_info['blocker'][0] != 160 or (scene_info['blocker'][0] > self.his[-1]['blocker'][0])):
                self.his.append(scene_info)
                return 'NONE'
            if scene_info['ball'][1] == 80 and (scene_info['blocker'][0] != 140 or (scene_info['blocker'][0] < self.his[-1]['blocker'][0])):
                self.his.append(scene_info)
                return 'NONE'
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            his = self.his
            his.append(scene_info)
            if len(his) <= 1:
                return 'NONE'
            nx = scene_info["ball"][0]
            ny = scene_info["ball"][1]
            px = scene_info["platform_1P"][0] if self.side == '1P' else scene_info["platform_2P"][0]
            vx = his[-1]["ball"][0] - his[-2]['ball'][0]
            vy = his[-1]['ball'][1] - his[-1]['ball'][1]
            blockerX = scene_info['blocker'][0]
            Vblocker =  scene_info['blocker'][0] - his[-1]['blocker'][0]
            speed = scene_info['ball_speed']
            command = self.model.predict([[nx, ny, px, vx, vy, scene_info['frame'], blockerX, Vblocker, speed[0], speed[1] ]])

        if command == 0: return "NONE"
        elif command == 1: return "MOVE_LEFT"
        else: return "MOVE_RIGHT"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
