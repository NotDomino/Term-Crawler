from dataclasses import dataclass, field
from math import ceil, radians, cos, sin
from typing import List, Tuple
import numpy

def diagonalLine(
	coord1: Tuple[int, int],
	coord2: Tuple[int, int],
	girth: int
) -> List[Tuple[int, int]]:
	"""Generates a diagonal line given two coordinates and a girth"""
	ret = [coord1, coord2] # initial return values
	
	if girth <= 0: girth = 1 # so there's actual girth 

	x0, y0, = coord1
	x1, y1 = coord2

	try:
		m = (y0-y1)/(x0-x1)
	except:
		m = 100 # catches division by zero
	
	if x0 == x1: r1, r2 = 0, 1
	elif x0 < x1: r1, r2 = x0, x1
	else: r1, r2 = x1, x0

	for i in range(r1, r2):#range of smallest to biggest
		for xThickness in range(1-girth, 1+girth):
			for yThickness in range(1-girth, 1+girth):
				for grad in range(ceil(abs(m))) if abs(m) >= 1 else range(1):#makes an extra block upwards per gradient run
					if ( # if line will go past destination, stop
						(round(m * (i-x0) + y0) + yThickness-grad) < y1
						and (round(m * (i-x0) + y0) + yThickness-grad) < y0
					):
						break
					
					ret.append(((i + xThickness), (round(m * (i-x0) + y0) + yThickness-grad)))

	return numpy.array(ret, dtype='i, i')


class Rectangle:
	"""Generates a Rectangle in given coordinates"""
	def __init__(self, x, y, width, height) -> None:
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	
	@property
	def center(self) -> Tuple[int, int]:
		"""Returns the center of the rectangle"""
		return ((self.x + self.width//2), (self.y + self.height//2))
	
	@property
	def inner(self) -> numpy.ndarray:
		"""Generates a list of coordinates that represent a quadrilateral at a given x, y pos"""
		toReturn = []
		for xIter in range(self.width):
			for yIter in range(self.height):
				toReturn.append((self.x+xIter*2, self.y+yIter))
				toReturn.append(((self.x+xIter*2)+1, self.y+yIter))
		return numpy.array(toReturn, dtype='i, i')

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
		return numpy.array(newcoords, dtype='i, i')

	@property
	def center(self) -> Tuple[int, int]:
		return (self.xPos, self.yPos)