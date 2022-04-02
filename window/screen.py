from __future__ import annotations
from typing import List, Optional, Tuple, TYPE_CHECKING
import curses.textpad as cr_text

from window.attributes import Attributes
from entities import NPC, Player, Enemy
from menus.escape import Escape
if TYPE_CHECKING:
	from main import Terminal
	from entities import Entity

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
			Enemy(self, '@', 20, 20),
			Player(self),
		]
		self.log: List[Tuple[str, int]] = []

		self.menus = {
			"main": None, # needs implementing
			"escape": Escape, # needs implementing
			"inventory": None, # needs implementing
			"options": None, # needs implementing
		}
		self.menu = None

	# --------------------------------------------------------

	# MENUS
	# --------------------------------------------------------
	def loadMenu(self, name: str) -> None:
		"""loads provided menu"""
		if not (name in self.menus.keys()):
			return
		self.menu = self.menus[name](self)
	
	# --------------------------------------------------------
	
	# LOGS
	# --------------------------------------------------------
	def addlog(self, text: str, attrib: int = None) -> None:
		"""Adds to the text log"""
		if not attrib:
			attrib = self.attribs.yellow
		self.log.append((text, attrib))
		while len(self.log) > self.term.height - self.height - 1:
			self.log.pop(0)
	
	def print_log(self) -> None:
		"""Prints the text log"""
		for index, log in enumerate(self.log):
			self.print(0, self.height+index+1, log[0], log[1])

	# --------------------------------------------------------

	# MAIN
	# --------------------------------------------------------

	def refresh(self) -> None:
		"""Refreshes the screen"""
		cr_text.rectangle( # draws the border (rectangle)
			self.term.stdscr, 
			self.y, self.x, 
			self.height, self.width
		)
		if self.menu:  
			return self.menu.run()
		self.print_log() # prints the log underneath the rectangle

		# TODO separate input back out of the player class, causing some more than mild issues
		for entity in self.entities:
			entity.update() # updates each entity
	
	# --------------------------------------------------------

	# KEY INPUTS
	# --------------------------------------------------------
	def getkey(self) -> str:
		"""gets key input"""
		return self.term.stdscr.getkey()

	def getch(self) -> int:
		"""gets key input"""
		return self.term.stdscr.getch()
	
	# --------------------------------------------------------
	# HELPFUL STUFF
	# --------------------------------------------------------

	def print(self, x: int, y: int, words: str, attr = None) -> None:
		"""Print shit to the screen"""
		if not attr:
			return self.term.stdscr.addstr(y, x, words)
		return self.term.stdscr.addstr(y, x, words, attr)

	def entityInPos(self, x: int, y: int) -> Optional[Entity]:
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
