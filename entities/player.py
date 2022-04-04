from __future__ import annotations
from typing import TYPE_CHECKING, List

from entities.entity import Entity

if TYPE_CHECKING:
	from window.screen import Screen


class Player(Entity):
	"""Player class"""
	def __init__(
		self,
		screen: Screen,
		sprite: str = '#',
	):
		super().__init__(screen, sprite)
		self.set_pos()
		self.isNPC = False
		self.maxHP = 10
		self.maxFP = 10
		self.hp = self.maxHP
		self.fp = self.maxFP
	
	def update(self):
		"""Custom update method for player"""
		self.draw()
		self.screen.term.stdscr.move(0, 0) # leave this here
		# handle_movement moved to the screen class
		
	def handle_movement(self) -> None:
		"""Handles player movement"""
		ch = self.screen.getch()
		match ch: # probably a better way of doing this, however i am lazy
			case 27: #escape key
				self.screen.loadMenu("options") # loads the escape menu
			
			case 259 | 119: # up arrow | w
				ent = self.screen.getEntityAtPos(self.x, self.y-1)
				if ent and ent.block:
					ent.interact()
					return
				self.y -= 1
				
			case 258 | 115: # down arrow | s
				ent = self.screen.getEntityAtPos(self.x, self.y+1)
				if ent and ent.block:
					ent.interact()
					return
				self.y += 1
				
			case 260 | 97: # left arrow | a
				ent = self.screen.getEntityAtPos(self.x-1, self.y)
				if ent and ent.block:
					ent.interact()
					return
				self.x -= 1
				
			case 261 | 100: # right arrow | d
				ent = self.screen.getEntityAtPos(self.x+1, self.y)
				if ent and ent.block:
					ent.interact()
					return
				self.x += 1

		# makes sure the positions are all ok
		self.inside_border_check()
	
	def interact(self) -> None:
		"""Unused, Nothing should interact with player"""
		pass

	@property
	def stats(self) -> List[str]:
		"""Returns dynamic statlist (WIP)"""
		attribs = self.screen.attribs
		hpPerc = self.hp / self.maxHP # HP percentage
		fpPerc = self.fp / self.maxFP # FP percentage

		# green if hp over 50%, otherwise yellow if over 25%, otherwise red
		hpCol = attribs.green if (hpPerc > 0.5) else attribs.yellow if (hpPerc > 0.25) else attribs.red
		fpCol = attribs.green if (fpPerc > 0.5) else attribs.yellow if (fpPerc > 0.25) else attribs.red

		barLen = 10
		hpBar = "#" * (int(hpPerc * barLen)) + "-" * int(barLen - (hpPerc * barLen))
		fpBar = "#" * int(fpPerc * barLen) + "-" * int(barLen - (fpPerc * barLen))
		
		return [
			f"Hp ({self.hp}/{self.maxHP})",
			(hpBar, hpCol | attribs.bold),
			
			f"Fp ({self.fp}/{self.maxFP})",
			(fpBar, fpCol | attribs.bold),
			
			f"Att | 0",
			f"Def | 0",
			f"Str | 0",
			f"Dex | 0",
			f"Mag | 0",
			f"Lck | 0"
		]
	
	def damage(self, hp: int) -> None:
		self.hp -= hp
		if self.hp < 0:
			self.hp = 0
	
	def heal(self, hp: int) -> None:
		self.hp += hp
		if self.hp > self.maxHP:
			self.hp = self.maxHP