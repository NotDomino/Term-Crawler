from dataclasses import dataclass, field
from math import radians, cos, sin
from typing import List, Tuple


def lineGen(coord1, coord2, girth):
	ret = [coord1, coord2]

	for x in ((range(coord1[0], coord2[0])) if coord1[0] < coord2[0] else range(coord2[0], coord1[0])):
		for xThickness in range(1-girth if girth > 0 else 0, 1+girth):
			for yThickness in range(1-girth if girth > 0 else 0, 1+girth):
				ret.append((
					(x + xThickness),
					(round((coord1[1]-coord2[1])/(coord1[0]-coord2[0]) * (x-coord1[0]) + coord1[1]) + yThickness)
				))
	return ret

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

	@staticmethod
	def circleCoords():
		return [( (round(cos(radians(q)), 10)) , (round(sin(radians(q)), 10)) ) for q in range(0, 361)]#passing a third value into this range can play with circle thickness (try numbers like 3 and 6)

	def genCoords(self):
		newcoords = []
		for x, y in self.circleCoords():
			for siz in range(0, self.radius):
				coord = (round(self.xPos+x*siz), round(self.yPos+y*siz))
				if not (coord in newcoords): newcoords.append(coord) 
		return newcoords

	@property
	def center(self) -> Tuple[int, int]:
		return (self.xPos, self.yPos)