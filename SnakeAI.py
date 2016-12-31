import random
class SnakeAI:
    def __init__(self, game):
        self.game = game
        self.width = game.width
        self.height = game.height
    # This is the major function you need to implement
    # The function takes "game" as an argument, you need to determine whether 
    # the snake should go "Up" or "Down" or "Left" or "Right"
    def GetDirection(self, game):
        return random.choice(['Up', 'Down', 'Left', 'Right'])
