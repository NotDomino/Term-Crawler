from __future__ import annotations
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .entity import Entity

# TODO: implement a way for enemy to pathfind player (Likely A* pathfinding)
class BasicMovement:
	def __init__(self, entity: Entity) -> None:
		self.entity = entity

	def handle(self) -> None:
		toX = random.randint(-1, 1)
		toY = random.randint(-1, 1)
		self.entity.move(toX, 0)
		self.entity.move(0, toY)
			

class PlayerInput:
	def __init__(self, entity: Entity) -> None:
		self.entity = entity

	def handle(self) -> None:
		"""Handles player movement"""
		ch = self.entity.map.game.getch()
		match ch: # probably a better way of doing this, however i am lazy
			case 27: #escape key
				self.entity.map.game.loadMenu("options") # loads the escape menu
			
			case 259 | 119: # up arrow | w
				self.entity.move(0, -1)
				
			case 258 | 115: # down arrow | s
				self.entity.move(0, 1)
				
			case 260 | 97: # left arrow | a
				self.entity.move(-1, 0)
				
			case 261 | 100: # right arrow | d
				self.entity.move(1, 0)