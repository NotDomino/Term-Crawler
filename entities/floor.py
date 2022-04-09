from dataclasses import dataclass

@dataclass
class Floor:
	x: int
	y: int
	char = '█'
	colour = None