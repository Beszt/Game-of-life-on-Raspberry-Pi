import time
import random

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont

class cCell:
	def __init__(self, x = 0, y = 0, live = False):
		self.x = x
		self.y = y
		self.live = live
		
		self.neighbours = 0

class cBoard():
	def __init__(self, xMax = 84, yMax = 48, randomize = True, percentLive = 10):
		self.xMax = xMax
		self.yMax = yMax
		self.randomize = randomize
		self.percentLive = percentLive
		
		liveCells = []
		
		self.cells = []
		self.size = self.xMax * self.yMax
		
		if (randomize == True):
			ic = 0
			while (ic <= (int(((self.size) / 100)*self.percentLive) - 1)):
				rand = random.randint(0,self.size)
				if not (rand in liveCells):
					liveCells.append(rand)
					ic += 1
			ic = 0
			for i in range(0,self.yMax):
				for i2 in range(0,self.xMax):
					if (ic in liveCells):
						self.cells.append(cCell(i2,i,True))
					else:
						self.cells.append(cCell(i2,i,False))
					ic += 1
				
class cGame():
	def countNeighboors(self):
		for i in range(0,self.board.size):
			self.board.cells[i].neighbours = 0;
			if (((i - self.board.xMax - 1) >= 0) and ((self.board.cells[i].y - self.board.cells[i - self.board.xMax - 1].y) == 1)):
				if (self.board.cells[i - self.board.xMax - 1].live == True):
					self.board.cells[i].neighbours += 1;
			if ((i - self.board.xMax) >= 0):
				if (self.board.cells[i - self.board.xMax].live == True):
					self.board.cells[i].neighbours += 1;
			if (((i - self.board.xMax + 1) >= 0) and ((self.board.cells[i].y - self.board.cells[i - self.board.xMax + 1].y) == 1)):
				if (self.board.cells[i - self.board.xMax + 1].live == True):
					self.board.cells[i].neighbours += 1;
			if (((i - 1) >= 0) and ((self.board.cells[i].y - self.board.cells[i - 1].y) == 0)):
				if (self.board.cells[i - 1].live == True):
					self.board.cells[i].neighbours += 1;
			if (((i + 1) < self.board.size) and ((self.board.cells[i].y - self.board.cells[i + 1].y) == 0)):
				if (self.board.cells[i + 1].live == True):
					self.board.cells[i].neighbours += 1;
			if (((i + self.board.xMax - 1) < self.board.size) and ((self.board.cells[i + self.board.xMax - 1].y - self.board.cells[i].y) == 1)):
				if (self.board.cells[i + self.board.xMax - 1].live == True):
					self.board.cells[i].neighbours += 1;
			if ((i + self.board.xMax) < self.board.size):
				if (self.board.cells[i + self.board.xMax].live == True):
					self.board.cells[i].neighbours += 1;
			if (((i + self.board.xMax + 1) < self.board.size) and ((self.board.cells[i + self.board.xMax + 1].y - self.board.cells[i].y) == 1)):
				if (self.board.cells[i + self.board.xMax + 1].live == True):
					self.board.cells[i].neighbours += 1;
			
	def calcLive(self):
		for i in range(0,self.board.size):
			if ((self.board.cells[i].live == True) and (self.board.cells[i].neighbours < 2)):
				self.board.cells[i].live = False
			if ((self.board.cells[i].live == True) and (self.board.cells[i].neighbours > 3)):
				self.board.cells[i].live = False
			if ((self.board.cells[i].live == False) and (self.board.cells[i].neighbours == 3)):
				self.board.cells[i].live = True
	
	def countLive(self):
		cL = 0;
		for i in range(0,self.board.size):
			if (self.board.cells[i].live == True):
				cL += 1
		return cL
		
	def start(self):
		iGen = 0
		while (True):
			print(self.countLive())
			self.countNeighboors()
			self.calcLive()
			iGen += 1

	def __init__(self, xMax = 84, yMax = 48, randomize = True, percentLive = 10):
	    self.board = cBoard(xMax, yMax, randomize, percentLive)

DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

disp.begin(contrast=32)

disp.clear()
disp.display()

font = ImageFont.load_default()

image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
draw = ImageDraw.Draw(image)

draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

game = cGame(84,48,True,12)
for i in range(game.board.size):
    if (game.board.cells[i].live == True):
        draw.point([(game.board.cells[i].x,game.board.cells[i].y)],fill=0)
disp.image(image)
disp.display()
iGen = maxGens = 0
while True:
    game.countNeighboors()
    game.calcLive()
    iGen += 1
    if ((game.countLive() < 220) and (iGen >= 20)):
        if (maxGens < iGen):
            maxGens = iGen;
            print('Nowy rekord generacji: ' + str(maxGens));
        iGen = 0;
        game = cGame(84,48,True,12)
	
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	
    for i in range(game.board.size):
        if (game.board.cells[i].live == True):
            draw.point([(game.board.cells[i].x,game.board.cells[i].y)],fill=0)
    disp.image(image)
    disp.display()