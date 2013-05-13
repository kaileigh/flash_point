#include <stdio.h>
#include <stdlib.h>

#include "board_utils.h"

board_t* create_board(board_t* board, int board_rows, int board_cols){
  char* line;
  FILE* f = fopen("./board.txt", "r");
  int input_row = 0;
  int input_col = 0;
  int width = 2*board_cols - 1;
  line = malloc(width+3);
  board->rows = board_rows;
  board->cols = board_cols;
  board->grid = malloc(board_rows*board_cols*sizeof(space_t*));
  while (fgets(line, width+3, f) != NULL){
    printf("%s", line);
    for(input_col = 0; input_col < width; input_col++){
      if(!(input_row % 2)){
        if(!(input_col % 2)){
          /* Even row, even col */
          space_t* space = create_space(board, input_row / 2, input_col / 2);
          board->grid[space->row * board->cols + space->col] = space;
        }else{
          /* Even row, odd col */
          if((line[input_col] == '|') || (line[input_col] == '+')){
            wall_t* wall = create_wall(line[input_col]);
            GET_SPACE(board,input_row/2,input_col/2)->walls[EAST] = wall;
          }
        }
      }else{
        if(!(input_col % 2)){
          /* Odd row, even col */
          if((line[input_col] == '-') || (line[input_col] == '+')){
            wall_t* wall = create_wall(line[input_col]);
            GET_SPACE(board,input_row/2,input_col/2)->walls[SOUTH] = wall;
          }
        }else{
          /* Odd row, odd col */
        }
      }
    }
    input_row++;
  }
  return board;
}

void display_board(board_t* board){
  int output_row, output_col, i;
  int display_size = (2*board->cols)*(2*board->rows) + 1;
  char* output = calloc(display_size, 1);
  for(i = 0; i < display_size-1; i++){
    output[i] = ' ';
  }

  
  for(output_row = 0; output_row < board->rows; output_row++){
    for(output_col = 0; output_col < board->cols; output_col++){
      space_t* space = GET_SPACE(board, output_row, output_col);
      OUTPUT(board, 2*output_row, 2*output_col) = '.';
      if(space->walls[EAST]){
        OUTPUT(board, 2*output_row, 2*output_col + 1) = space->walls[EAST]->display;
      }else{
        OUTPUT(board, 2*output_row, 2*output_col + 1) = ' ';
      }
      if(space->walls[SOUTH]){
        OUTPUT(board, 2*output_row + 1, 2*output_col) = space->walls[SOUTH]->display;
      }else{
        OUTPUT(board, 2*output_row + 1, 2*output_col) = ' ';
      }
    }
    OUTPUT(board, 2*output_row, 2*(output_col)-1) = '\n';
    OUTPUT(board, 2*output_row + 1, 2*(output_col)-1) = '\n';
  }
  printf("%s",output);
}

space_t* create_space(board_t* board, int row, int col){
  int i;
  space_t* space = malloc(sizeof(space_t));
  space->row = row;
  space->col = col;
  space->fire_status = EMPTY;
  space->poi = NULL;
  space->hotspot = 0;
  space->hazmat = 0;
  if(space->row == 0 || space->row > board->rows ||
     space->col == 0 || space->col > board->cols){
    space->inside_house = 0;
  }else{
    space->inside_house = 1;
  }
  for(i = 0; i < 4; i++){
    space->walls[i] = NULL;
  }
  /* If the previous space in this row has an eastern wall, make that our
   * western wall. If the previous space in this column has a southern wall,
   * make that our northern wall. */
  if(col){
    if(GET_SPACE(board, row, col-1)->walls[EAST]){
      space->walls[WEST] = GET_SPACE(board, row, col-1)->walls[EAST];
    }
  }
  if(row){
    if(GET_SPACE(board, row-1, col)->walls[SOUTH]){
      space->walls[NORTH] = GET_SPACE(board, row-1, col)->walls[SOUTH];
    }
  }
  return space;
}

void debug(board_t* board){
  int i,j;
  for(i = 0; i < board->rows; i++){
    for(j = 0; j < board->cols; j++){
      space_t* space = GET_SPACE(board, i, j);
      printf("space (%d, %d) has walls: %p %p %p %p\n", i, j, (void*) space->walls[NORTH], (void*) space->walls[EAST], (void*) space->walls[SOUTH], (void*) space->walls[WEST]);
    }
  }
}

   

wall_t* create_wall(char display){
  wall_t* wall = malloc(sizeof(wall_t));
  if(display == '+'){
    wall->door = 1;
  }else{
    wall->door = 0;
  }
  wall->damage = 0;
  wall->open = 0;
  wall->display = display;
  return wall;
}
   
