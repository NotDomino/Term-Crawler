from __future__ import annotations
import curses.textpad as cr_text
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
	from .game import Game
	
class UI:
	def __init__(self, game: Game) -> None:
		self.game = game

		self.lastKeyInput = None
		
		self.log: List[Tuple[str, int]] = []
		self.addLog('You wake up in a dungeon... where am i?', self.game.attribs.cyan | self.game.attribs.bold)

	def OK(self, title, text) -> None:
		enterText = 'enter to continue >>'
		text = self.textWrap(text, self.game.width//4)

		width = len(text[0])
		if len(title) > width:
			width = len(title)
		if len(enterText) > width:
			width = len(enterText)
		height = len(text)
		width += 5
		height += 2

		x = self.game.width//2 - width//2
		y = self.game.height//2 - height//2
		
		while True:
			self.draw_box(x, y, width, height)
			self.print(x+width//2, y, title, self.game.attribs.standout, center_align=True)
			for i, item in enumerate(text):
				self.print(x+1, y+i+1, item)

			self.print(x+width//2+1, y+height, enterText, self.game.attribs.standout, True)

			self.game.term.stdscr.refresh()

	
	@staticmethod
	def textWrap(string: str, width: int) -> List[str]:
		"""Text wrapper"""
		return [string[i:i + width] for i in range(0, len(string), width)]
	
	def draw_box(self, x, y, width, height) -> None:
		# clear inside of rect area
		for xIter in range(width):
			for yIter in range(height):
				self.print(x+xIter, y+yIter, '.', self.game.attribs.clear)

		for xIter in range(width):
			self.print(x+xIter, y, '═')
			self.print(x+xIter, y+height, '═')

		for xIter in range(height):
			self.print(x, y+xIter, '║')
			self.print(x+width, y+xIter, '║')

		#replace 4 corners
		self.print(x, y, '╔')
		self.print(x+width, y, '╗')
		self.print(x, y+height, '╚')
		self.print(x+width, y+height, '╝')
	
	def drawBorder(self) -> None:
		"""draws the rectangular border"""
		cr_text.rectangle(
			self.game.term.stdscr, 
			self.game.y, self.game.x, 
			self.game.height, self.game.width
		)
	
	def print(
		self,
		x: int,
		y: int,
		text: str,
		attr = None,
		center_align: bool = False
	) -> None:
		"""Print stuff to the screen
		args:
			attr: eg: self.screen.attribs.yellow | self.screen.attribs.bold
			center_align: bool = False
		"""
		scr = self.game.term.stdscr

		if center_align:
			x -= len(text)//2
			
		if not attr:
			return scr.addstr(y, x, text)
		scr.addstr(y, x, text, attr)

	def printStats(self) -> None:
		"""Prints the players stats"""
		x = self.game.width + (self.game.term.width-self.game.width) //2

		playerStats = self.game.player.stats

		self.print(x, 0, "STATS", self.game.attribs.yellow | self.game.attribs.bold, True) # prints the STATS title

		for i in range(len(playerStats)):
			stat = playerStats[i]
			if type(stat) == tuple: # if the text has custom attributes assigned to it
				stat, attrib = stat
				self.print(x, i+2, stat, attrib, True)
				continue

			self.print(x, i+2, stat, self.game.attribs.yellow, True)
	
	def printDebug(self) -> None:
		self.print(2, 2, "DEBUG", self.game.attribs.magenta | self.game.attribs.bold)
		self.print(2, 3, f"Player XY: {self.game.player.x}|{self.game.player.y}")
		self.print(2, 4, f"camera XY: {self.game.map.x}|{self.game.map.y}")
		self.print(2, 5, f"Last key input: {self.lastKeyInput}")
		
	def addLog(self, text: str, attrib: int = None) -> None:
		"""Adds to the text log"""
		if not attrib:
			attrib = self.game.attribs.yellow

		self.log.append((text, attrib))
		
		# TODO: don't delete oldest logs, just print most recent logs
		# delete oldest logs
		while len(self.log) > (self.game.term.height - self.game.height) - 1:
			self.log.pop(0)
	
	def printLog(self) -> None:
		"""Prints the text log"""
		# TODO: add keybind to print all logs into a menu (v or L probably)
		# TODO: don't delete oldest logs, just print most recent logs
		for index, log in enumerate(self.log):
			self.print(0, self.game.height +index+1, log[0], log[1])

	def clearLog(self) -> None:
		"""Clears the whole text log"""
		self.log = []