from __future__ import annotations
import curses
import curses.textpad as cr_text
from typing import TYPE_CHECKING, NoReturn
if TYPE_CHECKING:
	from _curses import _CursesWindow

from colours import Colours

class Player:
	"""Player class
	"""
	def __init__(
		self,
		screen: Screen,
		x: int,
		y: int,
		sprite: str = '#',
	):
		self.screen = screen
		self.x, self.y = x, y
		self.sprite = sprite
	
	def handle_movement(self, key: str) -> None:
		"""Handles player movement

		Args:
			key (str): key (received through getkey())
		"""
		match key:
			case "KEY_UP" | "w":
				self.y -= 1
			case "KEY_DOWN" | "s":
				self.y += 1
			case "KEY_LEFT" | "a":
				self.x -= 1
			case "KEY_RIGHT" | "d":
				self.x += 1

		# TODO screen scrolling ( so below code won't be necessary )
		# keeps player within screen borders
		if self.x <= self.screen.x:
			self.x += 1
		if self.x >= self.screen.width:
			self.x -= 1
		if self.y <= self.screen.y:
			self.y += 1
		if self.y >= self.screen.height:
			self.y -= 1

class Terminal:
	"""Custom terminal wrapper for Curses, don't hand this down to classes, hand the Screen class"""
	def __init__(
		self,
		stdscr: _CursesWindow
	):
		self.stdscr = stdscr
		self.height, self.width = stdscr.getmaxyx() # terminal dimensions
		self.screen = Screen(
			self.stdscr,
			2, 2,
			self.width-2, self.height-2
		) # going to be a box that is inset by 2 on all sides

		# big ups initializer (couldn't live without you)
		self.__loop()

	@property
	def dimensions(self):
		"""returns terminal dimensions

		Returns:
			tuple: (height, width)
		"""
		return self.stdscr.getmaxyx()

	def __loop(self) -> NoReturn:
		
		while True:
			self.stdscr.clear()
			self.screen.refresh()
			self.stdscr.refresh()

class Screen:
	"""Hand this class down to other classes (eg. Player class)"""
	def __init__(
		self,
		mainWindow: _CursesWindow,
		x, y,
		width, height
	):
		self.colours = Colours() # colours initialization
		self.term = mainWindow #stdscr, not "really" necessary (as of right now) 
		self.x = x
		self.y = y

		# "screen" = visible rectangle
		self.width = width - 2 # -2 because we want the "screen" to be inset by 2
		self.height = height - 2 # -2 because we want the "screen" to be inset by 2
		self.player = Player(self, self.x+1, self.y+1)
	
	def refresh(self) -> None:
		player = self.player
		cr_text.rectangle(
			self.term, 
			self.y, self.x, 
			self.height, self.width
		)

		self.screenPrint(player.x, player.y, player.sprite)
		self.player.handle_movement(self.term.getkey())		

	def screenPrint(self, x: int, y: int, words: str) -> None:
		"""Print shit to the screen"""
		self.term.addstr(y, x, words)

if __name__ == '__main__':
	curses.wrapper(Terminal)
