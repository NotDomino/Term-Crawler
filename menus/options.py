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
				option, self.screen.attribs.reverse,
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
		self.screen.term.stdscr.clear() # mandatory, leave it alone
		self.screen.draw_border()
		bold = self.screen.attribs.bold
		xoff, yoff = self.screen.center[0], 1 # offset everything here by these values
		self.screen.print(xoff, yoff, "HELP MENU", bold, True)
		
		self.screen.print(xoff, yoff+2, "Gameplay", bold, True)
		self.screen.print(xoff-6, yoff+3, "W/↑ | UP ARROW")
		self.screen.print(xoff-6, yoff+4, "A/← | LEFT")
		self.screen.print(xoff-6, yoff+5, "S/↓ | DOWN")
		self.screen.print(xoff-6, yoff+6, "D/→ | RIGHT")
		self.screen.print(xoff-6, yoff+7, "esc | options menu")

		self.screen.print(xoff, yoff+9, "Menus", bold, True)
		self.screen.print(xoff-6, yoff+10, "W/↑ | scroll up")
		self.screen.print(xoff-6, yoff+11, "S/↓ | scroll down", bold)

		self.screen.print(self.screen.x+1, self.screen.height-1, "Press any key to continue...")
		self.screen.getch() # to pause on the help screen