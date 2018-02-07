What started as a fork is now a complete rewrite. Naturally.


to get some output, try:

python3 tetris_engine.py

Note that this will thrash the hell out of your CPU and write > 200 images to your disk. Also, the convolved screen is yellow, and I'm not sure why yet.





Old README:

gym-tetris
******

Tetris OpenAI gym environment.

Installing everything
---------------------

gym_tetris requires PyGame installed:

On OSX:

.. code:: shell

    brew install sdl sdl_ttf sdl_image sdl_mixer portmidi  # brew or use equivalent means
    conda install -c https://conda.binstar.org/quasiben pygame  # using Anaconda

On Ubuntu 14.04:

.. code:: shell

    apt-get install -y python-pygame

More configurations and installation details on: http://www.pygame.org/wiki/GettingStarted#Pygame%20Installation

And finally clone and install this package

.. code:: shell

    git clone https://github.com/lusob/gym-tetris.git 
    cd gym-tetris/
    pip install -e .

Example
=======

Run ``python example.py`` file to play tetris game with a random_agent (you need to have installed openai gym).

