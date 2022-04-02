from __future__ import annotations
from typing import TYPE_CHECKING

from entities.entity import Entity

if TYPE_CHECKING:
	from window.screen import Screen

class NPC(Entity):
	"""NPC class"""

	def __init__(
		self,
		screen: Screen,
		sprite: str,
		x: int,
		y: int
	):
		super().__init__(screen, sprite, screen.attribs.green)
		self.x = x
		self.y = y
	
	def handle_movement(self) -> None:
		"""Not a current desire to have the NPC move... maybe in the future we could have a wandering one"""
		self.inside_border_check() # makes sure entity doesn't leave borders
	
	def interact(self) -> None:
		self.screen.addlog("Why did you just touch me?")