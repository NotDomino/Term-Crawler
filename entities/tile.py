from dataclasses import dataclass
from typing import Optional

@dataclass
class Tile:
	x: int
	y: int
	char: str = '█'
	colour: Optional[int] = None