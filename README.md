# Snake Game

A modern twist on the classic snake game, featuring customizable themes, challenging game modes, and dynamic sprite-based visuals.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Story](#project-story)
- [Challenges](#challenges)
- [License](#license)

## Overview

This project is a reimagined version of the traditional snake game. It incorporates modern design elements, such as custom sprites for the snake (head, body, and tail), customizable themes (green, black, and white backgrounds), and two distinct game modes: Classic and Challenge. The Challenge mode introduces obstacles that are added each time the snake eats an apple, increasing the game’s difficulty dynamically.

![image](https://github.com/user-attachments/assets/89f6fab1-c0dd-47dc-89f0-e155ce628f48)


## Features

- **Customizable Themes:**  
  Choose from green, black, or white backgrounds, with matching text colors.
  
- **Sprite-Based Visuals:**  
  The game uses custom sprites for the snake's head, body (including curves), tail, and the apple.
  
- **Multiple Game Modes:**  
  - **Classic Mode:** Standard snake gameplay without permanent obstacles.  
  - **Challenge Mode:** New obstacles are added every time the snake consumes an apple.
  
- **Dynamic Difficulty:**  
  The game speed increases every 5 points, challenging your reflexes as you progress.
  
- **High Score Tracking:**  
  Saves and displays the top 5 scores using file I/O.

## Technologies Used

- **Language:** Python
- **Framework/Library:** Pygame (for graphics, event handling, and overall game development)
- **Platform:** Desktop (cross-platform)
- **Other Technologies:**  
  - File I/O for saving high scores  
  - Custom sprite assets for enhanced visuals

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/snake-game.git
   cd snake-game

2.Install Dependencies:

Make sure you have Python installed (Python 3.x recommended). Install Pygame using pip:
   ```bash
    pip install pygame
  ```

Assets:

Ensure the assets folder is in the root directory of the project and contains the following files:

apple.png
head_up.png
head_down.png
head_left.png
head_right.png
tail_up.png
tail_down.png
tail_left.png
tail_right.png
body_horizontal.png
body_vertical.png
body_topleft.png
body_topright.png
body_bottomleft.png
body_bottomright.png
Usage
Run the game by executing the main Python file:

bash
```
python Snake.py
```
Navigate through the main menu using the keyboard:

Press 1 to start the game.
Press I for instructions.
Press S to open settings and change the theme.
Press Q to quit.
During the game, use the arrow keys to control the snake. In Challenge mode, avoid the obstacles that appear with each apple eaten.

Project Story
Inspiration
This project was inspired by a love for retro games and a desire to enhance a timeless classic. The simplicity and addictiveness of the original snake game motivated me to modernize it with updated graphics, new gameplay mechanics, and customizable features.

What I Learned
Game Development:
Gained experience with game loops, event handling, collision detection, and sprite management in Pygame.

Modular Programming:
Improved code organization by dividing the project into classes and modular functions.

User Experience:
Explored how customizable themes and dynamic difficulty can enhance player engagement.

How I Built It
I started with planning the game mechanics and features.
Incremental development allowed me to build and test each component separately.
I integrated custom sprite assets and handled complex sprite rotations and curves.
I iterated on the design based on testing feedback, especially around curve transitions.
Challenges Faced
Sprite Alignment:
Adjusting the logic to ensure that the correct curve sprites appear when the snake turns, particularly for up and down movements.

Code Organization:
Balancing modularity with responsiveness in the game loop.

Customizability:
Implementing customizable themes and dynamic difficulty while maintaining intuitive user interactions.

License
This project is licensed under the MIT License. 
