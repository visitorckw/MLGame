"""
The template of the main script of the machine learning process
"""

import random
px = 0
py = 0
flag = False
ver = -100
history = {}
report = False

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        global px
        global py
        global flag
        global ver
        px = 0
        py = 0
        flag = False
        ver = -100

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        global px
        global py
        global flag
        global ver
        global history
        global report

        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            # if random.random() < 0.01:
            #     self.ball_served = True
            #     return "SERVE_TO_LEFT"
            # if random.random() < 0.5:
            #     return 'MOVE_LEFT'
            # return 'MOVE_RIGHT'
            self.ball_served = True
            return "SERVE_TO_LEFT"

        if not report:
            history = scene_info
            report = True
            return 'NONE'
        vx = scene_info['ball'][0] - history['ball'][0]
        vy = scene_info['ball'][1] - history['ball'][1]
        history = scene_info
        if vy < 0: # moving up
            hit = False
            hitY = 0
            for b in scene_info['bricks']: # 撞磚底判斷
                if b[1] + 10 > scene_info['ball'][1]:
                    continue
                t = (b[1] + 10 - scene_info['ball'][1]) / vy
                px = scene_info['ball'][0] + vx * t
                while 0 > px or px > 200:
                    if 0 > px:
                        px = -px
                    else:
                        px = 400 - px
                if b[0] <= px and px <= b[0] + 25:
                    hit = True
                    hitY = max(hitY, b[1] + 10)
            for b in scene_info['hard_bricks']: # 撞磚底判斷
                if b[1] + 10 > scene_info['ball'][1]:
                    continue
                t = (b[1] + 10 - scene_info['ball'][1]) / vy
                px = scene_info['ball'][0] + vx * t
                while 0 > px or px > 200:
                    if 0 > px:
                        px = -px
                    else:
                        px = 400 - px
                if b[0] <= px and px <= b[0] + 25:
                    hit = True
                    hitY = max(hitY, b[1] + 10)
            if hit:
                t = ((scene_info['ball'][1] - hitY) + (400 - hitY)) / vy
                t = -t
                predict = scene_info['ball'][0] + vx * t
                while 0 > predict or predict > 200:
                    if 0 > predict:
                        predict = -predict
                    else:
                        predict = 400 - predict
                if -5 < predict - scene_info['platform'][0] - 20 and predict - scene_info['platform'][0] -20 < 5:
                    return 'NONE'
                if predict < scene_info['platform'][0] + 20:
                    return 'MOVE_LEFT'
                return 'MOVE_RIGHT'


            if scene_info['ball'][0] < scene_info['platform'][0] + 20:
                return 'MOVE_LEFT'
            return 'MOVE_RIGHT'
        # moving down

        ball = [ scene_info['ball'][0] , scene_info['ball'][1] ]
        while True:
            hit = False
            minT = 1e6
            if vx < 0: # 撞磚側 球向左
                Tlimit = ball[0] / (-vx)
                for b in scene_info['bricks']:
                    if b[0] + 25 > ball[0] or b[1] < ball[1]:
                        continue
                    t = (b[0] + 25 - scene_info['ball'][0]) / vx
                    if t > Tlimit:
                        continue
                    py = ball[1] + vy * t
                    if b[1] <= py and py <= b[1] + 10:
                        hit = True
                        minT = min(minT, t)
            else: # 撞磚側 球向右
                Tlimit = (200 - ball[0]) / vx
                for b in scene_info['bricks']:
                    if b[0] < ball[0] or b[1] < scene_info['ball'][1]:
                        continue
                    t = (b[0] - ball[0]) / vx
                    if t > Tlimit:
                        continue
                    py = ball[1] + vy * t
                    if b[1] <= py and py <= b[1] + 10:
                        hit = True
                        minT = min(minT, t)
            if hit:
                ball[0] = ball[0] + vx * minT
                ball[1] = ball[1] + vy * minT
                vx = -vx
            else:
                break

        
        t = (400 - ball[1]) / vy
        predict = ball[0] + vx * t

        while 0 > predict or predict > 200:
            if 0 > predict:
                predict = -predict
            else:
                predict = 400 - predict
        if -5 < predict - scene_info['platform'][0] - 20 and predict - scene_info['platform'][0] -20 < 5:
            return 'NONE'
        if predict < scene_info['platform'][0] + 20:
            return 'MOVE_LEFT'
        return 'MOVE_RIGHT'



    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
