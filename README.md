# Guerreiros Integrais

![A screenshot showing the game title](https://raw.githubusercontent.com/vito0182/trabalho-lp-a2/main/titlescreen_screenshot.png)

Made by Anne Cardoso, Larissa Lemos, Pedro Tokar and Vitor do Nascimento.

## Introduction

This game is our work for the second evaluation in the Programming Languages
subject, lectioned at the second semester of the courses Data Science and Applied
Mathematics in FGV - EMAp.

During the second part of the PL course, we learnt about __Object Oriented
Programing__ concepts, in parallel with applying them to Python programs. This
work aims to show the concepts we learnt so far (like encapsulation and
inheritance) applied in a game, developed entirely by us.

## About the game

In this game, you control a brave warrior that should fight against evil integrals
in a notebook. This fight never ends, like the pain in solving hard triple integrals
in calculus II classes. The game objective is to defeat the maximum amount of
integrals you can, lasting as long as possible without dying. You can move the
player with the **WASD keys**, shoot with the **right mouse button** and change
guns using the **mouse scroll**, you can also dash when pressing **spacebar button**.

![A screenshot showing the game.](https://raw.githubusercontent.com/vito0182/trabalho-lp-a2/main/gameplay_screenshot.png)

The game genre chosen by the group was a top-down shooter, decided after voting.
This game uses concepts like maps, a player, enemy, weapons, guns, etc., and all
of these are represented as classes in the code. There is also a game loop,
responsible for accounting the endless events that can occur each frame, like
a gun being shot and a player taking damage.

## Running

In order to run the game, you need to have [Python](https://www.python.org/)
installed (version 3.9 or higher) in your system. How to install python differs
greatly from operational system to operational system. Once you have installed
python, you also need the [pygame](https://www.pygame.org/news) library. The
library abstracts a lot of things involving creating windows and drawing in them.

To install it, you can run on your terminal, from the project root:

```shell {"id":"01HH9N9BC3FX76SVKDJJVRCT45"}
$ pip install - r requirements.txt
```

After that, you have all the necessary things to run the game. So, to do it, run:

```sh {"id":"01HH9N9BC3FX76SVKDJK44J0C7"}
$ python src/main.py
```

## Documentation

You can see the documentation at [Guerreiros Integrais](https://vito0182.github.io/trabalho-lp-a2/build/html/index.html).

# Sources

All the sprites were created by us.

The sounds effects were generated using the website [JSFXR](https://sfxr.me/)

The music was taken from [Iron Main - Black Sabbath free MIDI](https://www.midis101.com/free-midi/40824-black-sabbath-iron-man) and converted to wav using GXSCC and audacity
