# mybots
repository for Ludobots Assignment 7
Jeffrey He

Run main.py to start the code.

Assignment 7:
Body/Brain Generation:
PIC
DESCRIPTION

Body generation:
A random amount of links gets generated between 5-15.

Each link can is randomly chosen to be a sensor with a 50% probability.

Each link has its x,y,z dimensions stored in a dictionary randomly between 0.2 and 1.2.

Dictionary stores information regarding to open faces for future joints and links.

Dictionary stores information regarding relative position for each link to avoid collision on forming.

First two links and first joint are hard coded.

Subsequent links and joints are created through for loop to the amount of links.

For each new link, it creates a joint between a randomly selected old link. Then a randomly selected available face is selected on that link.

A while loop checks to make sure the selected old link has a possible face.

Then, collision detection is run so that the new link does not exist in the same space as an old link.

If so, create a joint between a different link and face.

When creating a new link and joint, previous link information is used to create the new joint position in joint_maker.

Iterate over every new link and then end pyrosim.


Brain Generation:
Use stored variables to create sensors for the appropriate links, and generate motors off the list of joints created in body generation.

The weights for the sensors and motors are chosen at random as well.


It fills 3d space by having the option to produce multiple links off the same link instead of one link per link. The limbs protrude into free space and anti-collision detection is recorded through having each links' relative position and making sure it doesn't collide.
Most of the work done is in solution, with most lines commented what they are trying to do.

Video: vid

Resources:
Pyrosim: https://github.com/jbongard/pyrosim
Ludobots: https://reddit.com/r/ludobots
