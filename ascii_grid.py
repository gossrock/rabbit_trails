from typing import NamedTuple, List

class BorderChars(NamedTuple):
	tl:str
	tr:str
	bl:str
	br:str
	
	lT:str
	rT:str
	tT:str
	bT:str
	
	horiz:str
	vert:str
	cross:str
SmplBdr = BorderChars(tl='+', tr='+', bl='+', br='+', lT='+', rT='+', tT='+', bT='+', horiz='-', vert='|', cross='+')
StdBdr = BorderChars(tl='┌', tr='┐', bl='└', br='┘', lT='├', rT='┤', tT='┬', bT='┴', horiz='─', vert='│', cross='┼')
BoldBdr = BorderChars(tl='┏', tr='┓', bl='┗', br='┛', lT='┣', rT='┫', tT='┳', bT='┻', horiz='━', vert='┃', cross='╋')
DblBdr = BorderChars(tl='╔', tr='╗', bl='╚', br='╝', lT='╠', rT='╣', tT='╦', bT='╩', horiz='═', vert='║', cross='╬')


def makeGrid(col_widths:List[int], row_heights:List[int], bc:BorderChars) -> str:
	grid:str = ''
	cols:int = len(col_widths)
	rows:int = len(row_heights)
	for r in range(rows):
		# Top line of cell row
		for c in range(cols):
			# top of cell
			# top left of cell
			if r == 0 and c == 0:
				grid += bc.tl
			elif r == 0:
				grid += bc.tT
			elif c == 0:
				grid += bc.lT
			else:
				grid += bc.cross
			# top middle of cell
			for _ in range(col_widths[c]):
				grid += bc.horiz
			#top right of cell if at the end of the row (otherwise top right is top left of next cell)
			if r==0 and c == cols-1:
				grid += bc.tr 
				grid += '\n'
			elif c == cols-1:
				grid += bc.rT
				grid += '\n'
		# center portion of cell
		for _ in range(row_heights[r]):
			for c in range(cols):
				grid += bc.vert
				for _ in range(col_widths[c]):
					grid += ' '
				if c == cols - 1:
					grid += bc.vert
					grid += '\n'
		# if last row add bottom line
		if r == rows - 1: 
			for c in range(cols):
				# lower left of cell
				if c == 0:
					grid += bc.bl
				else:
					grid += bc.bT
				# bottom middle of cell
				for _ in range(col_widths[c]):
					grid += bc.horiz
				#if last col add last corner
				if c == cols - 1:
					grid += bc.br
					grid += '\n'
					
	return grid
				
if __name__=='__main__':
	print(makeGrid([4, 4, 4, 4], [2, 2, 2, 2], SmplBdr))
	print(makeGrid([3,2, 1], [1, 2, 3, 4], StdBdr))
	#print(makeGrid([5, 4, 3, 2, 1], [2, 1], BoldBdr))
	#print(makeGrid([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], DblBdr))
			
