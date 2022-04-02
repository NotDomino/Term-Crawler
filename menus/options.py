from __future__ import annotations
from typing import TYPE_CHECKING

from .menu import Menu

if TYPE_CHECKING:
	from window.screen import Screen

class Options(Menu):
	def __init__(
		self,
		screen: Screen
	) -> None:
		super().__init__(screen,
			opts = {
				"resume": self.back, # returns to the game
				"help": self.help,
				"save": self.save,
				"load": self.load,
				"exit": exit,
			},
			title = "Options"
		) 

	def run(self):
		offset = 3 # the offset for how far away from the "menu" text the options are
		width, height = self.screen.center
		self.screen.print(width, height-offset, self.title) # prints the title text
		
		for i, option in enumerate(self.opts):
			if self.index != i:
				self.screen.print(width, height+i, option) # unselected option
				continue
			self.screen.print(width, height+i, option, self.screen.attribs.reverse) # selected option

		self.getKeyIn()

	def save(self) -> None:
		# TODO implement save function
		self.back()

	def load(self) -> None:
		# TODO implement load function
		self.back()

	def back(self):
		self.screen.menu = None

	def help(self):
		# TODO implement help section
		self.back()