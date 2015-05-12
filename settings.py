"""
Sangkatauhan Settings

"""

DAY_DURATION = 5  # simulated days in secs
DAYS_IN_YEAR = 365

HUMAN_INIT_MIN = 5  # min humans on initialization
HUMAN_INIT_MAX = 99  # max humans on initialization
HUMAN_BIRTH_AGE = 13 * DAYS_IN_YEAR  # age at birth (simplified)
HUMAN_MAX_AGE = 99 * DAYS_IN_YEAR  # max age (simplified)
HUMAN_FEMALE_MOTHERHOOD = int(DAYS_IN_YEAR * 0.7)  # days when females can't give birth
HUMAN_FEMALE_SEX_MAX_AGE = 50  # max age females can give birth
HUMAN_MALE_SEX_MAX_AGE = 80  # max age males can procreate

WORLD_INIT_AGE = 0
WORLD_MAX_AGE = 1024 * DAYS_IN_YEAR  # days before the world ends
WORLD_SIZE = 1024  # world size in square points i.e. 32x32
