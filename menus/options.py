from __future__ import annotations
from typing import TYPE_CHECKING

from .menu import Menu
from inputHandlers import EventHandler, OptionsMenuHandler

if TYPE_CHECKING:
	from window.game import Game

enabled = lambda x: '☒' if x else '☐'

class Options(Menu):
	def __init__(
		self,
		game: Game
	) -> None:
		super().__init__(game,
			opts = {
				"resume": self.back, # returns to the game
				"help": self.help,
				"save": self.save,
				"load": self.load,
				f"{enabled(game.debug)} Debug": self.toggleDebug,
				"exit": exit,
			},
			title = "Options"
		)

	def render(self):
		offset = 3 # the offset for how far away from the "menu" text the options are
		width, height = self.game.center
		self.game.UI.print(
			width, height-offset,
			self.title,
			center_align=True
		) # prints the title text
		
		for i, option in enumerate(self.opts):
			if self.index != i:
				self.game.UI.print(
					width, height+i,
					option,
					center_align=True
				) # unselected option
				continue
			self.game.UI.print(
				width, height+i,
				option, self.game.attribs.standout,
				center_align = True
			) # selected option

	def save(self) -> None:
		# TODO: implement save function
		# these todos are gonna be here for a while
		self.back()

	def load(self) -> None:
		# TODO: implement load function
		# these todos are gonna be here for a while
		self.back()

	def enter(self) -> None:
		self.opts[ list(self.opts.keys())[self.index] ]()

	def back(self):
		self.game.menu = None
		self.game.eventHandler = EventHandler(self.game)

	def help(self):
		"""Help menu"""
		self.game.term.stdscr.clear() # mandatory, leave it alone
		self.game.UI.drawBorder()
		bold = self.game.attribs.bold
		xoff = self.game.center[0]# offset everything here by these values

		self.game.UI.print(xoff, 1, "HELP MENU", bold, True)
		self.game.UI.print(xoff//2, 3, "Gameplay", bold, True)

		# prints gameplay part of menus
		gameplay = [
			"W/↑ | UP ARROW",
			"A/← | LEFT",
			"S/↓ | DOWN",
			"D/→ | RIGHT",
			"esc | options menu"
		]
		for i in range(len(gameplay)):
			self.game.UI.print((xoff//2)-6, i+4, gameplay[i])
		
		self.game.UI.print(xoff, 3, "Menus", bold, True)
		self.game.UI.print(xoff-6, 4, "W/↑ | scroll up")
		self.game.UI.print(xoff-6, 5, "S/↓ | scroll down", bold)

		self.game.UI.print(self.game.x+1, self.game.height-1, "Press any key to continue...")
		self.game.getch() # to pause on the help screen
	
	def toggleDebug(self) -> None:
		index = list(self.opts.keys()).index(f'{enabled(self.game.debug)} Debug')
		
		self.game.debug = not self.game.debug
		
		self.game.menu = Options(self.game)
		self.game.menu.index = index

		self.game.UI.addLog('Debug mode toggled!', self.game.attribs.magenta)
		self.game.UI.addLog(f"State: {self.game.debug}", self.game.attribs.magenta)