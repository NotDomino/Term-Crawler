from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import actions

if TYPE_CHECKING:
	from .window.game import Game


class EventHandler:
	def __init__(self, game: Game) -> None:
		self.game = game

	def keyDown(self) -> Optional[actions.Action]:
		ch = self.game.getch()
		self.game.UI.lastKeyInput = ch # for debugging purposes

		match ch:
			# case 10: # enter key
				# pass

			case 27: #escape key
				return actions.EscapeAction()
			
			case 259 | 119: # up arrow | w
				return actions.MovementAction(0, -1)
				
			case 258 | 115: # down arrow | s
				return actions.MovementAction(0, 1)
				
			case 260 | 97: # left arrow | a
				return actions.MovementAction(-1, 0)
				
			case 261 | 100: # right arrow | d
				return actions.MovementAction(1, 0)
			
			case __:
				return None

class OptionsMenuHandler:
	def __init__(self, game: Game) -> None:
		self.game = game
	
	def keyDown(self) -> Optional[int]:
		ch = self.game.getch()
		self.game.UI.lastKeyInput = ch # for debugging purposes

		match ch:
			case 10: # enter key
				return self.game.menu.enter()

			case 27: #escape key
				self.game.menu = None
				self.game.eventHandler = EventHandler(self.game)
				return
			
			case 259 | 119: # up arrow | w
				return self.game.menu.scrollUp()
				
			case 258 | 115: # down arrow | s
				return self.game.menu.scrollDown()
			
			case __:
				return None