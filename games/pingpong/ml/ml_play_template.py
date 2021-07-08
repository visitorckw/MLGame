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
        self.block_his = []
        self.counter = 0

    def update(self, scene_info):
        # print('ball = ', end ='')
        # print(scene_info['ball'])
        # print('blocker = ', end ='')
        # print(scene_info['blocker'])
        """
        Generate the command according to the received scene information
        """
        if scene_info['status'] == "GAME_1P_WIN" or scene_info['status'] == "GAME_2P_WIN":
            print(scene_info['ball_speed'])
        # if self.side == '1P':
            # print('ball = ' ,end = '')
            # print(scene_info['ball'])
            # print('blocker = ', end = '')
            # print(scene_info['blocker'], end = '\n\n')
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        # else:
            # return "MOVE_LEFT"

        ball = list(scene_info['ball'])
        v = list(scene_info['ball_speed'])
        plate = list(scene_info['platform_1P']) if self.side == '1P' else list(scene_info['platform_2P'])
        pic = scene_info['frame'] % 100
        predict = 80
        solve = False
        block = list(scene_info['blocker'])
        Vblock = 0
        if len(self.block_his):
            Vblock = block[0] - self.block_his[-1]
        self.block_his.append(block[0])

        # if ball[1] >= 420 and self.side == '1P':
        #     print('ball = ', end = '')
        #     print(ball)
        #     print('plate = ', end ='')
        #     print(plate)
        #     return 'NONE'
        ctr = 0
        while not solve:
            if ctr >= 50:
                return 'NONE'
            ctr += 1
            # time = 100 - pic - 3 # for jumping accelerate
            # if v[0] < 0:
            #     time = min(time, int(-ball[0]//v[0]))
            # else:
            #     time = min(time, int((195 - ball[0]) // v[0]))
            # if v[1] > 0:
            #     time = min(time, int((420 - ball[1]) // v[1]))
            # else:
            #     time = min(time, int((80 - ball[1]) // v[1]))
            # time -= 3
            # if time < 0:
            #     time = 0
            # print('time = ', end = '')
            # print(time)
            ball[0] += v[0] #+ time * v[0]
            ball[1] += v[1] #+ time * v[1]
            pic += 1 # + time
            if block[0] <= 0 or block[0] >= 170:
                Vblock = -Vblock
            block[0] += Vblock
            if pic > 100:
                if v[0] > 0:
                    v[0] += 1
                else:
                    v[0] -= 1
                if v[1] > 0:
                    v[1] += 1
                else:
                    v[1] -= 1 
                pic -= 100
            if ball[0] <= 0:
                ball[0] = 0
                v[0] = -v[0]
                # print('hit left')
            elif ball[0] >= 195:
                ball[0] = 195
                v[0] = -v[0]
                # print('hit right')
            if ball[1] >= 420:
                if self.side == '1P':
                    predict = ball[0]
                    solve = True
                    break
                ball[1] = 415
                v[1] = -v[1]
                # print('hit P1')
            elif ball[1] <= 80:
                if self.side == '2P':
                    predict = ball[0]
                    solve = True
                    break
                ball[1] = 80
                v[1] = -v[1]
            
            if block[0] <= ball[0] and ball[0] <= block[0] + 30 and block[1] <= ball[1] and ball[1] <= ball[1] + 20:
                hitup = False
                hitdown = False
                hitleft = False
                hitright = False
                upT = 1000
                downT = 1000
                leftT = 1000
                rightT = 1000
                if v[1] > 0:
                    bx = ball[0] - v[0]
                    by = ball[1] - v[1]
                    time = (block[1] - by) / v[1]
                    hx = bx + v[0] * time
                    if block[0] <= hx and hx <= block[0] + 30:
                        # if self.side == '1P':
                        #     print('hit up', end = ' ')
                        #     print(self.counter)
                        #     self.counter += 1
                        # ball[1] = block[1] + 5
                        # v[1] = -v[1]
                        hitup = True
                        upT = time
                else:
                    bx = ball[0] - v[0]
                    by = ball[1] - v[1]
                    time = (block[1] + 20 - by) / v[1]
                    hx = bx + v[0] * time
                    if block[0] <= hx and hx <= block[0] + 30:
                        # if self.side == '1P':
                        #     print('hit down', end = ' ')
                        #     print(self.counter)
                        #     self.counter += 1
                        # ball[1] = block[1] + 20
                        # v[1] = -v[1]
                        hitdown = True
                        downT = time
                if v[0] > 0:
                    bx = ball[0] - v[0]
                    by = ball[1] - v[1]
                    time = (block[0] - bx) / v[0]
                    hy = by + v[1] * time
                    if block[1] <= hy and hy <= block[1] + 20:
                        # if self.side == '1P':
                        #     print('hit left', end = ' ')
                        #     print(self.counter)
                        #     self.counter += 1
                        # ball[0] = block[0] + 5
                        # v[0] = -v[0]
                        hitleft = True
                        leftT = time
                else:
                    bx = ball[0] - v[0]
                    by = ball[1] - v[1]
                    time = (block[0] + 30 - bx) / v[0]
                    hy = by + v[1] * time
                    if block[1] <= hy and hy <= block[1] + 20:
                    #     if self.side == '1P':
                    #         print('hit right', end = ' ')
                    #         print(self.counter)
                    #         self.counter += 1
                    #     ball[0] = block[0] + 30
                    #     v[0] = -v[0]
                        hitright = True
                        rightT = time
                # if not hitup and not hitdown and not hitleft and not hitright:
                    # continue
                hit = 'none'
                minT = 10.0
                if hitup and upT < minT:
                    hit = 'up'
                    minT = upT
                if hitdown and downT < minT:
                    hit = 'down'
                    minT = downT
                if hitleft and leftT < minT:
                    hit = 'left'
                    minT = leftT
                if hitright and rightT < minT:
                    hit = 'right'
                    minT = rightT
                
                if hit != 'none' and self.side == '1P':
                    print('Hit ' + hit, end = '')
                    print(self.counter)
                    self.counter += 1

                if hit == 'up':
                    ball[1] = block[1] + 5
                    v[1] = -v[1]
                elif hit == 'down':
                    ball[1] = block[1] + 20
                    v[1] = -v[1]
                elif hit == 'left':
                    ball[0] = block[0] + 5
                    v[0] = -v[0]
                elif hit == 'right':
                    ball[0] = block[0] + 30
                    v[0] = -v[0]
            
        predict += 2.5
        
        if -3 < predict - plate[0] - 15 and predict - plate[0] - 15 < 3:
            return 'NONE'
        if predict < plate[0] + 20:
            return 'MOVE_LEFT'
        return 'MOVE_RIGHT'
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
