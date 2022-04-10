"""Not really much point touching this file"""
from typing import NoReturn

from .game import Game

class Terminal:
	"""Custom terminal wrapper for Curses. Don't really recommend touching this class"""
	def __init__(
		self,
		stdscr
	) -> None:
	
		self.stdscr = stdscr
		self.height, self.width = self.dimensions # terminal dimensions
		self.screen = Game(
			self,
			0, 0,
			self.width-20, self.height-10	
		) # going to be a box that is inset by 4 on all sides


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

			self.screen.render()
			self.screen.handle()
			self.stdscr.refresh() # mandatory, leave it alone