# 2048
This is a project creating a 2048 game. It includes an original version for human player and an AI version using greedy algorithm to play the game. The following contents introduces commands and environments. 

# Commands
Download the code and run it from your editor(take VS Code for example).
## Original Version
Use arrows to control the movement of squares.  
### LeftArrow
squares go left  
### RightArrow
squares go right  
### UpArrow
squares go up  
### DownArrow
squares go down
### Other Keys
nothing will be happen
## AI Version
Algorithm plays the game automatically, programmors only needs to control the process.
### Space
press Space to let AI enter the next turn.
## AIplus Version
try to use search algorithm, MCTS and LLM to play the game automatically.
### Search Algorithm
use the function 'run_game' and provide parameters 'ai_mode=True', 'ai_type=naive'.
### MCTS
use the function 'run_game' and provide parameters 'ai_mode=True', 'ai_type=mcts'.
### LLM
use the function 'run_game' and provide parameters 'ai_mode=True', 'ai_type=llm'.

# Environment
Python 3.12  
pygame 2.6.0  
