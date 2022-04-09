from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING


from .attributes import Attributes
from .UI import UI
from map import Map
from menus import Options

if TYPE_CHECKING:
	from menus import Menu
	from main import Terminal

class Game:
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
		
		self.map = Map(self)
		self.UI = UI(self)

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
			self.UI.print(0, self.height+index+1, log[0], log[1])

	def clearLog(self) -> None:
		"""Clears the whole text log"""
		self.log = []

	# --------------------------------------------------------
	# MAIN
	# --------------------------------------------------------

	def refresh(self) -> None:
		"""Refreshes the screen"""
		self.UI.drawBorder()
		
		if self.menu:  
			return self.menu.render()

		self.UI.printStats()
		self.printLog() # prints the log underneath the border
		
		self.map.render()

	# --------------------------------------------------------
	# HELPFUL STUFF
	# --------------------------------------------------------

	def getkey(self) -> str:
		"""gets key input"""
		return self.term.stdscr.getkey()

	def getch(self) -> int:
		"""gets key input"""
		return self.term.stdscr.getch()
	
	@property
	def center(self) -> Tuple[int, int]:
		"""Returns center XY coordinates of the screen

		Returns:
			Tuple[int, int]: (x, y)
		"""
		return (self.width//2, self.height//2)