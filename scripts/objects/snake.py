import pygame
from random import randint
from objects.segment import Segment


class Snake():
	def __init__(self, grid_origin, grid_size, unit_size, game_sprites):
		# Sprites
		self.sprites = {
			"straight": game_sprites[0],
			"curved": game_sprites[1],
			"head": game_sprites[2],
			"tail": game_sprites[3]
		}

		grid_units = (int(grid_size[0] / unit_size), int(grid_size[1] / unit_size))

		self.lives = 2
		self.size = 1


		# Head direction & position
		head_pos = [randint(2, grid_units[0] - 3), randint(2, grid_units[1] - 3)]

		front = randint(0, 3)
		self.head_direction = [front, 0]

		if front < 2:
			self.head_direction[1] = front + 2
		else:
			self.head_direction[1] = front - 2

		self.segments = [Segment(head_pos, self.head_direction)]
		self.addSegment()
		self.addSegment()


	def update(self, input, slow_frame):

		if pygame.K_RIGHT in input["KEYSDOWN"]:
			self.head_direction = [0, 2]
		elif pygame.K_DOWN in input["KEYSDOWN"]:
			self.head_direction = [1, 3]
		elif pygame.K_LEFT in input["KEYSDOWN"]:
			self.head_direction = [2, 0]
		elif pygame.K_UP in input["KEYSDOWN"]:
			self.head_direction = [3, 1]

		if slow_frame:
			if self.head_direction[1] != self.segments[0].direction[0]:
				self.segments[0].direction = self.head_direction

			self.movement(input)


	def addSegment(self):
		self.size += 1
		self.segments.append(Segment(self.getUnitBehind(), self.segments[-1].direction))


	def getUnitBehind(self, index=-1):
		x = y = 0

		if self.segments[index].direction[0] == 0:
			x = -1
		elif self.segments[index].direction[0] == 2:
			x = 1
		elif self.segments[index].direction[0] == 1:
			y = -1
		else:
			y = 1

		return [ self.segments[index].pos[0] + x, self.segments[index].pos[1] + y ]


	def movement(self, input):
		# Update head
		x = y = 0

		if self.segments[0].direction[1] == 0:
			x = -1
		elif self.segments[0].direction[1] == 2:
			x = 1
		elif self.segments[0].direction[1] == 1:
			y = -1
		else:
			y = 1

		self.segments[0].pos[0] += x
		self.segments[0].pos[1] += y

		# Update body
		oppositeDirections = [2, 3, 0, 1]

		for i in range(1, len(self.segments)):
			self.segments[i].pos = self.getUnitBehind(i - 1)

			self.segments[i].direction[0] = oppositeDirections[self.segments[i].direction[1]]
			self.segments[i].direction[1] = oppositeDirections[self.segments[i - 1].direction[0]]

		# Update tail
		self.segments[-1].direction[1] = oppositeDirections[self.segments[-2].direction[0]]
		self.segments[-1].direction[0] = oppositeDirections[self.segments[-1].direction[0]]


	def setSnakeSprites(self):
		for i in range(len(self.segments)):
			# print(f"{self.segments[i].pos} | {self.segments[i].direction}")
			self.setSegmentRotation(i)

			if i == 0:
				self.segments[0].sprite = "head"

			elif i == len(self.segments) - 1:
				self.segments[-1].sprite = "tail"

			else:
				if abs(self.segments[i].direction[0] - self.segments[i].direction[1]) != 2:
					self.segments[i].sprite = "curved"
				else:
					self.segments[i].sprite = "straight"
		# print()


	def setSegmentRotation(self, i):
		direction_difference = abs(self.segments[i].direction[0] - self.segments[i].direction[1])
		direction_sum = self.segments[i].direction[0] + self.segments[i].direction[1]

		rotation = 0

		if direction_difference == 3:
			rotation = 1

		elif direction_difference == 2:
			rotation = range(0, 4)[- self.segments[i].direction[0]]

		elif direction_difference == 1:
			if direction_sum == 1:
				rotation = 0
			if direction_sum == 3:
				rotation = 3
			if direction_sum == 5:
				rotation = 2

		self.segments[i].rotation = rotation

	def getOppositeDirection(self, direction):
		return [2, 3, 0, 1][direction]
