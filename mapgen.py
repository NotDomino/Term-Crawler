import random
from typing import List, Tuple
from entities import Entity
from entities.tile import Tile
from geometry import Rectangle, diagonalLine
import numpy as np
from map import Map

def generateMap(game, player: Entity) -> Map:
	map = Map(game, 100, 100)

	rooms: List[Rectangle] = []
	coordList: List[Tuple[int, int]] = []

	for _ in range(5): # max rooms
		room_width, room_height = random.randint(2, 10), random.randint(2, 10)

		x = random.randint(0, map.width - room_width - 1)
		y = random.randint(0, map.height - room_height - 1)
		room = Rectangle(x, y, room_width, room_height)

		if len(rooms) == 0:
			player.set_pos(room.x, room.y)
			map.center_on(player)
		else:
			coordList.append(diagonalLine(rooms[-1].center, room.center, 1))

		rooms.append(room)
		coordList.append(room.inner)


	coordList = mergeLists(*coordList)
	for coord in coordList:
		x, y = coord
		map.floors.append(Tile(x, y))

	# holy mother of inefficiency 
	for floor in map.floors:
		# corners
		if not map.getTileAtPos(floor.x-1, floor.y-1): # top left corner
			map.walls.append(Tile(floor.x-1, floor.y-1))
		if not map.getTileAtPos(floor.x-1, floor.y+1): # bottom left corner
			map.walls.append(Tile(floor.x-1, floor.y+1))
		if not map.getTileAtPos(floor.x+1, floor.y-1): # top right
			map.walls.append(Tile(floor.x+1, floor.y-1))
		if not map.getTileAtPos(floor.x+1, floor.y+1): # bottom right
			map.walls.append(Tile(floor.x+1, floor.y+1))
		
		# adjacent
		if not map.getTileAtPos(floor.x, floor.y-1): # above
			map.walls.append(Tile(floor.x, floor.y-1))
		if not map.getTileAtPos(floor.x, floor.y+1): # below
			map.walls.append(Tile(floor.x, floor.y+1))
		if not map.getTileAtPos(floor.x+1, floor.y): # to the left:
			map.walls.append(Tile(floor.x+1, floor.y))
		if not map.getTileAtPos(floor.x-1, floor.y): # to the right
			map.walls.append(Tile(floor.x-1, floor.y))
	return map


def mergeLists(*args) -> np.ndarray:
	"""Merges tupled lists, deleting any duplicates"""
	return np.unique(np.concatenate(args, 0)) 