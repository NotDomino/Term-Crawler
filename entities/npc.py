from __future__ import annotations
import random
from typing import TYPE_CHECKING

from .entity import Entity, Types

if TYPE_CHECKING:
	from window.screen import Screen

class Friendly(Entity):
	"""Friendly NPC class"""

	def __init__(
		self,
		screen: Screen,
		sprite: str,
		x: int,
		y: int,
		dialogue_opts: list = [
			"Why did you just touch me?",
			"Ew, go away!"
		]
	):
		super().__init__(screen, sprite, screen.attribs.green)
		self.x = x
		self.y = y
		self.dialogue_opts = dialogue_opts
	
	def interact(self, entity) -> None:
		if entity.type == Types.PLAYER:
			self.screen.addLog(random.choice(self.dialogue_opts))