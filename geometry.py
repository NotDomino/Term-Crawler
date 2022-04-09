import math
from typing import List, Tuple


def lineConnector(
	xy: Tuple[int, int],
	xy2: Tuple[int, int],
	girth
) -> List[Tuple[int, int]]:
	toReturn = [
		(xy[0], xy[1]), # beginning pos
		(xy2[0], xy2[1]) # end pos
	]
	m = (xy[1]-xy2[1])/(xy[0]-xy2[0])
	
	for x in range(abs(xy[0] - xy2[0])):
		for xThickness in range(1-girth if girth > 0 else 0, 1+girth):
			for yThickness in range(1-girth if girth > 0 else 0, 1+girth):
				toReturn.append((x + xThickness, round(m * (x-xy[0]) + xy[1]) + yThickness))
	return toReturn

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

def circle_coords(
	xPos: int,
	yPos: int,
	radius: int
):
	"""Returns a list of coordinates that represent a circle of a given radius as given x, y pos"""
	toReturn = []
	hUnitsPerChar = 1
	hChars = (2 * radius) / hUnitsPerChar
	
	for j in range(0, 2*radius):
		y = j + 0.5
		for i in range(0, int(hChars)):
			x = (i + 0.5) * hUnitsPerChar
			dist = math.sqrt(
				(x - radius) * (x - radius) +
				(y - radius) * (y - radius))
			if (dist < radius):
				toReturn.append((int(x+xPos)*2, int(y+yPos)))
				toReturn.append((int(x+xPos)*2+1, int(y+yPos)))
	return toReturn