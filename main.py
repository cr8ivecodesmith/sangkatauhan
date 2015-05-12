"""
Sangkatauhan

"""
import random
from datetime import datetime, timedelta

import settings
from core.humanoid import Humanoid


def process_encounters(encounters, humans, world_age):
    dead_humans = set()
    for enc in iter(encounters):
        p1, p2 = enc

        if (p1.sex == p2.sex) or p1.spouse != p2 or p2.spouse != p1:
            # TODO: Either humans will fight, hunt food, or just be passive
            continue

        # Humans procreate
        father = p1 if p1.sex == 'M' else p2
        mother = p1 if p1.sex == 'F' else p2

        if mother.mothered > 0 and (
            mother.age > settings.HUMAN_FEMALE_SEX_MAX_AGE and
            father.age > settings.HUMAN_MALE_SEX_MAX_AGE
        ):
            continue

        father.spouse = mother
        mother.spouse = father
        child = Humanoid(world_age, father=father, mother=mother)
        mother.mothered = settings.HUMAN_FEMALE_MOTHERHOOD
        humans.add(child)

        print('[{:%Y-%m-%d %H:%M:%S}] {} eloped {} and gave birth to {}!'.format(
            datetime.now(),
            father,
            mother,
            child
        ))

    return (humans, dead_humans)


def main():
    # Init counters
    world_age = settings.WORLD_INIT_AGE
    living_humans = set(
        [Humanoid(world_age)
         for i in range(0, random.choice(range(settings.HUMAN_INIT_MIN, settings.HUMAN_INIT_MAX)))]
    )
    dead_humans = set()
    human_encounters = set()
    start_time = datetime.now()
    world_start_time = start_time

    msg = '[{:%Y-%m-%d %H:%M:%S}] world age: {} living: {} dead: {} encounters: {}'.format(
        datetime.now(),
        world_age,
        len(living_humans),
        len(dead_humans),
        len(human_encounters)
    )
    print(msg)

    # Begin game loop
    while world_age <= settings.WORLD_MAX_AGE or living_humans:
        current_time = datetime.now()

        # Check if an encounter occurs
        for human in iter(living_humans):
            for other in iter(living_humans.difference(set([human]))):
                if human.position == other.position:
                    human_encounters.add((human, other))

        # Process encounters
        living_humans, dead_queue = process_encounters(human_encounters, living_humans, world_age)

        # Move
        for human in iter(living_humans):
            human.move()
            msg = '[{:%Y-%m-%d %H:%M:%S}] {} moved to {}'.format(
                datetime.now(),
                human,
                human.position
            )

        # Check for end of day
        if (current_time - start_time) > timedelta(seconds=settings.DAY_DURATION):
            # Update status of mothered females
            for human in iter(living_humans):
                if human.sex == 'F' and human.mothered > 0:
                    human.mothered -= 1

            # Update human age and kill the old ones.
            dead_humans.update(dead_queue)
            for human in iter(living_humans):
                human.age += 1
                if human.age >= settings.HUMAN_MAX_AGE:
                    human.deathday = world_age
                    dead_humans.add(human)

            # Update living humans and spouse attribute
            living_humans = living_humans.difference(dead_humans)
            for human in iter(living_humans):
                if human.spouse in dead_humans:
                    human.spouse = None

            # Log EOD stats
            msg = '[{:%Y-%m-%d %H:%M:%S}] world age: {} living: {} dead: {} encounters: {}'.format(
                datetime.now(),
                world_age,
                len(living_humans),
                len(dead_humans),
                len(human_encounters)
            )
            print(msg)

            # Re-initialize counters
            start_time = datetime.now()
            world_age += 1
            human_encounters.clear()


    if not living_humans and world_age < settings.WORLD_MAX_AGE:
        print('Human beings have died out before the world perished!')
    if living_humans and world_age >= settings.WORLD_MAX_AGE:
        print('The world has perished and human beings will soon die!')

    print('End.')


if __name__ == '__main__':
    main()
