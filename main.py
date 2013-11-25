#!/usr/bin/env python

import sys
import board_utils

board = board_utils.create_board(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
print sys.argv[1]
