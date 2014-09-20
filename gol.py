#game of life
import noise
import libtcodpy as libtcod
import random
import main

GOL_WIDTH  = 60
GOL_HEIGHT = 40

def initialize(self):
	self.con   = libtcod.console_new(main.SCREEN_WIDTH, main.SCREEN_HEIGHT)
	random.seed()
	noise_seed = random.randint(-10000,10000)
	scale      = 0.02
	self.noise = lambda x,y: noise.pnoise2(scale * (x + noise_seed), scale * (y + noise_seed),15,0.5,3)
	self.world = [[self.noise(x,y) > -0.1 for y in range(0,GOL_HEIGHT+2)] for x in range(0,GOL_WIDTH+2)]
	for x in range(0,GOL_WIDTH+2):
		self.world[x][0]            = False
		self.world[x][GOL_HEIGHT+1] = False
	for y in range(0,GOL_HEIGHT+2):
		self.world[0][y]            = False
		self.world[GOL_WIDTH+1][y]  = False
def next_iteration(world):
	new_world = world[:]
	for x in range(1,GOL_WIDTH):
		for y in range(1, GOL_HEIGHT):
			neighbours = 0
			for xoffset in range(-1,2):
				for yoffset in range(-1,2):
					if (xoffset != 0 or yoffset != 0) and world[x+xoffset][y+yoffset]:
						neighbours += 1
			if (neighbours == 2 and world[x][y]) or neighbours == 3:
				new_world[x][y] = True
			else:
				new_world[x][y] = False

	return new_world
					

def update(self):
	key = libtcod.console_wait_for_keypress(True)
	if key.vk == libtcod.KEY_ENTER:
		self.world = next_iteration(self.world)
	if key.vk == libtcod.KEY_ESCAPE:
		return True

def render(self):
	libtcod.console_clear(self.con)

	for x in range(0,GOL_WIDTH+2):
		for y in range(0,GOL_HEIGHT+2):
			if self.world[x][y] == True:
				libtcod.console_put_char(self.con,x,y,'.')
			if x == 0 or x == GOL_WIDTH+1 or y == 0 or y == GOL_HEIGHT+1:
				libtcod.console_put_char(self.con,x,y,'#')
	
	libtcod.console_blit(self.con,0,0,0,0,0,1,1)
	libtcod.console_flush()
