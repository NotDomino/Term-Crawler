from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from main import Screen

class NPC:
	def __init__(
		self,
		screen: Screen,
		x:int,
		y: int
	):
		self.screen = screen
		self.x = x
		self.y = y
	
	def draw(self) -> None:
		self.screen.print(self.x, self.y, self.sprite)
	
	def refresh(self) -> None:
		#Just gonna stand here for now
		self.draw()