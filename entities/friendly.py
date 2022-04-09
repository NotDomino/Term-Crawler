from __future__ import annotations
import random
from typing import TYPE_CHECKING

from .entity import Entity, Types

if TYPE_CHECKING:
	from map import Map

class Friendly(Entity):
	"""Friendly NPC class"""

	def __init__(
		self,
		map: Map,
		sprite: str,
		x: int,
		y: int,
		dialogue_opts: list = [
			"Why did you just touch me?",
			"Ew, go away!"
		]
	):
		super().__init__(map, sprite, map.game.attribs.green)
		self.x = x
		self.y = y
		self.type = Types.FRIENDLY
		self.dialogue_opts = dialogue_opts
	
	def interact(self, entity) -> None:
		if entity.type == Types.PLAYER:
			self.map.game.UI.OK("Entity Interaction", random.choice(self.dialogue_opts))