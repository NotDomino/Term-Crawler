from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Tuple

from entities import Enemy, Friendly, Player
if TYPE_CHECKING:
	from entities import Entity
	from window.game import Game

class Map:
	def __init__(self, game: Game) -> None:
		self.game = game
		self.width = 100
		self.height = 100

		self.entities: List[Entity] = [
			Friendly(self, '#', 1, 10),
			Enemy(self, '@', 20, 20),
			Player(self), 
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
		# adjust camera first before rendering entities
		xMargin = self.game.width//2 - (self.centeredEntity.x + self.x)
		yMargin = self.game.height//2 - (self.centeredEntity.y + self.y)		
		if yMargin > 5:
			self.y += 1
		if yMargin < -5:
			self.y -= 1
		if xMargin > 5:
			self.x += 1
		if xMargin < -5:
			self.x -= 1

		# render entities
		for entity in self.entities:
			if entity.x + self.x >= self.game.width:
				continue
			if entity.x + self.x <= 0:
				continue
			if entity.y + self.y >= self.game.height:
				continue
			if entity.y + self.y <= 0:
				continue
			self.game.print(
				entity.x + self.x,
				entity.y + self.y,
				entity.char, entity.colour
			)

		self.game.term.stdscr.move(0, 0) # leave this here
		
		self.player.InputManager.handle()
		

	def getEntityAtPos(self, x: int, y: int) -> Optional[Entity]:
		"""Checks if an entity is in the given position"""
		for entity in self.entities:
			if entity.x == x and entity.y == y:
				return entity
		return None
	
	@property
	def player(self) -> Player:
		for entity in self.entities:
			if not entity.isPlayer:
				continue
			return entity

	@property
	def center(self) -> Tuple[int, int]:
		"""Returns center XY coordinates of the map

		Returns:
			Tuple[int, int]: (x, y)
		"""
		return (self.width//2, self.height//2)