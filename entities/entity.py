from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING, Optional

class Types(Enum):
	"""Entity types"""
	FRIENDLY = auto()
	ENEMY = auto()
	PLAYER = auto()

class Entity:
	"""class for any on-screen entities"""
	def __init__(
		self,
		colour: Optional[int],
		x: int,
		y: int,
		char: str = '@',
		name: str = 'Entity'
	) -> None:
		self.colour = colour
		self.x: int = x
		self.y: int = y
		self.char = char
		self.type: Types = None # entity type (from Types class above)

		self.name = name
		self.maxHP = 10
		self.maxFP = 10
		self.hp = self.maxHP
		self.fp = self.maxFP
		self.dmg = 2

		self.block = True
	
	def die(self) -> None:
		"""Entity died"""
		# attribs = self.map.game.attribs
		self.InputManager = None
		self.block = False
		self.char = 'x'
		# self.colour = attribs.red
		# self.map.game.UI.addLog(f'{self.name} died!', attribs.red | attribs.bold)
	
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
		self.x += x
		self.y += y
	
	def set_pos(self, x:int, y:int) -> None:
		"""Sets the X and Y positions of an entity"""
		if x:
			self.x = x
		if y:
			self.y = y
	
	@property
	def isPlayer(self) -> bool:
		if self.type == Types.PLAYER:
			return True
		return False