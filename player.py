from __future__ import annotations

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
	from main import Screen


class Player:
	"""Player class
	"""
	def __init__(
		self,
		screen: Screen,
		sprite: str = '#',
	):
		self.screen = screen
		self.x: int = None,
		self.y: int = None
		self.set_pos()
		self.sprite = sprite
	
	def set_pos(
		self,
		x:Optional[int] = None, 
		y:Optional[int] = None
	) -> None:
		"""Sets the player's X and Y positions

		Args:
			x (int, optional): X coordinate. Defaults to None.
			y (int, optional): Y coordinate. Defaults to None.
		"""	
		if x:
			self.x = x
		if y:
			self.y = y
			
		if not x and not y:
			self.x, self.y = self.screen.center
		self.pos_check()

	def handle_movement(self) -> None:
		"""Handles player movement"""

		key = self.screen.getKey()
		match key: # probably a better way of doing this, however i am lazy
			case "KEY_UP" | "w":
				self.y -= 1
			case "KEY_DOWN" | "s":
				self.y += 1
			case "KEY_LEFT" | "a":
				self.x -= 1
			case "KEY_RIGHT" | "d":
				self.x += 1

		# makes sure the positions are all ok
		self.pos_check()

	def pos_check(self) -> None:
		"""Checks the position of the player, makes adjustments if necessary"""
		# TODO screen scrolling ( so below code won't be necessary )
		# keeps player within screen borders
		if self.x <= self.screen.x:
			self.x = self.screen.x + 1
			
		if self.x >= self.screen.width:
			self.x = self.screen.width -1
			
		if self.y <= self.screen.y:
			self.y = self.screen.y +1

		if self.y >= self.screen.height:
			self.y = self.screen.height -1

	def draw(self) -> None:
		self.screen.print(self.x, self.y, self.sprite)

	def refresh(self) -> None:
		"""Refreshes the player"""
		self.draw()
		self.handle_movement()