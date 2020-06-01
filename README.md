# Genetic Algorithm for a simple video game

## Disclaimer
This project is mainly for fun and the code is very bad. I wanted to make the game playable by people and at the same time implement the genetic algorithm. As I wasn't familiar with the pygame module beforehand, this ended up in limiting the genetic algorithm tricks that could have been implemented for better convergence to the goal.

## Requirements
The pygame module

## Description 
In the python file, we code a simple video game. The player moves a circle with the keyobard arrows and the goal is to reach the red circle on the bottom right of the window. There are some obstacles on the way that need to be passed around.

![ScreenShot](/images/Screenshot_90.png)

***
At the same time, we use a genetic algorithm to have the computer beat the game on each own. Here are some screenshots of a run the reached the goal in 45 generations:

![ScreenShot](/images/Screenshot_10.png)
![ScreenShot](/images/Screenshot_20.png)
![ScreenShot](/images/Screenshot_30.png)
![ScreenShot](/images/Screenshot_40.png)
![ScreenShot](/images/Screenshot_50.png)
![ScreenShot](/images/Screenshot_60.png)
![ScreenShot](/images/Screenshot_70.png)
![ScreenShot](/images/Screenshot_80.png)

If the circle follow the shortest path going below the first obstacle, it takes them around 40 generations to reach the goal. But if they take the path above the first obstacle, then they get stuck on top of the second obstacle and then they might spend upwards of 300 generations to discover a novelty that gets them around it!
