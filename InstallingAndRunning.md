# Introduction #

Purruyura is a command line blackjack game.  It is mostly intended as  a demo for using cmd, but as a pleasant side effect, you can play blackjack, too.  The computer-dealer stands on 17


# Details #

Installing is as simple as downloading.  On linux-like boxes with python located at /user/bin/python running the game may be as simple as typing "./purruyura.py"

If that doesn't work, try these steps:
  * Type "python" and make sure a python prompt appears (type quit() to exit python)
  * Type "chmod a+x purruyura.py" Make sure you really want to give everyone execute permission for this file first, modify the command as needed
  * Try "python purruyura.py" if the first two steps worked

Assuming the above troubleshooting steps have worked, and "./purruyura.py" doesn't work, type "which python" to get an idea of what to change the shebang to.

# Usage #

Actually playing the game is fairly straight forward.  Typing "help" will give a list of available commands.  During your turn (which is when you are able to give commands) type hit or stand to do something.  Type exit if you are fed up at any point.