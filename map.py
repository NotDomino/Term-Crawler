from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Tuple
import math

from entities import Enemy, Friendly, Player
if TYPE_CHECKING:
	from entities import Entity
	from window.game import Game

class Map:
	def __init__(self, game: Game) -> None:
		self.game = game
		self.width = 100
		self.height = 100

		self.player = Player(self)
		self.entities: List[Entity] = [
			Friendly(self, '#', 1, 10),
			Enemy(self, '@', 20, 20),
		]
		self.centeredEntity = None
		self.center_on(self.player)

	def center_on(self, entity: Entity) -> None:
		self.centeredEntity = entity
		self.reCenter()
	
	def reCenter(self) -> None:
		self.x = -self.centeredEntity.x + self.game.width//2
		self.y = -self.centeredEntity.y + self.game.height//2

	def render(self) -> None:
		# adjust camera on y axis
		yMargin = self.game.height//2 - (self.centeredEntity.y + self.y)		
		if yMargin > 5:
			self.y += 1
		if yMargin < -5:
			self.y -= 1
		# adjust camera on x axis
		xMargin = self.game.width//2 - (self.centeredEntity.x + self.x)
		if xMargin > 5:
			self.x += 1
		if xMargin < -5:
			self.x -= 1

		# render walls n shit here
		# for coord in self.circle_coords(0, 0, 10):
		# 	self.place(coord[0], coord[1], '█')

		# render entities
		for entity in self.entities:
			if entity.InputManager:
				entity.InputManager.handle()
			self.place(entity.x, entity.y, entity.char, entity.colour)
			
		"""
		█ << these are to be used too
			╔═╦═╗
			║ ║ ║
			╠═╬═╣
			║ ║	║
			╚═╩═╝
		"""
		# TODO write wall generator (based on above image)

		self.place(self.player.x, self.player.y, self.player.char, self.player.colour)
		self.game.term.stdscr.move(0, 0) # leave this here
		
		self.player.InputManager.handle()
		
	def place(self, x: int, y: int, text: str, attr = None) -> None:
		"""Place stuff on the screen
		args:
			attr: eg: self.screen.attribs.yellow | self.screen.attribs.bold
			center_align: bool = False
		"""
		# if the entity isn't on the screen, don't render it
		if x + self.x >= self.game.width:
			return
		if x + self.x <= 0:
			return
		if y + self.y >= self.game.height:
			return
		if y + self.y <= 0:
			return
		self.game.UI.print(
			x + self.x,
			y + self.y,
			text, attr
		)
		
	def getEntityAtPos(self, x: int, y: int) -> Optional[Entity]:
		"""Checks if an entity is in the given position"""
		for entity in self.entities:
			if entity.x == x and entity.y == y:
				return entity
		return None

	@property
	def center(self) -> Tuple[int, int]:
		"""Returns center XY coordinates of the map

		Returns:
			Tuple[int, int]: (x, y)
		"""
		return (self.width//2, self.height//2)