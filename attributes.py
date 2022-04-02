import curses

class Attributes:
	def __init__(self):
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
		curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
		
		# colours
		self.default = curses.color_pair(1)
		self.red = curses.color_pair(2)
		self.green = curses.color_pair(3)
		self.blue = curses.color_pair(4)
		self.yellow = curses.color_pair(5)
		self.magenta = curses.color_pair(6)
		self.cyan = curses.color_pair(7)

		# attribs
		self.blink = curses.A_BLINK
		self.bold = curses.A_BOLD
		self.dim = curses.A_DIM
		self.reverse = curses.A_REVERSE
		self.standout = curses.A_STANDOUT
		self.underline = curses.A_UNDERLINE

