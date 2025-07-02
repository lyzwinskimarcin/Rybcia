# Rybcia
Rybcia is an AI engine for a popular logical board game "Hey, that's my fish", based on Monte Carlo Tree Search algorithm with some customizations. It was created as part of my Bachelor Thesis at the University of Warsaw. Since the engine has not been tested against any expert players (I do not think there are many in the world), its true power is hard to measure. It seems to be strong against amateur players, yet after learning the game and practicing it is defenitely possible to beat it. It has been modeld to be effective against my own playstyle therefore a different playstyle might be rewarded. Pygame visualisation was not the focus of my work so bugs are defenitely possible during the gameplay.
To avoid crashing the game:
- don't click any fields while the AI opponent is thinking
- don't move the window while AI is thinking


## Try facing it yourself
You will need Python (at least 3.9), numpy, numba and pygame. In the file "__main__.py" you can set most of the parameters.


How to run:
- Download final_version directory
- Put it in an empty new directory
- Open in the terminal
- pip install numpy numba pygame or activate suitable environment
- run the following command:
  python -m final_version
- With default parameters AI will take about 27 seconds, depending on the hardware and it will be quicker each move it makes. In the case of my laptop endgame moves are being made in about 5 seconds.



How to play:
- In the starting phase, select a tile with only 1 fish. This is the penguin placement phase and you have two penguins two place alternating.
- In the later phase, during your turn, first select the penguin you want to move, then click where you want to place it. If you select the wrong penguin try to move him on an unavailable tile this will allow you to choose again.
- Monitor console window for information about the ongoing game.
- In the final phase, there is a chance that one player's penguins will be trapped. in this case the player that still has moves has to make moves untill their moves run out.
- Whoever has the most Fishes wins.


## About the algorithm

The engine is based on a classical MCTS with few modifications to achieve better results in this specific game:
- Engine prioritizes calculating moves that limit opponent first.
- it is forced to at least consider every possible move from the starting position (position that is being evaluated), before moving on to expanding the search tree onto deeper nodes
- there is a treshold of visits implemented  for deeper levels of the search tree in order to make the algorithm expand deeper nodes. Later on when all peer nodes reach the vis_treshold, they are being expanded until it is possible. This part makes sense only because the search tree is being reused in the next move.
- Search Tree recycling. Since the moves that have been played are represented on the search tree from the last search, the tree is being cut off at the node representing the last made move thus allowing the algorithm to continue the search.
