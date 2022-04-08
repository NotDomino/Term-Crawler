from __future__ import annotations
from typing import List, Optional, Tuple, TYPE_CHECKING
import curses.textpad as cr_text

from entities.entity import Types

from .attributes import Attributes
from entities import Friendly, Player, Enemy, Entity
from menus import Options

if TYPE_CHECKING:
	from menus import Menu
	from main import Terminal

class Screen:
	"""The Screen is anything inside that large rectangle (if you run the file)
	"""

	def __init__(
		self,
		terminal: Terminal,
		x, y,
		width, height
	) -> None:
		self.attribs = Attributes() # colours initialization
		self.term = terminal
		self.x = x
		self.y = y

		# "screen" = visible rectangle
		self.width = width
		self.height = height
		
		self.entities: List[Entity] = [
			Player(self), # Player should always be first in the 
			Friendly(self, '#', 10, 10),
			Enemy(self, '@', 20, 20),
		]

		# TODO: map class
		self.walls = [] # not yet implemented
		
		self.log: List[Tuple[str, int]] = []
		self.addLog('You wake up in a dungeon... where am i?', self.attribs.cyan | self.attribs.bold)
		self.menus = {
			"main": None, # needs implementing
			"options": Options, 
			"inventory": None, # needs implementing
		}

		self.menu: Menu = None

	# --------------------------------------------------------
	# MENUS
	# --------------------------------------------------------

	def loadMenu(self, name: str) -> None:
		"""loads provided menu"""
		self.menu = self.menus[name](self)
	
	# --------------------------------------------------------
	# LOGS
	# --------------------------------------------------------
	
	def addLog(self, text: str, attrib: int = None) -> None:
		"""Adds to the text log"""
		if not attrib:
			attrib = self.attribs.yellow

		self.log.append((text, attrib))
		
		# TODO: don't delete oldest logs, just print most recent logs
		# delete oldest logs
		while len(self.log) > (self.term.height - self.height) - 1:
			self.log.pop(0)
	
	def printLog(self) -> None:
		"""Prints the text log"""
		# TODO: add keybind to print all logs into a menu (v or L probably)
		# TODO: don't delete oldest logs, just print most recent logs
		for index, log in enumerate(self.log):
			self.print(0, self.height+index+1, log[0], log[1])

	def clearLog(self) -> None:
		"""Clears the whole text log"""
		self.log = []

	# --------------------------------------------------------
	# MAIN
	# --------------------------------------------------------

	def refresh(self) -> None:
		"""Refreshes the screen"""
		self.drawBorder()
		if self.menu:  
			return self.menu.run()

		self.printStats()
		self.printLog() # prints the log underneath the border

		for entity in self.entities:
			if entity.isPlayer:
				player = entity # mild optimization
				continue
			entity.update() # updates each entity

		player.update()
		
	# --------------------------------------------------------
	# HELPFUL STUFF
	# --------------------------------------------------------

	def getkey(self) -> str:
		"""gets key input"""
		return self.term.stdscr.getkey()

	def getch(self) -> int:
		"""gets key input"""
		return self.term.stdscr.getch()

	def drawBorder(self) -> None:
		"""draws the rectangular border"""
		cr_text.rectangle(
			self.term.stdscr, 
			self.y, self.x, 
			self.height, self.width
		)
		
	def printStats(self) -> None:
		"""Prints the players stats"""
		x = self.width + (self.term.width-self.width) //2

		playerStats = self.player.stats

		self.print(x, 0, "STATS", self.attribs.yellow | self.attribs.bold, True) # prints the STATS title

		for i in range(len(playerStats)):
			stat = playerStats[i]
			if type(stat) == tuple: # if the text has custom attributes assigned to it
				stat, attrib = stat
				self.print(x, i+2, stat, attrib, True)
				continue

			self.print(x, i+2, stat, self.attribs.yellow, True)

	def print(self, x: int, y: int, text: str, attr = None, center_align: bool = False) -> None:
		"""Print stuff to the screen
		args:
			attr: eg: self.screen.attribs.yellow | self.screen.attribs.bold
		"""
		if center_align:
			x -= len(text)//2

		if not attr:
			return self.term.stdscr.addstr(y, x, text)
		self.term.stdscr.addstr(y, x, text, attr)

	def getEntityAtPos(self, x: int, y: int) -> Optional[Entity]:
		"""Checks if an entity is in the given position"""
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

	@property
	def player(self) -> Player:
		for entity in self.entities:
			if not entity.isPlayer:
				continue
			return entity