from dataclasses import dataclass
import math
from typing import List, Tuple


def lineGen(coord1, coord2, girth):
	ret = []
	x0, y0 = coord1
	x1, y1 = coord2
	for _  in range(girth):
		ret = ret + list(set(bresenham(x0, y0, x1, y1)) - set(ret))
		ret = ret + list(set(bresenham(x0+_, y0, x1+_, y1)) - set(ret))
		ret = ret + list(set(bresenham(x0-_, y0, x1-_, y1)) - set(ret))
		ret = ret + list(set(bresenham(x0, y0+_, x1, y1+_)) - set(ret))
		ret = ret + list(set(bresenham(x0, y0-_, x1, y1-_)) - set(ret))
	return ret


def bresenham(x0, y0, x1, y1):
	deltax = x1-x0
	dxsign = int(abs(deltax)/deltax)
	deltay = y1-y0
	dysign = int(abs(deltay)/deltay)
	deltaerr = abs(deltay/deltax)
	error = 0
	y = y0
	for x in range(x0, x1, dxsign):
		yield x, y
		error = error + deltaerr
		while error >= 0.5:
			y += dysign
			error -= 1
	yield x1, y1

print(lineGen((0, 0), (5, 5), 2))

def square_coords(
	xPos: int,
	yPos: int,
	width: int,
	height: int
) -> List[Tuple[int, int]]:
	"""Returns a list of coordinates that represent a quadrilateral at a given x, y pos"""
	
	toReturn = []
	for xIter in range(width):
		for yIter in range(height):
			toReturn.append((xPos+xIter, yPos+yIter))
			toReturn.append((xPos+xIter*2+1, yPos+yIter))
	return toReturn

@dataclass
class Circle:
	xPos: int
	yPos: int
	radius: int

	def coords(self):
		"""Returns a list of coordinates that represent a circle of a given radius as given x, y pos"""
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
		coord = self.coords()
		return coord[len(coord)//2]