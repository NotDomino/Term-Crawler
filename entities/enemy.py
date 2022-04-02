from __future__ import annotations
from typing import TYPE_CHECKING

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
	
	def interact(self) -> None:
		self.screen.addlog("Harder", self.screen.attribs.red)
	
	def handle_movement(self) -> None:
		self.inside_border_check() # makes sure entity doesn't leave borders