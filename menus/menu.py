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
		self.game = screen
		self.opts: dict = opts
		self.index: int = 0
		self.title = title
		
	def scrollUp(self) -> None:
		self.index -= 1
		if self.index < 0:
			self.index = len(self.opts.keys()) -1

	def scrollDown(self) -> None:
		self.index += 1
		if self.index > len(self.opts.keys()) -1:
			self.index = 0
	
	@abstractclassmethod
	def render() -> None:
		raise NotImplementedError