
import noise
import random
import libtcodpy as libtcod
import main
import math

MAP_WIDTH  = 70
MAP_HEIGHT = 70
REGION_WIDTH  = 16
REGION_HEIGHT = 16
OVERVIEW_SCREEN_WIDTH  = 30
OVERVIEW_SCREEN_HEIGHT = 30
SCROLL_STRICTNESS = 8

WATER_THRESHOLD = 0.0
TREELINE        = 0.26

RIVER_EROSION = 0.002
RIVERLAKES = 200
RIVERLEVEL = WATER_THRESHOLD - 0.01

class Tile():
	#Smallest unit of land there is. Has a height. belongs to region
	def __init__(self,height):
		self.height  = height
class Region():
	def __init__(self,height_map,rain_fall_map,temperature_map,x,y,width,height):
		self.tiles = []
		heightsum  = 0.0
		for xx in range(0,width):
			tilecolumn = []
			for yy in range(0,height):
				heightsum += height_map(x*width + xx,y*height+yy)
				tilecolumn.append(Tile(height_map(x*width + xx,y*height+yy)))
			self.tiles.append(tilecolumn)
		self.average_height = heightsum / (width * height)
		self.rainfall = rain_fall_map(x,y) *3 - self.average_height * 3 + 2
		self.temperature = temperature_map(x,y)
		if self.average_height < WATER_THRESHOLD:
			self.biome = "ocean"
		elif self.average_height >= TREELINE:
			self.biome = "mountain"
		elif self.temperature < 0:
			self.biome = "tundra"
		elif self.temperature < 14:
			if self.rainfall < 1:
				self.biome = "temperate grassland"
			elif self.rainfall < 1.3:
				self.biome = "woodland"
			else:
				self.biome = "boreal forest"
		elif self.temperature < 22:
			if self.rainfall < 1.1:
				self.biome = "temperate grassland"
			elif self.rainfall < 1.5:
				self.biome = "woodland"
			else:
				self.biome = "temperate forest"
		else:
			if self.rainfall < 1.3:
				self.biome = "desert"
			elif self.rainfall < 1.8:
				self.biome = "tropical forest"
			else:
				self.biome = "tropical rainforest"

def initialize(self):
	self.overview_con = libtcod.console_new(OVERVIEW_SCREEN_WIDTH, OVERVIEW_SCREEN_HEIGHT)
	self.debug_con    = libtcod.console_new(OVERVIEW_SCREEN_WIDTH, 10)
	self.region_con   = libtcod.console_new(REGION_HEIGHT,REGION_WIDTH)
	random.seed()
	height_map_seed = random.randint(-1000000,1000000)
	rain_fall_map_seed = random.randint(-1000000,1000000)
	temperature_map_seed = random.randint(-1000000,1000000)
	self.cameraX    = 0
	self.cameraY    = 0
	self.cursorX    = OVERVIEW_SCREEN_WIDTH  / 2
	self.cursorY    = OVERVIEW_SCREEN_HEIGHT / 2
	self.region_cursorX = 0
	self.region_cursorY = 0
	height_map = gen_height_map(height_map_seed, 0.004,10)
	rain_fall_map = gen_rainfall_map(rain_fall_map_seed,0.09,10)
	temperature_map = gen_temperature_map(temperature_map_seed,0.004,MAP_WIDTH,10)
	self.world = []
	for x in range(0,MAP_WIDTH):
		tilecolumn = []
		for y in range(0,MAP_HEIGHT):
			tilecolumn.append(Region(height_map,rain_fall_map,temperature_map,x,y,REGION_WIDTH,REGION_HEIGHT))
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
			self.world[mapX][mapY].tiles[regX][regY].height = RIVERLEVEL
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
			#height = self.world[self.cameraX + x][self.cameraY + y].average_height
			draw_region(x,y,self.world[self.cameraX+x][self.cameraY+y].average_height,self.world[self.cameraX+x][self.cameraY+y].biome,self.overview_con)
			#if height < WATER_THRESHOLD:
			#	libtcod.console_put_char_ex(self.overview_con, x,y, '~', libtcod.lighter_blue * (height * 1.5 + 1), libtcod.blue * (height *1.5 + 1))
			#elif height >= WATER_THRESHOLD and height < TREELINE:
			#	libtcod.console_put_char_ex(self.overview_con,x,y, chr(33),libtcod.green * (height *-1.5 +1), libtcod.dark_green * (height * -1.5 + 1))
			#elif height >= TREELINE:
			#	libtcod.console_put_char_ex(self.overview_con, x,y, '^', libtcod.light_grey, libtcod.dark_grey)
			if self.cursorX - self.cameraX == x and self.cursorY- self.cameraY == y:
				libtcod.console_put_char_ex(self.overview_con,x,y,'X',libtcod.white,libtcod.black)
	
	#draw region map
	for x in range(0,REGION_WIDTH):
		for y in range(0,REGION_HEIGHT):
			draw_tile(x,y,self.world[self.cursorX][self.cursorY].tiles[x][y].height,self.world[self.cursorX][self.cursorY].biome,self.region_con)

	#debug text
	libtcod.console_print(self.debug_con,0,0,"cursorX: " + str(self.cursorX))
	libtcod.console_print(self.debug_con,0,1,"cursorY: " + str(self.cursorY))
	libtcod.console_print(self.debug_con,0,2,"cameraX: " + str(self.cameraX))
	libtcod.console_print(self.debug_con,0,3,"cameraY: " + str(self.cameraY))
	libtcod.console_print(self.debug_con,0,4,"temperature: " + str(self.world[self.cursorX][self.cursorY].temperature))
	libtcod.console_print(self.debug_con,0,5,"rainfall:    " + str(self.world[self.cursorX][self.cursorY].rainfall))
	libtcod.console_print(self.debug_con,0,6,"biome: " + self.world[self.cursorX][self.cursorY].biome)
	libtcod.console_print(self.debug_con,0,7,"avg.height: " + str(self.world[self.cursorX][self.cursorY].average_height))


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

def gen_rainfall_map(seed, scale, octaves=1,persistence=0.5):
	return lambda x,y: noise.pnoise2(scale * (x + seed), scale * (y + seed),octaves,persistence,2.5)

def gen_temperature_map(seed,scale,mapY,octaves=1,persistence=0.5):
	return lambda x,y: noise.pnoise2(scale * (x + seed), scale * (y + seed),octaves,persistence,2.5)*50 - (abs(y - (mapY / 2.0)) * (60.0 / mapY)) + 36

def draw_region(x,y,height,biome,con):
	if biome == "ocean":
		libtcod.console_put_char_ex(con, x,y, '~', libtcod.lighter_blue * (height * 1.5 + 1), libtcod.blue * (height *1.5 + 1))
	elif biome == "mountain":
		libtcod.console_put_char_ex(con, x,y, '^', libtcod.light_grey, libtcod.dark_grey)
	elif biome == "boreal forest":
		libtcod.console_put_char_ex(con, x,y, chr(157), libtcod.dark_green, libtcod.darkest_green)
	elif biome == "tundra":
		libtcod.console_put_char_ex(con, x,y, chr(177), libtcod.lighter_sky, libtcod.sky)
	elif biome == "temperate grassland":
		libtcod.console_put_char_ex(con, x,y, chr(176), libtcod.green, libtcod.desaturated_chartreuse)
	elif biome == "woodland":
		libtcod.console_put_char_ex(con, x,y, chr(244), libtcod.darker_chartreuse,libtcod.dark_chartreuse)
	elif biome == "temperate forest":
		libtcod.console_put_char_ex(con, x,y, chr(237), libtcod.darkest_yellow, libtcod.dark_green * 0.8)
	elif biome == "tropical forest":
		libtcod.console_put_char_ex(con, x,y, chr(186), libtcod.dark_sea,libtcod.darkest_sea)
	elif biome == "tropical rainforest":
		libtcod.console_put_char_ex(con, x,y, chr(215), libtcod.dark_sea * 0.8, libtcod.darkest_sea)
	elif biome == "desert":
		libtcod.console_put_char_ex(con, x,y, chr(177), libtcod.light_yellow, libtcod.dark_yellow)
	else:
		libtcod.console_put_char_ex(con, x,y, 'a', libtcod.white, libtcod.black)

def draw_tile(x,y,height,biome,con):
	if height < WATER_THRESHOLD:
		libtcod.console_put_char_ex(con, x,y, '~', libtcod.lighter_blue * (height * 1.5 + 1), libtcod.blue * (height *1.5 + 1))
	elif height <= TREELINE and biome not in ("ocean","mountain"):
		draw_region(x,y,height,biome,con)
	elif height > TREELINE:
		libtcod.console_put_char_ex(con, x,y, '^', libtcod.light_grey, libtcod.dark_grey)
	else:
		libtcod.console_put_char_ex(con, x,y, chr(178),libtcod.light_green,libtcod.darker_green)

