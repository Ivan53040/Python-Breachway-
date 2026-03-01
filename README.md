Python Breachway – CSSE7030 Assignment 2

📌 About

This project is the Python implementation of Breachway, developed as Assignment 2 for the course CSSE7030 Software Engineering Principles and Processes.

It features a complete text-based version of the Breachway game, built with object-oriented design principles and modular structure. The code includes models for game entities, game logic in a dedicated controller, and display routines to interact with the player through the console.

The repository also includes unit tests to verify correctness and help ensure that core features behave as expected.

📋 Overview

Python-Breachway- contains all files needed to run and test your game:

- a2.py – the main game entry point

- display.py – responsible for output and user interaction

- support.py – helper functions and constants

- gameplay/ – core gameplay logic and classes

- levels/ – level definitions supporting progression

- autosave.txt – example game state, used for saving/loading

This structure emphasises separation of concerns and keeps the program organised.

🎮 Game Features

✔ Robust command-line gameplay
✔ Multiple levels with increasing challenge
✔ Well-structured class design (Breachway controllers, entities, utilities)
✔ Input validation for smooth play experience
✔ Game saving and loading support
✔ Automated tests for core logic

🧪 Running Tests

This repository includes automated tests to ensure game mechanics work correctly.

Using an IDE

1. Open the project in your Python-compatible IDE (e.g. PyCharm, VS Code).

2. Locate the tests/ folder.

3. Run all tests via the IDE’s built-in test runner.

Using Command Line

If you have pytest installed:

pip install pytest
pytest

This will discover and run all test cases automatically.

🛠 How to Play

1. Clone the repository:

git clone https://github.com/Ivan53040/Python-Breachway-.git

2. Navigate to the project directory.

3. Run the game:

python a2.py

4. Follow on-screen instructions to play.

📐 Design Principles Demonstrated

- Object-oriented design – classes model ships, hazards, actions

- Modularity – logic separated into clean modules

- Test-driven mindset – tests help ensure behaviour consistency

- Clear user interaction – well-organised display routines

This project is an example of clean and maintainable Python engineering suitable for both coursework and portfolio showcase.

