from dataclasses import dataclass
@dataclass
class Actor:
	char: str = '@'
	colour: int = None
	x: int = 0
	y: int = 0
	block: bool = True

	def set_pos(self, x:int, y:int) -> None:
		"""Sets the X and Y positions of an actor"""
		if x:
			self.x = x
		if y:
			self.y = y
	