from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Tuple

from entities import Enemy, Friendly, Player
from entities.floor import Floor
from geometry import Circle, lineGen
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
			Friendly(self, '#', 10, 9),
			Enemy(self, '@', 20, 20),
		]
		self.floors: List[Floor] = []
		
		circle1 = Circle(0, 0, 5)
		circle2 = Circle(10, 30, 5)
		line = list(lineGen(circle1.center, circle2.center, girth=3))
		toFloor = circle1.coords() + circle2.coords() + line

		for coord in toFloor:
			exists = False
			for floor in self.floors:
				if floor.x == coord[0] and floor.y == coord[1]:
					exists = True
					break
			if not exists:
				self.floors.append(Floor(coord[0], coord[1]))
		
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

		for x in range(self.game.width-1):
			for y in range(self.game.height-1):
				self.game.UI.print(x+1, y+1, '█')

		# render floors 
		for floor in self.floors:
			self.place(floor.x, floor.y, floor.char, self.game.attribs.clear)
		
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
		# TODO write wall renderer (based on above image)

		self.place(self.player.x, self.player.y, self.player.char, self.player.colour)
		self.game.term.stdscr.move(0, 0) # leave this here
		
		# Debug menu
		if self.game.debug:
			self.game.UI.printDebug()

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
	
	def getGroundAtPos(self, x: int, y: int) -> Optional[Floor]: 
		for floor in self.floors:
			if floor.x == x and floor.y == y:
				return floor
	@property
	def center(self) -> Tuple[int, int]:
		"""Returns center XY coordinates of the map

		Returns:
			Tuple[int, int]: (x, y)
		"""
		return (self.width//2, self.height//2)