from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractclassmethod

if TYPE_CHECKING:
	from window.screen import Screen

class Entity(ABC):
	"""base class for any on-screen entities
	"""

	def __init__(
		self,
		screen: Screen,
		sprite: str,
		colour: Optional[int] = None
	) -> None:
		self.screen = screen
		self.sprite = sprite
		self.colour = colour
		self.x: int = 0
		self.y: int = 0
		
		self.block = True
		self.isNPC = True
	
	@property
	def isPlayer(self) -> bool:
		return not self.isNPC

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
			self.x, self.y = self.screen.center
		self.inside_border_check()
	
	def inside_border_check(self) -> None:
		"""Checks the position of the entity, makes adjustments if necessary"""
		# TODO screen scrolling ( so below code won't be necessary )
		# keeps entities within screen borders
		if self.x <= self.screen.x:
			self.x = self.screen.x + 1
			
		if self.x >= self.screen.width:
			self.x = self.screen.width -1
			
		if self.y <= self.screen.y:
			self.y = self.screen.y +1

		if self.y >= self.screen.height:
			self.y = self.screen.height -1

	def draw(self) -> None:
		if not self.colour:
			self.screen.print(self.x, self.y, self.sprite)
		else:
			self.screen.print(self.x, self.y, self.sprite, self.colour)

	def update(self):
		self.draw()
		self.screen.term.stdscr.move(0, 0) # leave this here
		self.handle_movement()
	
	def move(self, x: int, y: int):
		"""Moves the entity

		Args:
			x (int): only needs to be -1, 0, 1
			y (int): only needs to be -1, 0, 1
		"""
		self.x += x
		self.y += y

		self.inside_border_check()

	@abstractclassmethod
	def handle_movement(self) -> None:
		"""Handles movement"""
		raise NotImplementedError
	
	@abstractclassmethod
	def interact(self) -> None:
		"""Handles interaction with this entity"""
		raise NotImplementedError