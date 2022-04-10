from __future__ import annotations
from random import randint
from typing import TYPE_CHECKING, List, Optional, Tuple
import numpy as np

from entities import Enemy, Friendly, Entity
from entities.tile import Tile
if TYPE_CHECKING:
	from window.game import Game

class Map:
	def __init__(self, game: Game, width: int, height: int) -> None:
		self.game = game
		self.width = width
		self.height = height
		self.centeredEntity = None
		
		self.floors: List[Tile] = []
		self.walls: List[Tile] = []

		self.entities: List[Entity] = []

	def center_on(self, entity: Entity) -> None:
		self.centeredEntity = entity
		self.reCenter()
	
	def reCenter(self) -> None:
		self.x = -self.centeredEntity.x + self.game.width//2
		self.y = -self.centeredEntity.y + self.game.height//2

	def refresh(self) -> None:
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

		# render walls
		for wall in self.walls:
			self.render(wall.x, wall.y, wall.char)
				
		# render entities
		for entity in self.entities:
			self.render(entity.x, entity.y, entity.char, entity.colour)
			
		"""
		█ << these are to be used too
			╔═╦═╗
			║ ║ ║
			╠═╬═╣
			║ ║	║
			╚═╩═╝
		"""
		# TODO write wall renderer (based on above image)

		self.render(self.game.player.x, self.game.player.y, self.game.player.char, self.game.player.colour)
		self.game.term.stdscr.move(0, 0) # leave this here
		
		# Debug menu
		if self.game.debug:
			self.game.UI.printDebug()

	def render(self, x: int, y: int, text: str, attr = None) -> None:
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
	
	def getTileAtPos(self, x: int, y: int) -> Optional[Tile]: 
		for tile in self.floors:
			if tile.x == x and tile.y == y:
				return tile

	@property
	def center(self) -> Tuple[int, int]:
		"""Returns center XY coordinates of the map

		Returns:
			Tuple[int, int]: (x, y)
		"""
		return (self.width//2, self.height//2)