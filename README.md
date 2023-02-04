# mybots
repository for Ludobots Assignment 5
Jeffrey He

Run main.py to start the code.

Assignment 5:
New Creature was based off of previous quadruped, however, the right leg was taken off, instead two extra blocks were added that do not touch the ground there, but instead change how the center of mass and inertia works. The objective of the robot is to go as low as possible, while starting on top of two wide surfaces. Initially, the robot has no clue how to go lower, however, after parallel hill climbing, it optimizes the path it takes to go to the ground floor. Without enough optimization, sometimes the robot gets stuck at a local minimum due to there being obstructive blocks in the direction the robot can travel the fastest. Instead, it must go sideways which is slower and harder, but ends up with a better result.

Fitness Function: The lowest z value possible, or the robot trying to get as low as possible in height during each trial.

Video: https://youtu.be/kmg4JGV7Dc4

Resources:
Pyrosim: https://github.com/jbongard/pyrosim
Ludobots: https://reddit.com/r/ludobots
