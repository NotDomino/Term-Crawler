"""Not really much point touching this file"""
from typing import NoReturn

from window.screen import Screen

class Terminal:
	"""Custom terminal wrapper for Curses. Don't really recommend touching this class"""
	def __init__(
		self,
		stdscr
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