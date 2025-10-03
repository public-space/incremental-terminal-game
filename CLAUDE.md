🎮 Prompt for Claude: Terminal Idle Game in Python

You are going to design and code a terminal-based incremental/idle game in Python, inspired by games like NGU Industries, Universal Paperclips, Age of Empires, and classic ASCII roguelike aesthetics.

Requirements:

Game Loop & Structure

Tick-based system (e.g. every second) that updates resources and game state.

Idle mechanics: resources generate automatically once unlocked.

Balance progression: early actions should feel meaningful but not too fast.

Ability to save/load games to a local file.

Theme

You can invent a fresh theme (medieval kingdom, space colony, AI research, post-apocalypse, etc.) or remix an existing one like Paperclips.

It should be flexible enough to expand with more units/buildings/upgrades later.

Interface

ASCII graphics and simple animations (progress bars, blinking characters, cycling frames).

Use colorama or another terminal coloring library to make the UI visually appealing.

Split the screen into main game area (resources, upgrades, units) and menu/command area (player input).

Commands should be simple (single letters like B to build, U to upgrade, S to save, Q to quit).

Gameplay

Player starts with a small pool of resources (e.g., wood, stone, food, or abstract equivalents).

Resources can be spent to unlock producers (workers, machines, farms, factories).

Producers generate more resources over time, unlocking exponential growth.

Add at least 3 layers of progression: base resource → intermediate resource → advanced unlocks.

Include some upgrades or tech tree elements to make choices interesting.

Polish

Include ASCII animations (like a little worker icon moving, or blinking text when a building is producing).

Balance numbers so the game feels rewarding in the first 10 minutes but can be left running longer.

Code should be modular and easy to extend (split functions into sections for UI, game state, save/load, tick updates).

Extra (Optional but Nice)

Random events (small boosts or setbacks).

Prestige/reset mechanic.

Fun flavor text or jokes in the style of NGU.

Deliverable:

A small python  project structure.

Must run in Linux terminal (Ubuntu/Fedora/Arch).

Uses only standard libraries plus optional lightweight ones (colorama, blessed, etc.).

Should start with a menu: New Game / Load Game / Quit.

Each aspect and function should be in its own python file for maximum organization, modularability, and readable clean code. 
This will help us with later expansion. 

Keep a log file in markdown of each major change and include a timestamp. 

include a readme about the project. 

include instructions on how to install and run. 
make it without a virtual environment. 
include a script that can auto run and set it up. 
so the user can just enter: 
./name-of-game

Include a markdown file in which you keep track of all the mechanics, interactions, stats, and
formulas. 

include a tutorial/devlog on how the game is made. 
Include extensive error handling and debugging so the game doesn't crash and so we can figure
out what's wrong and fix it promptly. 

there should be a game screen and menus. 

very clean animations so the user knows something is happening. 
as well as clear indiciators of numbers and stats. 
dialogs to let the user know what to do in the beginning and to give hints along the way. 
Good menus and colors all around. 

You may pull from whatever resources you like. It is up to your discretion and imagination :)

I'm looking forward to seeing what you come up with!

-Donovan (User and Dev)
