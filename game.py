
import libtcodpy as libtcod
import main
import menu

class State:
	def __init__(self, init, update, render):
		self.init_   = init
		self.is_initialized = False
		self.update = update
		self.render = render
		self.requests_new_state = None
	def init(self):
		if not self.is_initialized:
			self.init_(self)

def init_game():
	global current_state
	current_state = State(menu.initialize,menu.update, menu.render)
	current_state.init()

def loop():
	global current_state
	if current_state.requests_new_state is not None:
		current_state = current_state.requests_new_state
		current_state.init()
	current_state.render(current_state)
	return current_state.update(current_state)
