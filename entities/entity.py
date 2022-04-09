from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING, Optional

from .actor import Actor

from .inputManager import BasicMovement
if TYPE_CHECKING:
	from map import Map

class Types(Enum):
	"""Entity types"""
	FRIENDLY = auto()
	ENEMY = auto()
	PLAYER = auto()

class Entity(Actor):
	"""class for any on-screen entities"""
	def __init__(
		self,
		map: Map,
		sprite: str,
		colour: Optional[int] = None,
		name: str = 'Entity'
	) -> None:
		super().__init__(block=True, char=sprite, colour=colour)
		self.map = map
		self.type: Types = None # entity type (from Types class above)

		self.name = name
		self.maxHP = 10
		self.maxFP = 10
		self.hp = self.maxHP
		self.fp = self.maxFP
		self.dmg = 2
		self.InputManager = None# BasicMovement(self)
	
	def die(self) -> None:
		"""Entity died"""
		attribs = self.map.game.attribs
		self.InputManager = None
		self.block = False
		self.char = 'x'
		self.colour = attribs.red
		self.map.game.UI.addLog(f'{self.name} died!', attribs.red | attribs.bold)
	
	def damage(self, hp: int) -> None:
		self.hp -= hp
		if self.hp <= 0:
			self.hp = 0
			self.die()
	
	def heal(self, hp: int) -> None:
		self.hp += hp
		if self.hp > self.maxHP:
			self.hp = self.maxHP

	def move(self, x: int, y: int):
		"""Moves the entity

		Args:
			x (int): only needs to be -1, 0, 1
			y (int): only needs to be -1, 0, 1
		"""
		ent = self.map.getEntityAtPos(self.x+x, self.y+y)
		if ent and ent.block and self != ent:
			return ent.interact(self)
			
		ground = self.map.getGroundAtPos(self.x+x, self.y+y)
		if ground:
			self.x += x
			self.y += y
	
	@property
	def isPlayer(self) -> bool:
		if self.type == Types.PLAYER:
			return True
		return False