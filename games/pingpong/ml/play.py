"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.his = []

    def update(self, scene_info):
        
        """
        Generate the command according to the received scene information
        """
        if scene_info['status'] == "GAME_1P_WIN" or scene_info['status'] == "GAME_2P_WIN":
            print(scene_info['ball_speed'])
       
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"

        if not len(self.his):
            self.his.append(scene_info)
            return 'NONE'

        self.his = [self.his[-1]]
        ball = list(scene_info['ball'])
        v = list(scene_info['ball_speed'])
        block = list(scene_info['blocker'])
        Vblock = scene_info['blocker'][0] - self.his[-1]['blocker'][0]
        predict = 100
        while True:
            if ball[1] <= block[1] and v[1] > 0:
                t = (block[1] - (ball[1] + 5)) / v[1]
                px = ball[0] + v[0] * t
                bx = block[0] + Vblock * t
                bounce = 0
                Bbounce = 0
                while px < 0 or px > 195:
                    bounce += 1
                    if px < 0:
                        px = -px
                    else:
                        px = 390 - px
                while bx < 0 or bx > 170:
                    Bbounce += 1
                    if bx < 0:
                        bx = -bx
                    else:
                        bx = 340 - bx
                if bx <= px + 5 and px <= bx + 30: # hit up
                    ball[0] = bx 
                    ball[1] = block[1] + 5 
                    v[1] *= -1
                    if self.side == '1P':
                        print('Hit Up')
                    continue
                ball[0] = px
                ball[1] = ball[1] + v[1] * t
                block[0] = bx
                if bounce & 1:
                    v[0] *= -1
                if Bbounce & 1:
                    Vblock *= -1
            if ball[1] >= block[1] + 20 and v[1] < 0:
                t = (block[1] + 20 - (ball[1])) / v[1]
                px = ball[0] + v[0] * t
                bx = block[0] + Vblock * t
                bounce = 0
                Bbounce = 0
                while px < 0 or px > 195:
                    bounce += 1
                    if px < 0:
                        px = -px
                    else:
                        px = 390 - px
                while bx < 0 or bx > 170:
                    Bbounce += 1
                    if bx < 0:
                        bx = -bx
                    else:
                        bx = 340 - bx
                if bx <= px and px <= bx + 30: # hit down
                    ball[0] = bx
                    ball[1] = block[1] + 20
                    v[1] *= -1
                    if self.side == '1P':
                        print('Hit Down')
                    continue
                ball[0] = px
                ball[1] = ball[1] + v[1] * t
                block[0] = bx
                if bounce & 1:
                    v[0] *= -1
                if Bbounce & 1:
                    Vblock *= -1
            
            if (v[1] > 0 and ball[1] > block[1] + 20 and self.side == '2P') or (v[1] < 0 and ball[1] < block[1] and self.side == '1P'):
                predict = 97.5
                break  
            if v[1] > 0:
                t = (420 - 5 - ball[1]) / v[1]
                px = ball[0] + v[0] * t
            else:
                t = (80 - ball[1]) / v[1]
                px = ball[0] + v[0] * t
            while px < 0 or px > 195:
                if px < 0:
                    px = - px
                else:
                    px = 390 - px
            predict = px + 2.5
            break
        # if scene_info['frame'] % 10 == 0:
            # print('predict = ', end = '')
            # print(predict)
        self.his.append(scene_info)
        plat = scene_info['platform_1P'] if self.side == '1P' else scene_info['platform_2P']
        if -3.0 <= plat[0] + 15 - predict and plat[0] + 15 - predict <= 3.0:
            return 'NONE'
        if plat[0] + 15 > predict:
            return 'MOVE_LEFT'
        else:
            return 'MOVE_RIGHT'
        return 'NONE'
        
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
