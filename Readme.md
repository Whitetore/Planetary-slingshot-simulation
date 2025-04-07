# Gravitational Slingshot Effect

This project simulates a gravitational slingshot effect using Pygame, where spacecraft can interact with a planet (Jupiter) and use its gravity to gain velocity. It features basic physics like gravitational attraction, velocity, and movement based on user input.

## Features
- Simulate the gravitational effect of Jupiter on spacecraft.
- The spacecraft's movement is controlled by mouse clicks, which determine the initial trajectory.
- Displays the spacecraft's speed, distance from the planet, and the gravitational force acting on it.
- Option to pause the simulation by pressing the `TAB` key.
- Allows for multiple spacecraft to be added and tracked at once.

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone or download this repository.
2. Install Python and Pygame if not already installed:
    ```bash
    pip install pygame
    ```
3. Download an image of Jupiter (`jupiter.png`) and place it in the same directory as the Python script.

## How to Run
1. Run the `main.py` script:
    ```bash
    python main.py
    ```
2. Click anywhere on the screen to spawn a spacecraft. The spacecraft will move according to the gravitational pull of the planet.
3. Press the `TAB` key to pause/resume the simulation.

## Controls
- **Mouse Click**: Spawn spacecraft at the clicked position with an initial velocity toward the mouse pointer.
- **TAB Key**: Pause or resume the simulation.

## Physics Overview
The program uses Newton's law of gravitation to calculate the force between the spacecraft and the planet, updating the spacecraft's velocity and position accordingly. The gravitational constant (G) is set, and the scale factor translates meters to pixels for visualization.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
