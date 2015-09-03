#!/usr/bin/env python

import sys
import board_utils
if len(sys.argv) != 3:
	print "Usage: main.py board_name num_rows num_cols"
	sys.exit(0)
board = board_utils.create_board(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))