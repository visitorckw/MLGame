"""
The template of the script for playing the game in the ml mode
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.last = 'D'

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"
        head = scene_info["snake_head"]
        # print(head)
        # food = scene_info["food"]

        if head[1] == 290:
            if head[0] >= 280:
                self.last = 'L'
                return 'LEFT'
            if head[0] == 0:
                self.last = 'U'
                return 'UP'
            return 'NONE'
        if head[1] == 280:
            if head[0] >= 280 and self.last == 'D':
                return 'NONE'
            if self.last == 'D':
                self.last = 'R'
                return 'RIGHT'
            else:
                self.last = 'U'
                return 'UP'
        if head[1] == 0:
            if self.last == 'U':
                self.last = 'R'
                return 'RIGHT'
            else:
                self.last = 'D'
                return 'DOWN'
        return 'NONE'
            

    def reset(self):
        """
        Reset the status if needed
        """
        self.last = 'D'
