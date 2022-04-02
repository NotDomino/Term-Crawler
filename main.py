from __future__ import annotations
import curses
import curses.textpad as cr_text
from typing import TYPE_CHECKING, NoReturn, Tuple

if TYPE_CHECKING:
	from _curses import _CursesWindow

from colours import Colours
from player import Player
from friendly import NPC


class Terminal:
	"""Custom terminal wrapper for Curses. Don't really recommend touching this class"""
	def __init__(
		self,
		stdscr: _CursesWindow
	) -> None:
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
		"""Main game loop"""
		while True:
			# TODO stick exception loop here, not done yet because i want it to crash :)
			self.stdscr.clear() # mandatory, leave it alone
			self.screen.refresh() # edit the refresh loop of THIS ONE
			self.stdscr.refresh() # mandatory, leave it alone


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
		self.entityList = [
			Player(self),
			NPC(self)
		]
	
	@property
	def center(self) -> Tuple[int, int]:
		"""Returns center XY coordinates of Screen

		Returns:
			Tuple[int, int]: (x, y)
		"""
		return (self.width//2, self.height//2)

	def refresh(self) -> None:
		"""Refreshes this portion of the code (only for use in Terminal)"""
		cr_text.rectangle( # draws the border (rectangle)
			self.term, 
			self.y, self.x, 
			self.height, self.width
		)
		for entity in self.entityList:
			entity.refresh()
				
	def print(self, x: int, y: int, words: str) -> None:
		"""Print shit to the screen"""
		self.term.addstr(y, x, words)
	
	def getKey(self) -> str:
		return self.term.getkey()


if __name__ == '__main__':
	curses.wrapper(Terminal)
