from __future__ import annotations
import curses
import curses.textpad as cr_text
from typing import TYPE_CHECKING, List, NoReturn, Optional, Tuple

if TYPE_CHECKING:
	from entity import Entity
	from _curses import _CursesWindow

from attributes import Attributes
from player import Player
from npc import NPC


class Terminal:
	"""Custom terminal wrapper for Curses. Don't really recommend touching this class"""
	def __init__(
		self,
		stdscr: _CursesWindow
	) -> None:
		self.stdscr = stdscr
		self.height, self.width = self.dimensions # terminal dimensions
		self.screen = Screen(
			self,
			0, 0,
			self.width-4, self.height-5
		) # going to be a box that is inset by 4 on all sides

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
		"""Main loop"""
		while True:
			# TODO stick exception loop here, not done yet because i want it to crash :)
			self.stdscr.clear() # mandatory, leave it alone
			self.screen.refresh() # edit the refresh loop of THIS ONE
			self.stdscr.refresh() # mandatory, leave it alone


class Screen:
	"""The Screen is anything inside that large rectangle (if you run the file)
	"""

	def __init__(
		self,
		mainWindow: Terminal,
		x, y,
		width, height
	):
		self.attribs = Attributes() # colours initialization
		self.term = mainWindow #stdscr, not "really" necessary (as of right now) 
		self.x = x
		self.y = y

		# "screen" = visible rectangle
		self.width = width # -2 because we want the "screen" to be inset by 2
		self.height = height # -2 because we want the "screen" to be inset by 2
		self.entities: List[Entity] = [
			NPC(self, '#', 10, 10),
			Player(self),
		]
		self.log: List[Tuple[str, int]] = []

	def addlog(self, text: str, attrib: int = None) -> None:
		"""Adds to the text log"""
		self.log.append((text, attrib))
		while len(self.log) > self.term.height - self.height - 1:
			self.log.pop(0)
	
	def print_log(self) -> None:
		"""Prints the text log"""
		for index, log in enumerate(self.log):
			self.print(0, self.height+index+1, log[0], log[1])

	def refresh(self) -> None:
		"""Refreshes this portion of the code (only for use in Terminal)"""
		cr_text.rectangle( # draws the border (rectangle)
			self.term.stdscr, 
			self.y, self.x, 
			self.height, self.width
		)
		self.print_log()
		for entity in self.entities:
			entity.update()
				
	def print(self, x: int, y: int, words: str, attr = None) -> None:
		"""Print shit to the screen"""
		if not attr:
			return self.term.stdscr.addstr(y, x, words)
		return self.term.stdscr.addstr(y, x, words, attr)
	
	def getkey(self) -> str:
		"""gets key input"""
		return self.term.stdscr.getkey()

	def getch(self) -> int:
		"""gets key input"""
		return self.term.stdscr.getch()

	def whatsInThisPosition(self, x: int, y: int) -> Optional[Entity]:
		for entity in self.entities:
			if entity.x == x and entity.y == y:
				return entity
		return None
			
	@property
	def center(self) -> Tuple[int, int]:
		"""Returns center XY coordinates of Screen

		Returns:
			Tuple[int, int]: (x, y)
		"""
		return (self.width//2, self.height//2)


if __name__ == '__main__':
	curses.wrapper(Terminal)
