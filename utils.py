"""
Utility module

"""
import re
import string
import random


def chance(probability, max_range=100):
    """ chance util

    """
    return True if random.choice(range(0, max_range)) >= probability else False


def rand_pos(world_size):
    """ rand_pos util

    """
    return (
        random.choice(range(0, world_size)),
        random.choice(range(0, world_size)),
    )


def inlist_map(iter1, iter2):
   """ inlist_map util

   Compares elements between iterables.
   Returns a list that maps to True or False depending if an element in
   iter1 is found in iter2.

   Useful in conjuction with the `any()` or `all()` functions to determine
   if any or all elements in iter1 are present in iter2.

   """
   return [True if i in iter2 else False for i in iter1]


def name_generator(min_len=3, max_len=6):
    """ name_generator util

    Rules:
    - if name begins with a consonant, it cannot be followed by another
      consonant.
    - max of 2 consonants in series.
    - max of 2 vowels in series.

    """
    VOWELS = 'aeiou'
    CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
    name = random.choice(string.ascii_lowercase)

    def _pick(chars):
        startswith_vowel = True if chars[0] in VOWELS else False
        if len(chars) < 2 and startswith_vowel:
            return random.choice(CONSONANTS)
        elif len(chars) < 2 and not startswith_vowel:
            return random.choice(VOWELS)
        else:
            choice = random.choice(string.ascii_lowercase)

        is_vowel = True if choice in VOWELS else False
        max_vowels = True if all(inlist_map(chars[-2:].lower(), VOWELS)) else False
        max_consonants = True if all(inlist_map(chars[-2:].lower(), CONSONANTS)) else False

        if (not max_vowels and is_vowel) or (not max_consonants and not is_vowel):
            return choice
        else:
            return _pick(chars)

    for i in range(0, random.choice(range(min_len, max_len))):
        name += _pick(name)

    return name.title()
