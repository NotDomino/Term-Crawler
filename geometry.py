from dataclasses import dataclass, field
import math
from typing import List, Tuple


def lineGen(coord1, coord2, girth):
	ret = [coord1, coord2]

	for x in range(abs(coord1[0] - coord2[0])):
		for xThickness in range(1-girth if girth > 0 else 0, 1+girth):
			for yThickness in range(1-girth if girth > 0 else 0, 1+girth):
				ret.append((
					(x + xThickness),
					(round((coord1[1]-coord2[1])/(coord1[0]-coord2[0]) * (x-coord1[0]) + coord1[1]) + yThickness)
				))
	return ret

print(lineGen((0, 0), (10, 0), 1))

@dataclass
class Rectangle:
	x: int
	y: int
	width: int
	height: int
	coords: List[Tuple[int, int]] = field(init=False)
	

	def __post_init__(self) -> None:
		self.coords =  self.genCoords()
	
	def genCoords(self) -> List[Tuple[int, int]]:
		"""Generates a list of coordinates that represent a quadrilateral at a given x, y pos"""
		toReturn = []
		for xIter in range(self.width):
			for yIter in range(self.height):
				toReturn.append((self.x+xIter*2, self.y+yIter))
				toReturn.append(((self.x+xIter*2)+1, self.y+yIter))
		return toReturn

	@property
	def center(self) -> Tuple[int, int]:
		"""Returns the center of the rectangle"""
		return ((self.x + self.width), (self.y + self.height//2))

@dataclass
class Circle:
	xPos: int
	yPos: int
	radius: int
	coords: List[Tuple[int, int]] = field(init=False)
	
	def __post_init__(self) -> None:
		self.coords = self.genCoords()

	def genCoords(self):
		"""generates a list of coordinates that represent a circle of a given radius as given x, y pos"""
		toReturn = []
		hChars = (2 * self.radius)
		
		for y in range(0, 2*self.radius):
			for x in range(0, int(hChars)):
				dist = math.sqrt(
					(x - self.radius) * (x - self.radius) +
					(y - self.radius) * (y - self.radius))
				if (dist < self.radius):
					toReturn.append((int(x+self.xPos)*2, int(y+self.yPos)))
					toReturn.append((int(x+self.xPos)*2+1, int(y+self.yPos)))
		return toReturn
	
	@property
	def center(self) -> Tuple[int, int]:
		return self.coords[len(self.coords)//2]