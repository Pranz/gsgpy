
import noise
import random
import libtcodpy as libtcod
import main
import math

MAP_WIDTH  = 40
MAP_HEIGHT = 30
REGION_WIDTH  = 16
REGION_HEIGHT = 16
OVERVIEW_SCREEN_WIDTH  = 40
OVERVIEW_SCREEN_HEIGHT = 30
SCROLL_STRICTNESS = 8

WATER_THRESHOLD = 0.0
TREELINE        = 0.3

RIVER_EROSION = 0.002
RIVERLAKES = 90

class Tile():
	#Smallest unit of land there is. Has a height and climate. Belongs to a region.
	def __init__(self,height,climate):
		self.height  = height
		self.climate = climate
class Region():
	def __init__(self,height_map, x,y,width,height):
		self.tiles = []
		heightsum  = 0.0
		for xx in range(0,width):
			tilecolumn = []
			for yy in range(0,height):
				heightsum += height_map(x*width + xx,y*height+yy)
				tilecolumn.append(Tile(height_map(x*width + xx,y*height+yy), None))
			self.tiles.append(tilecolumn)
		self.average_height = heightsum / (width * height)

def initialize(self):
	self.overview_con = libtcod.console_new(OVERVIEW_SCREEN_WIDTH, OVERVIEW_SCREEN_HEIGHT)
	self.debug_con    = libtcod.console_new(OVERVIEW_SCREEN_WIDTH, 10)
	self.region_con   = libtcod.console_new(REGION_HEIGHT,REGION_WIDTH)
	random.seed()
	height_map_seed = random.randint(-1000000,1000000)
	self.cameraX    = 0
	self.cameraY    = 0
	self.cursorX    = OVERVIEW_SCREEN_WIDTH  / 2
	self.cursorY    = OVERVIEW_SCREEN_HEIGHT / 2
	self.region_cursorX = 0
	self.region_cursorY = 0
	self.height_map = gen_height_map(height_map_seed, 0.004,10)
	self.world = []
	for x in range(0,MAP_WIDTH):
		tilecolumn = []
		for y in range(0,MAP_HEIGHT):
			tilecolumn.append(Region(self.height_map,x,y,REGION_WIDTH,REGION_HEIGHT))
		self.world.append(tilecolumn)
		print str(x) + " of " + str(MAP_WIDTH)
	i = 0
	print "heightmap done"
	while i < RIVERLAKES:
		x = random.randint(20,MAP_WIDTH*REGION_WIDTH - 20)
		y = random.randint(20,MAP_HEIGHT*REGION_HEIGHT - 20)
		def gen_river(mapX,mapY,regX,regY,min_height):
			try:
				height = self.world[mapX][mapY].tiles[regX][regY].height
			except IndexError:
				return False
			self.world[mapX][mapY].tiles[regX][regY].height = WATER_THRESHOLD - 0.01
			if height > min_height or height < WATER_THRESHOLD:
				return False
			for x in (-1,1):
				realx = mapX * REGION_WIDTH + regX + x
				gen_river(realx / REGION_WIDTH, mapY,realx % REGION_WIDTH, regY,height+RIVER_EROSION)
			for y in (-1,1):
				realy = mapY * REGION_HEIGHT + regY + y
				gen_river(mapX, realy / REGION_HEIGHT, regX, realy % REGION_HEIGHT, height+RIVER_EROSION)
			return True

		if gen_river(x / REGION_WIDTH, y / REGION_HEIGHT,x % REGION_WIDTH, y % REGION_HEIGHT,1):
			i += 1
			print ("river " + str(i) + " done")

		
def render(self):
	libtcod.console_clear(self.overview_con)
	libtcod.console_clear(self.debug_con)
	libtcod.console_clear(self.region_con)
	
	#draw overview map
	for x in range(0, OVERVIEW_SCREEN_WIDTH):
		for y in range(0, OVERVIEW_SCREEN_HEIGHT):
			height = self.world[self.cameraX + x][self.cameraY + y].average_height

			if height < WATER_THRESHOLD:
				libtcod.console_put_char_ex(self.overview_con, x,y, '~', libtcod.lighter_blue * (height * 1.5 + 1), libtcod.blue * (height *1.5 + 1))
			elif height >= WATER_THRESHOLD and height < TREELINE:
				libtcod.console_put_char_ex(self.overview_con,x,y, chr(33),libtcod.green * (height *-1.5 +1), libtcod.dark_green * (height * -1.5 + 1))
			elif height >= TREELINE:
				libtcod.console_put_char_ex(self.overview_con, x,y, '^', libtcod.light_grey, libtcod.dark_grey)
			if self.cursorX - self.cameraX == x and self.cursorY- self.cameraY == y:
				libtcod.console_put_char_ex(self.overview_con,x,y,'X',libtcod.white,libtcod.black)
	
	#draw region map
	for x in range(0,REGION_WIDTH):
		for y in range(0,REGION_HEIGHT):
			height = self.world[self.cursorX][self.cursorY].tiles[x][y].height
			libtcod.console_put_char_ex(self.region_con,x,y, ' ',libtcod.white, libtcod.Color(int(height*255),int(height*255),int(height*255)))
			if height < WATER_THRESHOLD:
				libtcod.console_put_char_ex(self.region_con, x,y, '~', libtcod.lighter_blue * (height * 1.5 + 1), libtcod.blue * (height *1.5 + 1))
			elif height >= WATER_THRESHOLD and height < TREELINE:
				libtcod.console_put_char_ex(self.region_con,x,y, chr(33),libtcod.green * (height*-1.5+ 1),libtcod.dark_green * (height*-1.5 + 1))
			elif height >= TREELINE:
				libtcod.console_put_char_ex(self.region_con, x,y, '^', libtcod.light_grey, libtcod.dark_grey)
			

	#debug text
	libtcod.console_print(self.debug_con,0,0,"cursorX: " + str(self.cursorX))
	libtcod.console_print(self.debug_con,0,1,"cursorY: " + str(self.cursorY))
	libtcod.console_print(self.debug_con,0,2,"cameraX: " + str(self.cameraX))
	libtcod.console_print(self.debug_con,0,3,"cameraY: " + str(self.cameraY))

	libtcod.console_blit(self.debug_con,0, 0, 0, 0, 0, 0, OVERVIEW_SCREEN_HEIGHT + 1)
	libtcod.console_blit(self.region_con,0, 0, 0, 0, 0, OVERVIEW_SCREEN_WIDTH +1,0)
	libtcod.console_blit(self.overview_con, 0, 0, 0, 0, 0, 0, 0)
	libtcod.console_flush()

def update(self):
	key = libtcod.console_wait_for_keypress(True)
	if key.vk == libtcod.KEY_ESCAPE:
		return True
	if key.vk ==libtcod.KEY_ENTER:
		self.height_map = gen_height_map(random.randint(-1000000,1000000), 0.004,10)
	increment = 1 if not libtcod.console_is_key_pressed(libtcod.KEY_SHIFT) else 10
	if key.vk == libtcod.KEY_RIGHT:
		self.cursorX = min(self.cursorX + increment, MAP_WIDTH -1)
	elif key.vk == libtcod.KEY_LEFT and self.cursorX:
		self.cursorX = max(self.cursorX - increment, 0)
	elif key.vk == libtcod.KEY_UP:
		self.cursorY = max(self.cursorY - increment, 0)
	elif key.vk == libtcod.KEY_DOWN:
		self.cursorY = min(self.cursorY + increment, MAP_HEIGHT -1)
	
	while self.cameraX != (MAP_WIDTH - OVERVIEW_SCREEN_WIDTH) and (self.cursorX - (self.cameraX + OVERVIEW_SCREEN_WIDTH / 2) >= SCROLL_STRICTNESS):
		self.cameraX += 1
	while self.cameraX and (self.cursorX - (self.cameraX + OVERVIEW_SCREEN_WIDTH / 2) <= -SCROLL_STRICTNESS):
		self.cameraX -= 1
	while self.cameraY != (MAP_HEIGHT - OVERVIEW_SCREEN_HEIGHT) and (self.cursorY - (self.cameraY + OVERVIEW_SCREEN_HEIGHT / 2) >= SCROLL_STRICTNESS):
		self.cameraY += 1
	while self.cameraY and (self.cursorY - (self.cameraY + OVERVIEW_SCREEN_HEIGHT / 2) <= -SCROLL_STRICTNESS):
		self.cameraY -= 1

def gen_height_map(seed,scale,octaves=1,persistence=0.3):
	return lambda x,y: noise.pnoise2(scale * (x + seed), scale * (y + seed),octaves,persistence,4)
