Nine-Board Tic-Tac-Toe Agent starter code
COMP3411/9814 Artificial Intelligence
# Briefly describe how your program works, including any algorithms and data structures employed, and explain any design decisions you made along the way:
  Our program works by looking at the current state of the boarding and performing a minimax alpha beta pruning search 
  on future states of the game to a specific depth defined by a depth interval step function, in order to calculate
   the best move to make at a given state
   The main datastrucutre employed is the use of a StateNode to store specific possible moves in the Minimax search
   this StateNode function also has a Transposition table class which is used to Cachce different results of the Alpha
   beta pruning search. This helps avoid needing to recaculate different future states for a potential serach that have already been Calculated
   One of the main design decisions was to use an extra state to keep track of the search in a transposition table
    Additionaly using a step function to define the depth that would be searched to was another essential design decision.
   as it allowed us to manually finetune the search to use a low depth at the begining and a higher depth at the end of the
