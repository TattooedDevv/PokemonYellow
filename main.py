import time
import numpy as np
import sys
import vlc


    #audio code from Google
sound_file = vlc.MediaPlayer(r"16_Battle (VS Trainer).mp3")
sound_file.play()
time.sleep(5.5)

print("""
░█▀▀█ █▀▀█ █▀▀█ █──█ 　 █▀▀ █──█ █▀▀█ █── █── █▀▀ █▀▀▄ █▀▀▀ █▀▀ █▀▀▄ 　 ─█▀▀█ █▀▀ █──█ 　 ▀▀█▀▀ █▀▀█ 　 █▀▀█ 
░█─▄▄ █▄▄█ █▄▄▀ █▄▄█ 　 █── █▀▀█ █▄▄█ █── █── █▀▀ █──█ █─▀█ █▀▀ █──█ 　 ░█▄▄█ ▀▀█ █▀▀█ 　 ──█── █──█ 　 █▄▄█ 
░█▄▄█ ▀──▀ ▀─▀▀ ▄▄▄█ 　 ▀▀▀ ▀──▀ ▀──▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀──▀ ▀▀▀▀ ▀▀▀ ▀▀▀─ 　 ░█─░█ ▀▀▀ ▀──▀ 　 ──▀── ▀▀▀▀ 　 ▀──▀ 
                                  █▀▀▄ █▀▀█ ▀▀█▀▀ ▀▀█▀▀ █── █▀▀ █ 
                                  █▀▀▄ █▄▄█ ──█── ──█── █── █▀▀ ▀ 
                                  ▀▀▀─ ▀──▀ ──▀── ──▀── ▀▀▀ ▀▀▀ ▄""")

def delay_print(s):
        # print one character at a time
        # From Chad https://github.com/csfeeser/Python/blob/master/cooltricks.md
        for c in s:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)


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

        # Print fight information
        print(f"\n{self.name}")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        # info on np.mean https://numpy.org/doc/stable/reference/generated/numpy.mean.html
        print("LVL/", 3 * (1 + np.mean([self.attack, self.defense])))

        print("\nVS")

        print(f"\n{rivalPokemon.name}")
        print("TYPE/", rivalPokemon.types)
        print("ATTACK/", rivalPokemon.attack)
        print("DEFENSE/", rivalPokemon.defense)
        print("LVL/", 3 * (1 + np.mean([rivalPokemon.attack, rivalPokemon.defense])))

        time.sleep(2)

        # There are type advantages in Pokemon Fire is weak against water, water is weak against grass, grass is weak
        #against fire.....Fire is strong against grass, Water is strong against fire and grass is strong against water
        version = ['Fire', 'Water', 'Grass', 'Normal']
        # website where I referenced the code below https://realpython.com/python-enumerate/#iterating-with-for-loops-in-python
        for i, k in enumerate(version):
                # rivalPokemon is STRONG
                if rivalPokemon.types == version[(i + 1) % 3]:
                    rivalPokemon.attack *= 2
                    rivalPokemon.defense *= 8
                    self.attack /= 2
                    self.defense /= 2
                    string_1_attack = '\nIts not very effective...'
                    string_2_attack = '\nIts super effective!'

                # rivalPokemon is WEAK
                if self.types == version[(i + 2) % 3]:
                    self.attack *= 4
                    self.defense *= 2
                    rivalPokemon.attack /= 6
                    rivalPokemon.defense /= 2
                    string_1_attack = '\nIts super effective!'
                    string_2_attack = '\nIts not very effective...'

        # Now for the actual fighting...
        # Continue while pokemon still have health
        while (self.bars > 0) and (rivalPokemon.bars > 0):
            # Print the health of each pokemon
            print(f"\n{self.name}\t\tHLTH\t{self.health}")
            print(f"\n{rivalPokemon.name}\t\tHLTH\t{rivalPokemon.health}\n")

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
                delay_print("\n..." + rivalPokemon.name + ' fainted.')
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





            while  self.bars <= 0:
                delay_print("\n..." + self.name + ' fainted.')
                break



        money = np.random.choice(5000)
        delay_print(f"\nOpponent paid you ${money}.\n")






if __name__ == '__main__':
    # Create Pokemon gen 1 dictionary

    Charmander = Pokemon('Charmander', 'Fire', ['Ember', 'Scratch', 'Tackle', 'Fire Punch'],{'ATTACK': 4, 'DEFENSE': 2})
    Squirtle = Pokemon('Squirtle', 'Water', ['Bubblebeam', 'Tackle', 'Headbutt', 'Surf'], {'ATTACK': 3, 'DEFENSE': 3})
    Bulbasaur = Pokemon('Bulbasaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Tackle', 'Leech Seed'],{'ATTACK': 2, 'DEFENSE': 4})
    Eevee = Pokemon('Eevee', 'normal', ['Tackle', 'Bite', 'Take Down', 'Body Slam'], {'ATTACK': 3, 'DEFENSE': 2})

    Squirtle.fight(Eevee)  # Get them to fight
