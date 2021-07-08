"""
The template of the script for the machine learning process in game pingpong
"""
import math
blocker_width=30
blocker_height=20
#python MLGame.py -r -f 80 -i ml_play_template.py pingpong HARD 3
#python MLGame.py -r -f 80 -i ml_play_template.py -i ml_play_template_n.py pingpong HARD 3
#python MLGame.py -r -f 80 -i ml_play_template_n.py -i ml_play_template.py pingpong HARD 3
#python MLGame.py -r -f 80 -i ml_play_template_n.py pingpong HARD 3
class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.scene_info={}
        self.blocker0_x=0
        self.left_bound=0
        self.his = {}
        # with open("D:\大學課程\ML\mlgame\MLGame-master\MLGame-master\input.txt",'r') as f:
        #     self.left_bound=f.read()
        # self.left_bound=int(self.left_bound)
        # print(self.left_bound)

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"
        # if(self.side=="1P"):
        #     print(scene_info)
        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        if not self.ball_served:
            # if not(scene_info['blocker'][0] == 60):
            #     return 'NONE'
            if self.his == {}:
                self.his = scene_info
                return 'NONE'
            # if self.side == '1P':
            #     if scene_info['ball'][1] == 415:
            #         print('serve from 1P')
            #     else:
            #         print('serve from 2P')
            if scene_info['ball'][1] == 415 and (scene_info['blocker'][0] != 160 or (scene_info['blocker'][0] > self.his['blocker'][0])):
                self.his = scene_info
                return 'NONE'
            if scene_info['ball'][1] == 80 and (scene_info['blocker'][0] != 140 or (scene_info['blocker'][0] < self.his['blocker'][0])):
                self.his = scene_info
                return 'NONE'
            if self.side == '1P':
                print('start at : ', end = '')
                print(scene_info['blocker'][0])
                print('x  = ', end = '')
                print(scene_info['ball'][0])
                print('y  = ', end = '')
                print(scene_info['ball'][1])
                # print('')
            self.ball_served = True
            self.scene_info=scene_info
            self.scene_info=self.sceneinfo_tupleToList()
            self.blocker0_x=scene_info["blocker"][0]-5
            return "SERVE_TO_LEFT"
            # return "SERVE_TO_RIGHT"
        else:
            if not(self.blocker0_x-scene_info["blocker"][0]):
                return  "NONE"
            # print(scene_info)
            # print("現在",scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"])
            # if(scene_info["ball"][1]>=420 or scene_info["ball"][1]<=80):
            # print(scene_info["ball"],"ball")
            self.scene_info=scene_info
            self.sceneinfo_tupleToList()
            if(self.side=="1P"):
                command=self.predict_p1()
            else:
                command=self.predict_p2()

            self.blocker0_x=scene_info["blocker"][0]
            return command
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
    
    def sceneinfo_tupleToList(self):
        self.scene_info["ball"]=list(self.scene_info["ball"])
        self.scene_info['ball_speed']=list(self.scene_info['ball_speed'])
        self.scene_info['platform_1P']=list(self.scene_info['platform_1P'])
        self.scene_info['platform_2P']=list(self.scene_info['platform_2P'])
        return self
    
    def predict_p1(self):
        path_list=[]
        predict_b=[self.scene_info["ball"][0],self.scene_info["ball"][1]]
        predict_blocker_x=self.scene_info["blocker"][0]
        blokcer_v=(self.scene_info["blocker"][0]-self.blocker0_x)
        while(predict_b[1]!=415):
            # path_list.append([predict_b[0], predict_b[1]])
            if(not(self.scene_info["frame"]%100)):
                if(self.scene_info["ball_speed"][0]>0):
                    self.scene_info["ball_speed"][0]+=1
                else:
                    self.scene_info["ball_speed"][0]-=1
                if(self.scene_info["ball_speed"][1]>0):
                    self.scene_info["ball_speed"][1]+=1
                else:
                    self.scene_info["ball_speed"][1]-=1
            # print("預測",predict_b,self.scene_info["ball_speed"])
            if (( (235-predict_b[1])<=abs(self.scene_info["ball_speed"][1]) and ((235-predict_b[1])>0) ) or (predict_b[1]<240+blocker_height and predict_b[1]>235) ) and (self.scene_info["ball_speed"][1]>0):
                #球上方塊下 球往下,球可能打到方塊上,注意球體積
                predict_blocker_x2=predict_blocker_x+1-1
                predict_b2=[predict_b[0]+1-1,predict_b[1]+1-1]
                blokcer_v2=blokcer_v
                ball_v2=[self.scene_info["ball_speed"][0],self.scene_info["ball_speed"][1]]
                isColide=0
                predict_b2_list=[]
                for i in range(0,abs(self.scene_info["ball_speed"][1])):
                    if not(isColide):
                        predict_b2[0]+=int(ball_v2[0]/abs(ball_v2[0]))  #可能須校正
                    predict_b2[1]+=int(ball_v2[1]/abs(ball_v2[1]))
                    predict_blocker_x2+=round(blokcer_v2/abs(self.scene_info["ball_speed"][1]),0)   #小心
        
                    if(predict_blocker_x2<0):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=-predict_blocker_x2
                    elif(predict_blocker_x2>170):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=340-predict_blocker_x2

                    if(predict_b2[0]<=0):
                        # ball_v2[0]=-ball_v2[0]
                        isColide=1
                        predict_b2[0]=0
                    elif(predict_b[0]>=195):
                        # ball_v2[0]=-ball_v2[0]
                        isColide=1
                        predict_b2[0]=195
                    
                    predict_b2_list.append([predict_b2[0],predict_b2[1]])
                    # if(predict_b2[1]==235):
                    #     print("y=235的位置",predict_b2[0],predict_blocker_x2)
                    if(predict_b2[1]==235 and ((predict_b2[0]>predict_blocker_x2 and predict_b2[0]<(predict_blocker_x2+blocker_width)) or (predict_b2[0]+5>predict_blocker_x2 and predict_b2[0]+5<(predict_blocker_x2+blocker_width)))):  #球打到方塊上
                        self.scene_info["frame"]+=1
                        predict_b[0]+=self.scene_info["ball_speed"][0]
                        predict_b[1]=predict_b2[1]
                        # print(predict_b,predict_blocker_x,"上撞擊點")

                        predict_blocker_x+=blokcer_v
                        if(predict_blocker_x<0):
                            predict_blocker_x=-predict_blocker_x
                            blokcer_v=-blokcer_v
                        elif(predict_blocker_x>170):
                            predict_blocker_x=340-predict_blocker_x
                            blokcer_v=-blokcer_v

                        self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]

                        if(predict_b[0]<=0):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=0
                        elif(predict_b[0]>=195):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=195
                        break
                    else:
                        # predict_blocker_x_next=predict_blocker_x+blokcer_v  #還是以1/7幀算
                        # if(predict_blocker_x_next<0):
                        #     predict_blocker_x_next=-predict_blocker_x_next
                        # elif(predict_blocker_x_next>170):
                        #     predict_blocker_x_next=340-predict_blocker_x_next
                        if(((predict_b2[0]+5<predict_blocker_x2+blocker_width) and (predict_b2[0]+5>predict_blocker_x2)) or ((predict_b2[0]>predict_blocker_x2) and (predict_b2[0]<predict_blocker_x2+blocker_width))) and ((predict_b2[1]<240+blocker_height and predict_b2[1]+5>240+blocker_height) or (predict_b2[1]+5>240 and predict_b2[1]<240)): #球打到方塊左右,限球速<30
                            if(ball_v2[0]>0): #往下撞方塊左邊  
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x
                                # print(predict_b,predict_blocker_x,"左邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            else:   #往下撞方塊右邊
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x+blocker_width
                                # print(predict_b,predict_blocker_x,"右邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            break
                        elif(i==abs(self.scene_info["ball_speed"][1])-1):
                            #到下一幀時依然沒撞到方塊
                            self.scene_info["frame"]+=1
                            predict_b[0]+=self.scene_info["ball_speed"][0]  #下一幀預定位置
                            predict_b[1]+=self.scene_info["ball_speed"][1]
                            predict_blocker_x+=blokcer_v
                            
                            if(predict_blocker_x<0):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=-predict_blocker_x
                            elif(predict_blocker_x>170):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=340-predict_blocker_x

                            if(predict_b[1]<=80):   
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                # predict_b[0]-=self.scene_info["ball_speed"][0]
                                # predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(80-predict_b[1]))
                                predict_b[1]=80
                            elif(predict_b[1]>=415):
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                # predict_b[1]=415
                                predict_b[0]-=self.scene_info["ball_speed"][0]
                                predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(predict_b[1]-415))
                                predict_b[1]=415

                            if(predict_b[0]<=0):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=0
                            elif(predict_b[0]>=195):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=195
                            break
            elif (( (predict_b[1]-(240+blocker_height))<=abs(self.scene_info["ball_speed"][1]) and ((predict_b[1]-(240+blocker_height))>0)) or (predict_b[1]<240+blocker_height and predict_b[1]>235)  ) and (self.scene_info["ball_speed"][1]<0):
                #球下方塊上 球往上,球可能打到方塊下,注意原本為if
                predict_blocker_x2=predict_blocker_x+1-1
                predict_b2=[predict_b[0],predict_b[1]]
                blokcer_v2=blokcer_v
                ball_v2=[self.scene_info["ball_speed"][0],self.scene_info["ball_speed"][1]]
                isColide=0
                predict_b2_list=[]
                for i in range(0,abs(self.scene_info["ball_speed"][1]) ):
                    if not(isColide):
                        predict_b2[0]+=int(ball_v2[0]/abs(ball_v2[0]))
                    predict_b2[1]+=int(ball_v2[1]/abs(ball_v2[1]))
                    predict_blocker_x2+=round((blokcer_v2)/abs(self.scene_info["ball_speed"][1]),0)

                    if(predict_blocker_x2<0):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=-predict_blocker_x2
                    elif(predict_blocker_x2>170):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=340-predict_blocker_x2

                    if(predict_b2[0]<=0):
                        # ball_v2[0]=-ball_v2[0]
                        predict_b2[0]=0
                        isColide=1
                    elif(predict_b[0]>=195):
                        # ball_v2[0]=-ball_v2[0]
                        predict_b2[0]=195
                        isColide=1
                    
                    predict_b2_list.append([predict_b2[0],predict_b2[1]])
                    # if(predict_b2[1]==260):
                    #     print("y=260的位置",predict_b2[0],predict_blocker_x2)
                    if (predict_b2[1]==240+blocker_height) and ((predict_b2[0]>predict_blocker_x2 and predict_b2[0]<(predict_blocker_x2+blocker_width) ) or (predict_b2[0]+5>predict_blocker_x2 and predict_b2[0]+5<(predict_blocker_x2+blocker_width))):#球打到方塊下 
                        self.scene_info["frame"]+=1
                        predict_b[0]+=self.scene_info["ball_speed"][0]
                        predict_b[1]=predict_b2[1]
                        # print(predict_b,predict_blocker_x,"下撞擊點")

                        predict_blocker_x+=blokcer_v
                        if(predict_blocker_x<0):
                            blokcer_v=-blokcer_v
                            predict_blocker_x=-predict_blocker_x
                        elif(predict_blocker_x>170):
                            blokcer_v=-blokcer_v
                            predict_blocker_x=340-predict_blocker_x
                            
                        self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]

                        if(predict_b[0]<=0):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=0
                        elif(predict_b[0]>=195):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=195
                        break
                    else:
                        # predict_blocker_x_next=predict_blocker_x+blokcer_v
                        # if(predict_blocker_x_next<0):
                        #     predict_blocker_x_next=-predict_blocker_x_next
                        # elif(predict_blocker_x_next>170):
                        #     predict_blocker_x_next=340-predict_blocker_x_next
                        if(((predict_b2[0]+5>predict_blocker_x2) and (predict_b2[0]+5<predict_blocker_x2+blocker_width)) or ((predict_b2[0]>predict_blocker_x2) and (predict_b2[0]<predict_blocker_x2))) and ((predict_b2[1]<240+blocker_height and predict_b2[1]+5>240+blocker_height) or (predict_b2[1]+5>240 and predict_b2[1]<240)): #球打到方塊左右
                            if(ball_v2[0]>0): #往上撞方塊左邊
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x
                                # print(predict_b,predict_blocker_x,"左邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            else:   #往上撞方塊右邊
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x+blocker_width
                                # print(predict_b,predict_blocker_x,"右邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            break
                        elif(i==abs(self.scene_info["ball_speed"][1])-1):
                            #到下一幀時依然沒撞到方塊
                            self.scene_info["frame"]+=1
                            predict_b[0]+=self.scene_info["ball_speed"][0]  #下一幀預定位置
                            predict_b[1]+=self.scene_info["ball_speed"][1]
                            predict_blocker_x+=blokcer_v
                            
                            if(predict_blocker_x<0):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=-predict_blocker_x
                            elif(predict_blocker_x>170):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=340-predict_blocker_x

                            if(predict_b[1]<=80):   
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                # predict_b[0]-=self.scene_info["ball_speed"][0]
                                # predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(80-predict_b[1]))
                                predict_b[1]=80
                            elif(predict_b[1]>=415):
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                # predict_b[1]=415
                                predict_b[0]-=self.scene_info["ball_speed"][0]
                                predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(predict_b[1]-415))
                                predict_b[1]=415

                            if(predict_b[0]<=0):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=0
                            elif(predict_b[0]>=195):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=195
                            break
            else:
                #非以上的狀況
                self.scene_info["frame"]+=1
                predict_b[0]+=self.scene_info["ball_speed"][0]  #下一幀預定位置
                predict_b[1]+=self.scene_info["ball_speed"][1]
                predict_blocker_x+=blokcer_v
                if(predict_blocker_x<0):
                    predict_blocker_x=-predict_blocker_x
                    blokcer_v=-blokcer_v
                elif(predict_blocker_x>170):
                    predict_blocker_x=340-predict_blocker_x
                    blokcer_v=-blokcer_v

                if(predict_b[1]<=80):   
                    self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                    # predict_b[0]-=self.scene_info["ball_speed"][0]
                    # predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(80-predict_b[1]))
                    predict_b[1]=80
                elif(predict_b[1]>=415):
                    self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                    # predict_b[1]=415
                    predict_b[0]-=self.scene_info["ball_speed"][0]
                    predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(predict_b[1]-415))
                    predict_b[1]=415

                if(predict_b[0]<=0):
                    self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                    predict_b[0]=0
                elif(predict_b[0]>=195):
                    self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                    predict_b[0]=195

        # print(predict_b,self.side,self.scene_info["platform_1P"])
        # print(path_list,"路徑分析")
        if(predict_b[0]>self.scene_info["platform_1P"][0]+35):
            return "MOVE_RIGHT"
        elif(predict_b[0]<self.scene_info["platform_1P"][0]+5):
            return "MOVE_LEFT"
        else:
            return "NONE"

    # def predict_p2(self):
    #     predict_b=self.scene_info["ball"]
    #     while(predict_b[1]!=80):
    #         if(not(self.scene_info["frame"]%100)):
    #             if(self.scene_info["ball_speed"][0]>0):
    #                 self.scene_info["ball_speed"][0]+=1
    #             else:
    #                 self.scene_info["ball_speed"][0]-=1
    #             if(self.scene_info["ball_speed"][1]>0):
    #                 self.scene_info["ball_speed"][1]+=1
    #             else:
    #                 self.scene_info["ball_speed"][1]-=1

    #         self.scene_info["frame"]+=1
    #         predict_b[0]+=self.scene_info["ball_speed"][0]
    #         predict_b[1]+=self.scene_info["ball_speed"][1]
            
    #         if(predict_b[1]<=80):
    #             self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
    #             # predict_b[1]=80
    #             predict_b[0]-=self.scene_info["ball_speed"][0]
    #             predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(80-predict_b[1]))
    #             predict_b[1]=80
    #         elif(predict_b[1]>=415):
    #             self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
    #             predict_b[1]=415
    #         if(predict_b[0]<=0):
    #             self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
    #             predict_b[0]=0
    #         elif(predict_b[0]>=195):
    #             self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
    #             predict_b[0]=195
    
    #     # print(predict_b,self.side,self.scene_info["platform_2P"])
    #     if(predict_b[0]>self.scene_info["platform_2P"][0]+40):
    #         return "MOVE_RIGHT"
    #     elif(predict_b[0]<self.scene_info["platform_2P"][0]):
    #         return "MOVE_LEFT"
    #     else:
    #         return "NONE"
    def predict_p2(self):
        # path_list=[]
        predict_b=[self.scene_info["ball"][0],self.scene_info["ball"][1]]
        predict_blocker_x=self.scene_info["blocker"][0]
        blokcer_v=(self.scene_info["blocker"][0]-self.blocker0_x)
        while(predict_b[1]!=80):
            # path_list.append([predict_b[0], predict_b[1]])
            if(not(self.scene_info["frame"]%100)):
                if(self.scene_info["ball_speed"][0]>0):
                    self.scene_info["ball_speed"][0]+=1
                else:
                    self.scene_info["ball_speed"][0]-=1
                if(self.scene_info["ball_speed"][1]>0):
                    self.scene_info["ball_speed"][1]+=1
                else:
                    self.scene_info["ball_speed"][1]-=1
            # print("預測",predict_b,self.scene_info["ball_speed"])
            if (( (235-predict_b[1])<=abs(self.scene_info["ball_speed"][1]) and ((235-predict_b[1])>0) ) or (predict_b[1]<240+blocker_height and predict_b[1]>235) ) and (self.scene_info["ball_speed"][1]>0):
                #球上方塊下 球往下,球可能打到方塊上,注意球體積
                predict_blocker_x2=predict_blocker_x+1-1
                predict_b2=[predict_b[0]+1-1,predict_b[1]+1-1]
                blokcer_v2=blokcer_v
                ball_v2=[self.scene_info["ball_speed"][0],self.scene_info["ball_speed"][1]]
                isColide=0
                # predict_b2_list=[]
                for i in range(0,abs(self.scene_info["ball_speed"][1])):
                    if not(isColide):
                        predict_b2[0]+=int(ball_v2[0]/abs(ball_v2[0]))  #可能須校正
                    predict_b2[1]+=int(ball_v2[1]/abs(ball_v2[1]))
                    predict_blocker_x2+=round(blokcer_v2/abs(self.scene_info["ball_speed"][1]),0)   #小心
        
                    if(predict_blocker_x2<0):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=-predict_blocker_x2
                    elif(predict_blocker_x2>170):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=340-predict_blocker_x2

                    if(predict_b2[0]<=0):
                        # ball_v2[0]=-ball_v2[0]
                        isColide=1
                        predict_b2[0]=0
                    elif(predict_b[0]>=195):
                        # ball_v2[0]=-ball_v2[0]
                        isColide=1
                        predict_b2[0]=195
                    
                    # predict_b2_list.append([predict_b2[0],predict_b2[1]])
                    # if(predict_b2[1]==235):
                    #     print("y=235的位置",predict_b2[0],predict_blocker_x2)
                    if(predict_b2[1]==235 and ((predict_b2[0]>predict_blocker_x2 and predict_b2[0]<(predict_blocker_x2+blocker_width)) or (predict_b2[0]+5>predict_blocker_x2 and predict_b2[0]+5<(predict_blocker_x2+blocker_width)))):  #球打到方塊上
                        self.scene_info["frame"]+=1
                        predict_b[0]+=self.scene_info["ball_speed"][0]
                        predict_b[1]=predict_b2[1]
                        # print(predict_b,predict_blocker_x,"上撞擊點")

                        predict_blocker_x+=blokcer_v
                        if(predict_blocker_x<0):
                            predict_blocker_x=-predict_blocker_x
                            blokcer_v=-blokcer_v
                        elif(predict_blocker_x>170):
                            predict_blocker_x=340-predict_blocker_x
                            blokcer_v=-blokcer_v

                        self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]

                        if(predict_b[0]<=0):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=0
                        elif(predict_b[0]>=195):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=195
                        break
                    else:
                        # predict_blocker_x_next=predict_blocker_x+blokcer_v  #還是以 1/速度 幀算
                        # if(predict_blocker_x_next<0):
                        #     predict_blocker_x_next=-predict_blocker_x_next
                        # elif(predict_blocker_x_next>170):
                        #     predict_blocker_x_next=340-predict_blocker_x_next
                        if(((predict_b2[0]+5<predict_blocker_x2+blocker_width) and (predict_b2[0]+5>predict_blocker_x2)) or ((predict_b2[0]>predict_blocker_x2) and (predict_b2[0]<predict_blocker_x2+blocker_width))) and ((predict_b2[1]<240+blocker_height and predict_b2[1]+5>240+blocker_height) or (predict_b2[1]+5>240 and predict_b2[1]<240)): #球打到方塊左右,限球速<30
                            if(ball_v2[0]>0): #往下撞方塊左邊  
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x
                                # print(predict_b,predict_blocker_x,"左邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            else:   #往下撞方塊右邊
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x+blocker_width
                                # print(predict_b,predict_blocker_x,"右邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            break
                        elif(i==abs(self.scene_info["ball_speed"][1])-1):
                            #到下一幀時依然沒撞到方塊
                            self.scene_info["frame"]+=1
                            predict_b[0]+=self.scene_info["ball_speed"][0]  #下一幀預定位置
                            predict_b[1]+=self.scene_info["ball_speed"][1]
                            predict_blocker_x+=blokcer_v
                            
                            if(predict_blocker_x<0):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=-predict_blocker_x
                            elif(predict_blocker_x>170):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=340-predict_blocker_x

                            if(predict_b[1]<=80):   
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                predict_b[0]-=self.scene_info["ball_speed"][0]
                                predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(80-predict_b[1]))
                                predict_b[1]=80
                            elif(predict_b[1]>=415):
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                # predict_b[1]=415
                                # predict_b[0]-=self.scene_info["ball_speed"][0]
                                # predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(predict_b[1]-415))
                                predict_b[1]=415

                            if(predict_b[0]<=0):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=0
                            elif(predict_b[0]>=195):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=195
                            break
            elif (( (predict_b[1]-(240+blocker_height))<=abs(self.scene_info["ball_speed"][1]) and ((predict_b[1]-(240+blocker_height))>0)) or (predict_b[1]<240+blocker_height and predict_b[1]>235)  ) and (self.scene_info["ball_speed"][1]<0):
                #球下方塊上 球往上,球可能打到方塊下,注意原本為if
                predict_blocker_x2=predict_blocker_x+1-1
                predict_b2=[predict_b[0],predict_b[1]]
                blokcer_v2=blokcer_v
                ball_v2=[self.scene_info["ball_speed"][0],self.scene_info["ball_speed"][1]]
                isColide=0
                # predict_b2_list=[]
                for i in range(0,abs(self.scene_info["ball_speed"][1]) ):
                    if not(isColide):
                        predict_b2[0]+=int(ball_v2[0]/abs(ball_v2[0]))
                    predict_b2[1]+=int(ball_v2[1]/abs(ball_v2[1]))
                    predict_blocker_x2+=round((blokcer_v2)/abs(self.scene_info["ball_speed"][1]),0)

                    if(predict_blocker_x2<0):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=-predict_blocker_x2
                    elif(predict_blocker_x2>170):
                        blokcer_v2=-blokcer_v2
                        predict_blocker_x2=340-predict_blocker_x2

                    if(predict_b2[0]<=0):
                        # ball_v2[0]=-ball_v2[0]
                        predict_b2[0]=0
                        isColide=1
                    elif(predict_b[0]>=195):
                        # ball_v2[0]=-ball_v2[0]
                        predict_b2[0]=195
                        isColide=1
                    
                    # predict_b2_list.append([predict_b2[0],predict_b2[1]])
                    # if(predict_b2[1]==260):
                    #     print("y=260的位置",predict_b2[0],predict_blocker_x2)
                    if (predict_b2[1]==240+blocker_height) and ((predict_b2[0]>predict_blocker_x2 and predict_b2[0]<(predict_blocker_x2+blocker_width) ) or (predict_b2[0]+5>predict_blocker_x2 and predict_b2[0]+5<(predict_blocker_x2+blocker_width))):#球打到方塊下 
                        self.scene_info["frame"]+=1
                        predict_b[0]+=self.scene_info["ball_speed"][0]
                        predict_b[1]=predict_b2[1]
                        # print(predict_b,predict_blocker_x,"下撞擊點")

                        predict_blocker_x+=blokcer_v
                        if(predict_blocker_x<0):
                            blokcer_v=-blokcer_v
                            predict_blocker_x=-predict_blocker_x
                        elif(predict_blocker_x>170):
                            blokcer_v=-blokcer_v
                            predict_blocker_x=340-predict_blocker_x
                            
                        self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]

                        if(predict_b[0]<=0):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=0
                        elif(predict_b[0]>=195):
                            self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            predict_b[0]=195
                        break
                    else:
                        # predict_blocker_x_next=predict_blocker_x+blokcer_v
                        # if(predict_blocker_x_next<0):
                        #     predict_blocker_x_next=-predict_blocker_x_next
                        # elif(predict_blocker_x_next>170):
                        #     predict_blocker_x_next=340-predict_blocker_x_next
                        if(((predict_b2[0]+5>predict_blocker_x2) and (predict_b2[0]+5<predict_blocker_x2+blocker_width)) or ((predict_b2[0]>predict_blocker_x2) and (predict_b2[0]<predict_blocker_x2))) and ((predict_b2[1]<240+blocker_height and predict_b2[1]+5>240+blocker_height) or (predict_b2[1]+5>240 and predict_b2[1]<240)): #球打到方塊左右
                            if(ball_v2[0]>0): #往上撞方塊左邊
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x
                                # print(predict_b,predict_blocker_x,"左邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            else:   #往上撞方塊右邊
                                self.scene_info["frame"]+=1
                                predict_blocker_x+=blokcer_v
                                if(predict_blocker_x<0):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=-predict_blocker_x
                                elif(predict_blocker_x>170):
                                    blokcer_v=-blokcer_v
                                    predict_blocker_x=340-predict_blocker_x

                                predict_b[1]+=self.scene_info["ball_speed"][1]
                                predict_b[0]=predict_blocker_x+blocker_width
                                # print(predict_b,predict_blocker_x,"右邊撞擊點")
                                # print("撞到前的路徑",predict_b2_list)

                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                            break
                        elif(i==abs(self.scene_info["ball_speed"][1])-1):
                            #到下一幀時依然沒撞到方塊
                            self.scene_info["frame"]+=1
                            predict_b[0]+=self.scene_info["ball_speed"][0]  #下一幀預定位置
                            predict_b[1]+=self.scene_info["ball_speed"][1]
                            predict_blocker_x+=blokcer_v
                            
                            if(predict_blocker_x<0):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=-predict_blocker_x
                            elif(predict_blocker_x>170):
                                blokcer_v=-blokcer_v
                                predict_blocker_x=340-predict_blocker_x

                            if(predict_b[1]<=80):   
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                predict_b[0]-=self.scene_info["ball_speed"][0]
                                predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(80-predict_b[1]))
                                predict_b[1]=80
                            elif(predict_b[1]>=415):
                                self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                                # predict_b[1]=415
                                # predict_b[0]-=self.scene_info["ball_speed"][0]
                                # predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(predict_b[1]-415))
                                predict_b[1]=415

                            if(predict_b[0]<=0):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=0
                            elif(predict_b[0]>=195):
                                self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                                predict_b[0]=195
                            break
            else:
                #非以上的狀況
                self.scene_info["frame"]+=1
                predict_b[0]+=self.scene_info["ball_speed"][0]  #下一幀預定位置
                predict_b[1]+=self.scene_info["ball_speed"][1]
                predict_blocker_x+=blokcer_v
                if(predict_blocker_x<0):
                    predict_blocker_x=-predict_blocker_x
                    blokcer_v=-blokcer_v
                elif(predict_blocker_x>170):
                    predict_blocker_x=340-predict_blocker_x
                    blokcer_v=-blokcer_v

                if(predict_b[1]<=80):   
                    self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                    predict_b[0]-=self.scene_info["ball_speed"][0]
                    predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(80-predict_b[1]))
                    predict_b[1]=80
                elif(predict_b[1]>=415):
                    self.scene_info["ball_speed"][1]=-self.scene_info["ball_speed"][1]
                    # predict_b[1]=415
                    # predict_b[0]-=self.scene_info["ball_speed"][0]
                    # predict_b[0]+=int(self.scene_info["ball_speed"][0]/abs(self.scene_info["ball_speed"][0]))*(abs(self.scene_info["ball_speed"][1])-(predict_b[1]-415))
                    predict_b[1]=415

                if(predict_b[0]<=0):
                    self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                    predict_b[0]=0
                elif(predict_b[0]>=195):
                    self.scene_info["ball_speed"][0]=-self.scene_info["ball_speed"][0]
                    predict_b[0]=195

        # print(predict_b,self.side,self.scene_info["platform_1P"])
        # print(path_list,"路徑分析")
        if(predict_b[0]>self.scene_info["platform_2P"][0]+35):
            return "MOVE_RIGHT"
        elif(predict_b[0]<self.scene_info["platform_2P"][0]+5):
            return "MOVE_LEFT"
        else:
            return "NONE"
            
    