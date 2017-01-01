from Tkinter import *
import random
import time
import sys
#import SnakeAI as AI
#============================= Snake Game =====================================
class Evaluator:
    def __init__(self, height = 24, width = 32, ai = None, config = None):
        self.game = Game(height, width)
        if ai == None:
            print 'You need an AI for evaluate mode'
            sys.exit(1)
        else:
            self.ai = ai.SnakeAI(self.game)
        self.config = config
    def Evaluate(self):
        timeUse = 0
        moveUse = 0
        lastScore = 0
        scoreMove = 0
        while self.game.state == 'play':
            self.game.Update()
            startTime = time.time()
            d = self.ai.GetDirection(self.game)
            timeUse += time.time() - startTime
            self.game.ChangeDirection(d)
            moveUse += 1
            scoreMove += 1
            if self.game.score != lastScore:
                scoreMove = 0
                lastScore = self.game.score
                if self.game.score % 10 == 0:
                    print "Score: {:3}, Time used {:.3f}, Move used {:5}".format(self.game.score, timeUse, moveUse)
            if scoreMove > self.game.height*self.game.width*2:
                print "Too long not score, break out"
                break
        print "Final score: {:3}".format(self.game.score)

class Frame:
    def __init__(self, height = 480, width = 640, ai = None, speed = 40):
        self.pixelSize = 20
        self.root = Tk()
        self.root.bind("<Key>", self.KeyPress)
        self.gameWidth = width
        self.gameHeight = height+self.pixelSize*2
        self.scoreVar = StringVar()
        self.scoreVar.set("Score: 0")
        self.scoreBoard = Label(self.root, textvariable=self.scoreVar)
        self.scoreBoard.pack()
        self.canvas = Canvas(self.root, bg='black',height=height, width=width)
        self.canvas.pack()
        self.speed = speed
        self.game = Game(height/self.pixelSize, width/self.pixelSize)
        self.load = False
        if ai:
            self.ai = ai.SnakeAI(self.game)
    def Show(self):
        self.game.start()
        self.Refresh()
        self.root.mainloop()
    def Refresh(self):
        self.game.Update()
        if self.load:
            self.load = False
            self.LoadGame()
            self.game.Pause()
            if self.ai:
                self.game.ChangeDirection(self.ai.GetDirection(self.game))
        if self.game.state == 'play':
            self.scoreVar.set("Score: {}".format(self.game.score))
            self.canvas.delete('all')
            self.DrawGame()
            if self.ai:
                self.game.ChangeDirection(self.ai.GetDirection(self.game))
            self.root.after(int(1000/self.speed), self.Refresh)
        elif self.game.state == 'pause':
            self.canvas.delete('all')
            self.DrawGame()
            self.root.after(int(1000/self.speed), self.Refresh)
        elif self.game.state == 'end':
            self.canvas.delete('all')
            self.DrawGame()
            self.canvas.create_text(self.gameWidth/2,self.gameHeight/2,text="Game Over, press space to restart!", fill='white')
    def DrawGame(self):
        self.DrawRect(self.game.food.pos, 'blue')
        l = len(self.game.snake.body)
        for i in range(len(self.game.snake.body[:-1])):
            p = self.game.snake.body[i]
            c = '#'+'FF'+"{:02x}".format(255-(i*255/l))*2
            self.DrawRect(p, c)
        self.DrawRect(self.game.snake.body[-1], 'red')
    def DrawRect(self, pos, color):
        x = pos[0]
        y = pos[1]
        pSize = self.pixelSize
        self.canvas.create_rectangle(x*pSize, y*pSize, (x+1)*pSize, (y+1)*pSize, fill=color)
    def SaveGame(self):
        with open('sav', 'w') as f:
            f.write(str(self.game.score) + '\n')
            f.write(str(self.game.food.pos) + '\n')
            f.write(str(self.game.snake.body) + '\n')
            f.write(str(self.game.snake.direction) + '\n')
    def LoadGame(self):
        if self.ai and self.ai.Clear():
            self.ai.Clear()
        with open('sav', 'r') as f:
            self.game.score = eval(f.readline()[:-1])
            self.game.food.pos = eval(f.readline()[:-1])
            self.game.snake.body = eval(f.readline()[:-1])

    def KeyPress(self, event):
        sym = event.keysym

        if self.game.state == 'play' or self.game.state == 'pause':
            if sym in ['Up', 'Down', 'Left', 'Right']:
                if not self.useAI:
                    self.game.ChangeDirection(sym)
            elif sym == 's':
                print 'Game is saved'
                self.SaveGame()
            elif sym == 'l':
                print 'Game is loaded'
                self.load = True
            elif sym == 'p':
                self.game.Pause()
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
        self.score = 0
    def start(self):
        self.state = 'play'
        self.snake.New()
        self.food.New(self.snake)
        self.score = 0
    def ChangeDirection(self, direction):
        if direction not in ['Up', 'Down', 'Left', 'Right']:
            raise Exception("You need to pass 'Up', 'Down', 'Left' or 'Right' to the function!")
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
        if not self.snake.dead and self.state == 'play':
            if self.snake.Next() == self.food.pos:
                self.snake.Move(eat = True)
                self.food.SetRandomPos(self.snake)
                self.score += 1
            else:
                self.snake.Move(eat = False)
            self.snake.CheckDeath()
        if self.snake.dead:
            self.state = 'end'
    def Pause(self):
        if self.state == 'play':
            self.state = 'pause'
        elif self.state == 'pause':
            self.state = 'play'

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
            print "Out of the boundary"
            self.dead = True
        for p in self.body[:-1]:
            if p == self.body[-1]:
                print p, " Hit self"
                self.dead = True
                break
        return self.dead

