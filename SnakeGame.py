from Tkinter import *
import random
import time
import SnakeAI
#============================= Snake Game =====================================
class Frame:
    def __init__(self, height = 480, width = 640, useAI = True, speed = 40):
        self.pixelSize = 20
        self.root = Tk()
        self.root.bind("<Key>", self.KeyPress)
        self.gameWidth = width
        self.gameHeight = height
        self.canvas = Canvas(self.root, bg='black',height=height, width=width)
        self.canvas.pack()
        self.speed = speed
        self.game = Game(height/self.pixelSize, width/self.pixelSize)
        # This is your AI
        self.useAI = useAI
        self.ai = SnakeAI.SnakeAI(self.game)
    def Show(self):
        self.game.start()
        self.Refresh()
        self.root.mainloop()
    def Refresh(self):
        self.game.Update()
        if self.game.state == 'play':
            self.canvas.delete('all')
            self.DrawGame()
            if self.useAI:
                self.game.ChangeDirection(self.ai.GetDirection(self.game))
            self.root.after(int(1000/self.speed), self.Refresh)
        else:
            self.canvas.delete('all')
            self.canvas.create_text(self.gameWidth/2,self.gameHeight/2,text="Game Over, press space to restart!", fill='white')
    def DrawGame(self):
        self.DrawRect(self.game.food.pos, 'blue')
        for p in self.game.snake.body[:-1]:
            self.DrawRect(p, 'white')
        self.DrawRect(self.game.snake.body[-1], 'red')
    def DrawRect(self, pos, color):
        x = pos[0]
        y = pos[1]
        pSize = self.pixelSize
        self.canvas.create_rectangle(x*pSize, y*pSize, (x+1)*pSize, (y+1)*pSize, fill=color)
    def KeyPress(self, event):
        sym = event.keysym
        if self.game.state == 'play':
            if sym in ['Up', 'Down', 'Left', 'Right']:
                if not self.useAI:
                    self.game.ChangeDirection(sym)
        elif self.game.state == 'end':
            if sym == 'space':
                self.game.start()
                self.Refresh()
class Game:
    def __init__(self, height = 20, width = 30):
        self.snake = Snake(width = width, height = height)
        self.food = Food(self.snake, width = width, height = height)
        self.width = width
        self.height = height
        self.speed = 5
        self.state = 'play'
    def start(self):
        self.state = 'play'
        self.snake.New()
        self.food.New(self.snake)
    def ChangeDirection(self, direction):
        if self.snake.direction[1] == 0:
            if direction == 'Up':
                self.snake.direction = (0,-1)
            elif direction == 'Down':
                self.snake.direction = (0,1)
        elif self.snake.direction[0] == 0:
            if direction == 'Left':
                self.snake.direction = (-1,0)
            elif direction == 'Right':
                self.snake.direction = (1,0)
    def Update(self):
        if not self.snake.dead:
            if self.snake.Next() == self.food.pos:
                self.snake.Move(eat = True)
                self.food.SetRandomPos(self.snake)
            else:
                self.snake.Move(eat = False)
            self.snake.CheckDeath()
        if self.snake.dead:
            self.state = 'end'

class Food:
    def __init__(self, snake = None, height = 20, width = 30):
        self.gameWidth = width
        self.gameHeight = height
        self.New(snake)
    def New(self, snake):
        self.pos = (0,0)
        self.SetRandomPos(snake)
    def SetRandomPos(self, snake):
        while True:
            self.pos = (random.randrange(0, self.gameWidth), 
                    random.randrange(0, self.gameHeight))
            if self.pos not in snake.body:
                break

class Snake:
    def __init__(self, height = 20, width = 30):
        self.gameWidth = width
        self.gameHeight = height
        self.New()
    def New(self):
        self.body = [(10, 10), (10, 11), (10, 12)]
        self.direction = (0,1)
        self.dead = False
    def Move(self, eat = False):
        if not self.dead:
            if not eat:
                self.body.pop(0)
            self.body.append(self.Next())
            self.CheckDeath()
    def Next(self):
        return (self.body[-1][0] + self.direction[0], self.body[-1][1] + self.direction[1])
    def CheckDeath(self):
        if not (0 <= self.body[-1][0] < self.gameWidth and 
                0 <= self.body[-1][1] < self.gameHeight):
            self.dead = True
        for p in self.body[:-1]:
            if p == self.body[-1]:
                self.dead = True
        return self.dead

