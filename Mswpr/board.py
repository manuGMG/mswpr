from random import shuffle
import pygame

class Board:
	'''
	MS Board Class
	
	BOMB  = -1
	EMPTY = 0
	'''
	def __init__(self, rows, cols, bombs):
		self.board = []
		self.cols = cols
		self.rows = rows
		self.bombs = bombs

	def generate(self):
		for x in range(self.rows*self.cols):
			self.board.append(-1) if x < self.bombs else self.board.append(0)
		shuffle(self.board)
		self.board = [self.board[i::self.rows] for i in range(self.rows)]
		for y in range(self.rows):
			for x in range(self.cols):
				if self.board[y][x] == -1:
					self.set_bomb(x, y)
		return self.board
	
	def set_bomb(self, x, y):
		bounds = [[x-1, y-1], [x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1], [x-1, y+1], [x-1, y]]
		for x in range(8):
			if (bounds[x][0] < 0) or (bounds[x][0] >= self.cols) or (bounds[x][1] < 0) or (bounds[x][1] >= self.rows):
				pass
			else:
				if self.board[bounds[x][1]][bounds[x][0]] != -1:
					self.board[bounds[x][1]][bounds[x][0]] += 1
	pass