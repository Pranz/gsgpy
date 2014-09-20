
#Menus are made of dictionaries
import libtcodpy as libtcod
import overworld
import game
import main
import util
import gol

menu = ["Play now",
		"GOL",
		"Test",
		["Branch","option1"
				 ,"option2"]
		]

def resolve_case(self, args):
	if args[-1] == "Play now":
		self.requests_new_state = game.State(overworld.initialize, overworld.update, overworld.render)
	elif args[-1] == "GOL":
		self.requests_new_state = game.State(gol.initialize,gol.update,gol.render)
def initialize(self):
	self.menu_choice  = 0
	self.current_menu = menu
	self.stack        = []
	self.menu_stack   = []
	self.con          = libtcod.console_new(main.SCREEN_WIDTH, main.SCREEN_HEIGHT)

def update(self):
	key = libtcod.console_wait_for_keypress(True)
	if libtcod.console_is_key_pressed(libtcod.KEY_ESCAPE):
		if self.menu_stack == []:
			return True
		self.current_menu = self.menu_stack[-1]
		self.menu_choice  = util.generic_index(lambda x: x[0] == self.stack[-1], self.current_menu)
		self.menu_stack   = self.menu_stack[:-1]
		self.stack        = self.stack[:-1]
	elif libtcod.console_is_key_pressed(libtcod.KEY_UP):
		if not self.menu_choice == 0:
			self.menu_choice -= 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		if not self.menu_choice == (len(self.current_menu) - 1):
			self.menu_choice += 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_ENTER):
		choice = self.current_menu[self.menu_choice]
		if type(choice) is list:
			self.menu_choice = 0
			self.menu_stack.append(self.current_menu)
			self.current_menu = choice[1:]
			self.stack.append(choice[0])
		else:
			self.stack.append(choice)
			resolve_case(self, self.stack)

def render(self):
	libtcod.console_clear(self.con)
	i = 0
	while i < len(self.current_menu):
		if type(self.current_menu[i]) is list:
			to_print = self.current_menu[i][0]
		else:
			to_print = self.current_menu[i]
		libtcod.console_print(self.con, 5, 10 + i, to_print)
		i += 1
	libtcod.console_print(self.con, 3, 10 + self.menu_choice, "*")
	libtcod.console_blit(self.con, 0, 0, 0, 0, 0, 1, 1)
	libtcod.console_flush()
