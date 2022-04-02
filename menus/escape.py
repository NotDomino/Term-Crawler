from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from window.screen import Screen

class Escape:
	def __init__(self, screen: Screen) -> None:
		self.screen = screen
		self.opts = {
			"resume": self.back, # returns to the game
			"options": self.optionsMenu,
			"exit": exit
		}
		self.index = 0
		self.offset = 3 # the offset for how far away from the "menu" text the options are

	def run(self):
		
		width, height = self.screen.center
		self.screen.print(width, height-self.offset, 'Menu')
		for i, option in enumerate(self.opts):
			if self.index != i:
				self.screen.print(width, height+i, option) # unselected option
				continue
			key = option
			self.screen.print(width, height+i, option, self.screen.attribs.reverse) # selected option

		ch = self.screen.getch()
		match ch:
			case 27: #escape key
				self.screen.menu = None

			case 259 | 119: # up arrow | w
				self.__scrollUp()
				
			case 258 | 115: # down arrow | s
				self.__scrollDown()
			case 10: # enter key
				self.opts[ key ]()

	def __scrollUp(self) -> None:
		self.index -= 1
		if self.index < 0:
			self.index = len(self.opts.keys()) -1

	def __scrollDown(self) -> None:
		self.index += 1
		if self.index > len(self.opts.keys())-1:
			self.index = 0

	def back(self):
		self.screen.menu = None

	def optionsMenu(self):
		return self.screen.loadMenu("options")