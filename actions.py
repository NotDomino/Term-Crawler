from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
	from .entities.entity import Entity
	from .window.game import Game


class Action:
	def perform(self, game: Game, entity: Entity) -> None:
		"""Perform this action with the objects needed to determine its scope"""
		raise NotImplementedError()


class EscapeAction(Action):
	def perform(self, game: Game, entity: Entity) -> None:
		game.loadMenu("options") # loads the escape menu


class MovementAction(Action):
	def __init__(self, dx: int, dy: int):
		super().__init__()

		self.dx = dx
		self.dy = dy

	def perform(self, game: Game, entity: Entity) -> None:
		dx = entity.x + self.dx
		dy = entity.y + self.dy
		
		if not game.map.getTileAtPos(dx, dy):
			return  # Destination is blocked by a tile.

		entity.move(self.dx, self.dy)
