import random
from datetime import datetime

import settings
import utils


class Humanoid:
    """ Humanoid base class

    """
    stat_modifiers = {
        'hp': 10,
        'ap': 10,
        'hunger': 100,
        'vit': 18,
        'str': 18,
        'int': 18,
    }

    actions = {
        'walk': {
            'type': ['passive'],
            'ap': 0.2,
            'hunger': 5,
            'chance': 50,
        },
        'run': {
            'type': ['defensive', 'passive'],
            'ap': 0.4,
            'hunger': 8,
            'chance': 50,
        },
        'fight': {
            'type': ['defensive', 'agressive'],
            'ap': 0.6,
            'hunger': 15,
            'chance': 50,
        },
        'hunt': {
            'type': ['survival'],
            'ap': 0.6,
            'hunger': 15,
            'chance': 50,
        },
        'mate': {
            'type': ['survival'],
            'ap': 0.4,
            'hunger': 10,
            'chance': 50,
        },
        'rest': {
            'type': ['survival'],
            'ap': 0.0,
            'hunger': 5,
            'chance': 50,
        },
    }

    def __init__(self, birthday, father=None, mother=None):
        self.name = utils.name_generator()
        self.birthday = birthday
        self.deathday = None
        self.age = settings.HUMAN_BIRTH_AGE
        self.sex = random.choice(['M', 'F'])
        self.father = father
        self.mother = mother
        self.spouse = None
        self.position = mother.position if mother else utils.rand_pos(settings.WORLD_SIZE)
        self.mothered = 0

        if isinstance(father, Humanoid) and isinstance(mother, Humanoid):
            parent_vit = self._choose_parent().vitality
            parent_str = self._choose_parent().strength
            parent_int = self._choose_parent().intelligence

            self.vitality = random.choice(range(1, parent_vit + 2)) + (
                random.choice(range(0, parent_vit + 1)) if utils.chance(50) else 0
            )
            self.strength = random.choice(range(1, parent_str + 2)) + (
                random.choice(range(0, parent_str + 1)) if utils.chance(50) else 0
            )
            self.intelligence = random.choice(range(1, parent_int + 2)) + (
                random.choice(range(0, parent_int + 1)) if utils.chance(50) else 0
            )
        else:
            self.vitality = random.choice(range(1, self.stat_modifiers['vit']))
            self.strength = random.choice(range(1, self.stat_modifiers['str']))
            self.intelligence = random.choice(range(1, self.stat_modifiers['int']))

        self.hp = random.choice(range(1, self.stat_modifiers['hp'])) + self.vitality
        self.ap = random.choice(range(1, self.stat_modifiers['ap'])) + (
            int(self.strength * 0.5) + int(self.intelligence * 0.5)
        )
        self.hunger = random.choice(range(40, 70))

    def move(self):
        """ move

        TODO: Right now all move does is change a human's position. What we
              want to achieve are more complex movements as indicated in the
              `actions` property.

        """
        DIRECTION = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            'stay': (0, 0)
        }

        def _pick(pos):
            pos_x, pos_y = pos
            dir_pos = random.choice(list(DIRECTION))
            pos_x += DIRECTION[dir_pos][0]
            pos_y += DIRECTION[dir_pos][1]
            if (
                (pos_x >= 0 and pos_x < settings.WORLD_SIZE) and
                (pos_y >= 0 and pos_y < settings.WORLD_SIZE)
            ):
                return (pos_x, pos_y)
            else:
                return _pick(pos)

        self.position = _pick(self.position)
        return self.position

    def _choose_parent(self):
        return random.choice([self.father, self.mother])

    def __str__(self):
        return '{} ({})'.format(self.name, self.sex)

    def __repr__(self):
        return self.__str__()
