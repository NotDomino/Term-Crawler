from __future__ import annotations
from typing import TYPE_CHECKING
import random

from entities.entity import Entity

if TYPE_CHECKING:
	from window.screen import Screen

class Enemy(Entity):
	def __init__(
		self,
		screen: Screen,
		sprite: str,
		x: int,
		y: int
	) -> None:
		super().__init__(screen, sprite, screen.attribs.red)
		self.x = x
		self.y = y

		self.damage = 2

	def interact(self) -> None:
		self.screen.addLog("Harder", self.screen.attribs.red)
	
	def handle_movement(self) -> None:
		# TODO: implement a way for enemy to find player (probably going to use TCOD library, haven't decided yet) 

		if random.randint(0, 1) == 0:
			toX = random.randint(-1, 1)
			ent = self.screen.getEntityAtPos(self.x+toX, self.y)
			if ent and ent.block:
				if ent.isPlayer:
					ent.damage(2)
				return
			self.move(toX, 0)
			
		else:
			toY = random.randint(-1, 1)
			ent = self.screen.getEntityAtPos(self.x, self.y+toY)
			if ent and ent.block:
				if ent.isPlayer:
					ent.damage(2)
				return
			self.move(0, toY)

		self.inside_border_check() # makes sure entity doesn't leave borders