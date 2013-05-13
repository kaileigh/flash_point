#include "board_utils.h"

int main(){
  board_t board;
  create_board(&board, 6, 8);
  debug(&board);
  display_board(&board);
  return 0;
}
