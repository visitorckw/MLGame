"""
The template of the main script of the machine learning process
"""
import os.path
import pickle

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        filename = 'model.pickle'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.last = int(2)

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS"):
            return "RESET"

        head = scene_info['snake_head']
        
        command = self.model.predict([[ head[0], head[1], self.last ]])
        if command:
            self.last = int(command)

        if command == 0: return "NONE"
        elif command == 1: return "UP"
        elif command == 2: return "DOWN"
        elif command == 3: return "LEFT"
        else: return "RIGHT"

    def reset(self):
        """
        Reset the status
        """
        self.last = 2
