# Robotics-final_project-robot_navigations_KOMODO

Robotics with Ros Operating System and Catkin_Ws workspace.

In this program we built a simple program that navigates the KOMODO around BGU floor.

The robot need to get to the nearest elevator and identify a red object on his front camera.

The proram is seperated to nodes, each is responsible for a cetain function:

1.The robot moves forward until he gets to a distance (user input) from a wall in front of him.

2.The robot rotates in an amount of degrees and direction (-1 is left 1 is right)- both are user input.

3.The robot moves forward for an amout of seconds (user input).

4.The robot searches for a red object in front of him.

The main.py is the node responsible for the entire program run. 

 

