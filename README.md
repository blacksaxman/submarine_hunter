# submarine_hunter

**IMPORTANT** you need to install termcolor for this game to run!  You can install
from powershell using:
```
pip install termcolor
```

This is the repo for an example of a turn based "Battleship"-like game in python

It does not have a GUI but does make use of clever techniques to display
"graphics" to the user in the terminal.  The subtitle "ASCII but deadly" is a
subtle nod to this fact.

I've tried to comment the code well, but please look through and see things you
don't understand and we can explain how they are used or why they are used.

When creating a game, you can make it as simple or as complex as you would like.
This code is not particularly complex, however the logic behind the code is the
majority of the difficulty.  In the expand.py file you'll see many nested for
loops that check conditions and update the state of objects.  You'll also see
class objects defined.  These classes make it easier to keep track of different
objects without having to manually define them yourselfs each time.

Concepts like these build upon the basic Python knowledge each of you should
have at this point and you should feel comfortable at least taking a look at the
code even if you don't fully understand what is going on.

To run the game just type:
```
python main.py
```

Useful links on concepts used in this game, because **knowledge is _POWER_**:
1. [Classes (aka objects) in Python](https://www.w3schools.com/python/python_classes.asp)
2. [termcolor (for adding color to your game)](https://pypi.org/project/termcolor/)
3. [Implementing pauses in python using time.sleep](https://www.programiz.com/python-programming/time/sleep)
4. [Figuring out your python terminal size](https://www.geeksforgeeks.org/python-os-get_terminal_size-method/)
5. [2-dimensional lists in Python (see combatGrid variable in expand.py)](https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/)
