from __future__ import annotations
from typing import TYPE_CHECKING

from .entity import Entity, Types

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
		self.type = Types.ENEMY
		self.set_pos(x, y)
	
	def interact(self, entity: Entity):
		"""How another entity interacts with this enemy"""
		if entity.type == Types.FRIENDLY:
			return
		self.screen.addLog(f"enemy was damaged for {entity.dmg} hp!")
		self.damage(entity.dmg)