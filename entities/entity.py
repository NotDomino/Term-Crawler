from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractclassmethod


from .InputManager import BasicMovement
if TYPE_CHECKING:
	from map import Map

class Types(Enum):
	"""Entity types"""
	FRIENDLY = auto()
	ENEMY = auto()
	PLAYER = auto()

class Entity(ABC):
	"""base class for any on-screen entities
	"""

	def __init__(
		self,
		map: Map,
		sprite: str,
		colour: Optional[int] = None
	) -> None:
		self.map = map
		self.char = sprite
		self.colour = colour
		self.x: int = 0
		self.y: int = 0
		self.type: Types = None

		self.maxHP = 10
		self.maxFP = 10
		self.hp = self.maxHP
		self.fp = self.maxFP
		self.dmg = 2
		self.block = True
		self.InputManager = BasicMovement(self)
	
	def die(self) -> None:
		"""Only run if the entity has died"""
		self.InputManager = None
		self.block = False
		self.char = 'x'
		self.map.game.addLog(f'entity died!', self.map.game.attribs.red | self.map.game.attribs.bold)
	
	def damage(self, hp: int) -> None:
		self.hp -= hp
		if self.hp <= 0:
			self.hp = 0
			self.die()
	
	def heal(self, hp: int) -> None:
		self.hp += hp
		if self.hp > self.maxHP:
			self.hp = self.maxHP

	def set_pos(
		self,
		x:int = None, 
		y:int = None
	) -> None:
		"""Sets the X and Y positions of an entity

		Args:
			x (int): X coordinate
			y (int): Y coordinate
		"""	
		if x:
			self.x = x
		if y:
			self.y = y
			
		if not x and not y:
			self.x, self.y = 0, 0
	
	def move(self, x: int, y: int):
		"""Moves the entity

		Args:
			x (int): only needs to be -1, 0, 1
			y (int): only needs to be -1, 0, 1
		"""
		ent = self.map.getEntityAtPos(self.x+x, self.y+y)
		if ent and ent.block and self != ent:

			return ent.interact(self)

		self.x += x
		self.y += y
	
	@abstractclassmethod
	def interact(self) -> None:
		raise NotImplementedError

	@property
	def isPlayer(self) -> bool:
		if self.type == Types.PLAYER:
			return True
		return False