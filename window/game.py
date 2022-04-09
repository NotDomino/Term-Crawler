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

		self.menus = {
			"main": None, # needs implementing
			"options": Options, 
			"inventory": None, # needs implementing
		}

		self.menu: Menu = None
		self.debug = False

	# --------------------------------------------------------
	# MENUS
	# --------------------------------------------------------

	def loadMenu(self, name: str) -> None:
		"""loads provided menu"""
		self.menu = self.menus[name](self)

	# --------------------------------------------------------
	# MAIN
	# --------------------------------------------------------

	def refresh(self) -> None:
		"""Refreshes the screen"""
		self.UI.drawBorder()
		
		if self.menu:  
			return self.menu.render()

		self.UI.printStats()
		self.UI.printLog() # prints the log underneath the border
		
		

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