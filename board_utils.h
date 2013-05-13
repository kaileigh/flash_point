#ifndef BOARD_UTILS_H
#define BOARD_UTILS_H

#define EMPTY 0
#define SMOKE 1
#define FIRE 2

#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

#define GET_SPACE(board, x, y) board->grid[((x)*board->cols) + (y)]
#define OUTPUT(board, x, y) board->output[((x)*board->cols*2) + (y)]

typedef struct {
  int door;
  int damage;
  int open;
  char display;

} wall_t;

typedef struct {
  int revealed;
  int false_alarm;
} poi_t;

typedef struct {
  int row;
  int col;
  int fire_status;
  poi_t* poi;
  int hotspot;
  int hazmat;
  int inside_house;
  wall_t* walls[4];
} space_t;

typedef struct {
  space_t** grid;
  char* output;
  int rows;
  int cols;
  int rescued;
  int lost;
  int remaining_damage;
} board_t;

board_t* create_board(board_t* board, int rows, int cols);

space_t* create_space(board_t* board, int row, int col);

wall_t* create_wall(char door);

void display_board(board_t* board);
void debug(board_t* board);

#endif
