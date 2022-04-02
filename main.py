import curses
from terminal import Terminal

if __name__ == '__main__':
	curses.wrapper(Terminal)
