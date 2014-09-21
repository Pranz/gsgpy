
# Grand strategy game taking place in a fantasy universe.
#
# Python 2.7
# All code except for the libtcod library written by Jesper Fridefors

import libtcodpy as libtcod
import os
import game

CWD = os.getcwd()
FONT_DIR = os.path.abspath(CWD + "/fonts")
DATA_DIR = os.path.abspath(CWD + "/data")

FONT     = "terminal12x12_gs_ro.png"

SCREEN_WIDTH  = 80
SCREEN_HEIGHT = 60

COLOR_TEXT = libtcod.Color(255,255,255)

if __name__ == "__main__":
	libtcod.console_set_custom_font(FONT_DIR + "/" + FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
	libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, "TownRPG", False)
	
	game.init_game()

	while not libtcod.console_is_window_closed():
		if game.loop():
			break
