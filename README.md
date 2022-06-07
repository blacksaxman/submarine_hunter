# submarine_hunter
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
