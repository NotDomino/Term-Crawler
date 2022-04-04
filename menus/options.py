from __future__ import annotations
from typing import TYPE_CHECKING
import curses.textpad as cr_text

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
		self.screen.print(
			width, height-offset,
			self.title,
			center_align=True
		) # prints the title text
		
		for i, option in enumerate(self.opts):
			if self.index != i:
				self.screen.print(
					width, height+i,
					option,
					center_align=True
				) # unselected option
				continue
			self.screen.print(
				width, height+i,
				option, self.screen.attribs.standout,
				center_align = True
			) # selected option

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
		"""Help menu"""
		self.screen.term.stdscr.clear() # mandatory, leave it alone
		self.screen.drawBorder()
		bold = self.screen.attribs.bold
		xoff = self.screen.center[0]# offset everything here by these values

		self.screen.print(xoff, 1, "HELP MENU", bold, True)
		self.screen.print(xoff//2, 3, "Gameplay", bold, True)

		# prints gameplay part of menus
		gameplay = [
			"W/↑ | UP ARROW",
			"A/← | LEFT",
			"S/↓ | DOWN",
			"D/→ | RIGHT",
			"esc | options menu"
		]
		for i in range(len(gameplay)):
			self.screen.print((xoff//2)-6, i+4, gameplay[i])
		
		self.screen.print(xoff, 3, "Menus", bold, True)
		self.screen.print(xoff-6, 4, "W/↑ | scroll up")
		self.screen.print(xoff-6, 5, "S/↓ | scroll down", bold)

		self.screen.print(self.screen.x+1, self.screen.height-1, "Press any key to continue...")
		self.screen.getch() # to pause on the help screen