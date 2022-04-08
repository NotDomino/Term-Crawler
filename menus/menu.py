from __future__ import annotations
from typing import TYPE_CHECKING, Dict
from abc import ABC, abstractclassmethod

if TYPE_CHECKING:
	from window.game import Game

class Menu(ABC):
	"""Baseclass menu"""
	def __init__(
		self,
		screen: Game,
		opts: Dict[str, function],
		title: str
	) -> None:
		self.screen = screen
		self.opts: dict = opts
		self.index: int = 0
		self.title = title
		
	def __scrollUp(self) -> None:
		self.index -= 1
		if self.index < 0:
			self.index = len(self.opts.keys()) -1

	def __scrollDown(self) -> None:
		self.index += 1
		if self.index > len(self.opts.keys()) -1:
			self.index = 0
	
	def getKeyIn(self) -> None:
		ch = self.screen.getch()
		match ch:
			case 27: #escape key goes back to game
				self.screen.menu = None

			case 259 | 119: # up arrow | w
				self.__scrollUp()
				
			case 258 | 115: # down arrow | s
				self.__scrollDown()

			case 10: # enter key
				self.opts[ list(self.opts.keys())[self.index] ]()
	
	@abstractclassmethod
	def run() -> None:
		raise NotImplementedError