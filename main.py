import time
import numpy as np
import pygame
from slowprint.slowprint import *

pygame.init()


class Music:
    def __init__(self):
        pygame.mixer.init()

        self.opening_track = pygame.mixer.Sound("music/02_Opening (part 2).mp3")
        self.rival_track = pygame.mixer.Sound("music/06_Rival Appears.mp3")
        self.battle_track = pygame.mixer.Sound("music/16_Battle (VS Trainer).mp3")
        self.victory_track = pygame.mixer.Sound("music/17_Victory (VS Trainer).mp3")
        self.current_track = self.opening_track

    def play(self, track_name):
        self.current_track.stop()
        self.current_track = self.__dict__.get(track_name)
        self.current_track.set_volume(0.1)
        self.current_track.play(loops=-1)

    def stop(self):
        self.current_track.stop()


music = Music()


def delay_print(s):
    # print one character at a time
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)


# Making the pokemon class with stats for user pokemon
# initialize the pokemon class and attributes
class Pokemon:

    # reference https://python-forum.io/Thread-Game-Logic-Pokemon-like-type-advantages-in-python
    def __init__(self, name, types, moves, EVs, health='==================='):
        # save variables as attributes

        self.name = name
        self.types = types
        self.moves = moves
        self.attack = EVs['ATTACK']
        self.defense = EVs['DEFENSE']
        self.health = health
        self.bars = 20  # Amount of health bars

    def fight(self, rivalPokemon):
        # Allow the pokemon to fight each other
        music.play("battle_track")
        # Print fight information
        print(f"\n{self.name}")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("LVL/", 3 * (1 + np.mean([self.attack, self.defense])))

        print("\nVS")

        print(f"\n{rivalPokemon.name}")
        print("TYPE/", rivalPokemon.types)
        print("ATTACK/", rivalPokemon.attack)
        print("DEFENSE/", rivalPokemon.defense)
        print("LVL/", 3 * (1 + np.mean([rivalPokemon.attack, rivalPokemon.defense])))

        time.sleep(2)

        version = ['Fire', 'Water', 'Grass', 'Normal']
        # website where I referenced the code below
        # https://realpython.com/python-enumerate/#iterating-with-for-loops-in-python
        for i, k in enumerate(version):
            # rivalPokemon is STRONG
            if rivalPokemon.types == version[(i + 1) % 3]:
                rivalPokemon.attack *= 4
                rivalPokemon.defense *= 6
                self.attack /= 2
                self.defense /= 6
                string_1_attack = '\n You Pokemons went down!'
                string_2_attack = '\nSuper effective'

            # rivalPokemon is WEAK
            if self.types == version[(i + 2) % 3]:
                self.attack *= 4
                self.defense *= 3
                rivalPokemon.attack /= 4
                rivalPokemon.defense /= 6
                string_1_attack = '\nCritical Hit!'
                string_2_attack = '\n Not very effective!'

        # Now for the actual fighting...
        # Continue while pokemon still have health
        time.sleep(3)
        while (self.bars > 0) and (rivalPokemon.bars > 0):
            # Print the health of each pokemon
            print(f"\n{self.name}\t\tHLTH\t{self.health}")
            print(f"\n{rivalPokemon.name}\t\tHLTH\t{rivalPokemon.health}")

            print(f"Go {self.name}!")
            for i, x in enumerate(self.moves):
                print(f"{i + 1}.", x)
            index = int(input('Pick a move: '))
            delay_print(f"\n{self.name} used {self.moves[index - 1]}!")
            time.sleep(1)
            delay_print(string_1_attack)

            # Determine damage
            rivalPokemon.bars -= self.attack
            rivalPokemon.health = ""

            # Add back bars plus defense boost
            for j in range(int(rivalPokemon.bars + .1 * rivalPokemon.defense)):
                rivalPokemon.health += "="

            time.sleep(1)
            print(f"\n{self.name}\t\tHLTH\t{self.health}")
            print(f"\n{rivalPokemon.name}\t\tHLTH\t{rivalPokemon.health}\n")
            time.sleep(.5)

            # Check to see if Pokemon fainted
            if rivalPokemon.bars <= 0:
                delay_print("\n..." + rivalPokemon.name + ' fainted.\n')
                self.victory()
                break

            # rivalPokemon's turn

            print(f"Go {rivalPokemon.name}!")
            for i, x in enumerate(rivalPokemon.moves):
                print(f"{i + 1}.", x)
            index = int(input('Pick a move: '))
            delay_print(f"{rivalPokemon.name} used {rivalPokemon.moves[index - 1]}!")
            time.sleep(1)
            delay_print(string_2_attack)

            # Determine damage
            self.bars -= rivalPokemon.attack
            self.health = ""

            # Add back bars plus defense boost
            for j in range(int(self.bars + .1 * self.defense)):
                self.health += "="

            time.sleep(1)
            print(f"{self.name}\t\tHLTH\t{self.health}")
            print(f"{rivalPokemon.name}\t\tHLTH\t{rivalPokemon.health}\n")
            time.sleep(.5)

            while self.bars <= 0:
                delay_print("\n..." + self.name + ' fainted.')
                break

    def victory(self):
        music.play("victory_track")
        money = np.random.choice(5000)
        delay_print("\nOkay! I'll make my Pokémon fight to toughen it up! Ash! Gramps! Smell you later!")
        delay_print(f"\nOpponent paid you ${money}.\n")
        time.sleep(10)


pokemon_choices = [

    Pokemon('Charmander', 'Fire', ['Ember', 'Scratch', 'Tackle', 'Fire Punch'], {'ATTACK': 4, 'DEFENSE': 4}),
    Pokemon('Squirtle', 'Water', ['Bubblebeam', 'Tackle', 'Headbutt', 'Surf'], {'ATTACK': 5, 'DEFENSE': 4}),
    Pokemon('Bulbasaur', 'Grass', ['Vine Whip', 'Razor Leaf', 'Tackle', 'Leech Seed'], {'ATTACK': 3, 'DEFENSE': 5}),
    Pokemon('Eevee', 'normal', ['Tackle', 'Bite', 'Take Down', 'Body Slam'], {'ATTACK': 4, 'DEFENSE': 3})

]


def pokemon_starter():
    music.play("opening_track")
    delay_print("Hello there! Welcome to the world of Pokémon! My name is Oak! People call me the Pokémon "
                "Prof! This world is inhabited by creatures called Pokémon! For some people, Pokémon are "
                "pets. Other use them for fights. \nMyself… I study Pokémon as a profession. First, "
                "what is your name? Right! So your name is Ash! \nThis is my grandson. He's been your rival "
                "since you were a baby. …Erm, what is his name again? That's right! I remember now! His name "
                "is Gary!\nYour very own Pokémon legend is about to unfold! A world of dreams and "
                "adventures with Pokémon awaits! Let's go!\n")
    starter = (int(input('Which pokemon will you choose? 1.Charmander, 2.Squritle, 3.Bulbasaur  \n')))
    return pokemon_choices[starter - 1]
    time.sleep(1)


def rival_appears():
    music.play("rival_track")
    delay_print("Wait Ash! Let's check out our Pokémon! Come on, I'll take you on!\n")
    time.sleep(5)
    return pokemon_choices[3]


def main():
    player = pokemon_starter()
    rival = rival_appears()
    player.fight(rival)
    music.stop()
    quit()


if __name__ == '__main__':
    main()

#[src/libmpg123/id3.c:482] error: No comment text / valid description?