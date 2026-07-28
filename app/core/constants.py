# ==========================================================
# Application constants.
# ==========================================================

from dataclasses import dataclass


@dataclass(frozen=True)
class PropertyOption:
    id: int | str | bool
    label: str
    icon: str


# ==========================================================
# Difficulty
# ==========================================================

DIFFICULTY_BEGINNER = 1
DIFFICULTY_NORMAL = 2
DIFFICULTY_HARD = 3

DIFFICULTY_CHOICES = [
    PropertyOption(DIFFICULTY_BEGINNER, "Beginner", "difficulty-1"),
    PropertyOption(DIFFICULTY_NORMAL, "Normal", "difficulty-2"),
    PropertyOption(DIFFICULTY_HARD, "Hard", "difficulty-3"),
]


# ==========================================================
# Distance
# ==========================================================

DISTANCE_SHORT = 1
DISTANCE_MEDIUM = 2
DISTANCE_LONG = 3

DISTANCE_CHOICES = [
    PropertyOption(DISTANCE_SHORT, "1-2 km", "distance-short"),
    PropertyOption(DISTANCE_MEDIUM, "3-5 km", "distance-medium"),
    PropertyOption(DISTANCE_LONG, "6+ km", "distance-long"),
]


# ==========================================================
# Language
# ==========================================================

LANGUAGE_EN = "en"
LANGUAGE_UK = "uk"
LANGUAGE_RU = "ru"

LANGUAGE_CHOICES = [
    PropertyOption(LANGUAGE_EN, "English", "lang-en"),
    PropertyOption(LANGUAGE_UK, "Українська", "lang-uk"),
    PropertyOption(LANGUAGE_RU, "Русский", "lang-ru"),
]


# ==========================================================
# Player mode
# ==========================================================

PLAYER_SOLO = 1
PLAYER_TEAM = 2
PLAYER_BOTH = 3

PLAYER_MODE_CHOICES = [
    PropertyOption(PLAYER_SOLO, "Solo", "solo"),
    PropertyOption(PLAYER_TEAM, "Team", "team"),
    PropertyOption(PLAYER_BOTH, "Solo / Team", "solo-team"),
]


# ==========================================================
# Duration
# ==========================================================

DURATION_SHORT = 1
DURATION_MEDIUM = 2
DURATION_LONG = 3

DURATION_CHOICES = [
    PropertyOption(DURATION_SHORT, "<1 h", "duration-short"),
    PropertyOption(DURATION_MEDIUM, "1-2 h", "duration-medium"),
    PropertyOption(DURATION_LONG, "2+ h", "duration-long"),
]


# ==========================================================
# Age
# ==========================================================

AGE_0 = 1
AGE_6 = 2
AGE_10 = 3
AGE_16 = 4
AGE_18 = 5

AGE_GROUP_CHOICES = [
    PropertyOption(AGE_0, "0+", "age-0"),
    PropertyOption(AGE_6, "6+", "age-6"),
    PropertyOption(AGE_10, "10+", "age-10"),
    PropertyOption(AGE_16, "16+", "age-16"),
    PropertyOption(AGE_18, "18+", "age-18"),
]

# ==========================================================
# ALLOW REPLAY
# ==========================================================

ALLOW_REPLAYS_YES = True
ALLOW_REPLAYS_NO = False

ALLOW_REPLAYS_CHOICES = [
    PropertyOption(ALLOW_REPLAYS_YES, "Allowed", "allow-replays-yes"),
    PropertyOption(ALLOW_REPLAYS_NO, "Only once", "allow-replays-no"),
]


PROPERTY_OPTIONS = {
    "difficulty": DIFFICULTY_CHOICES,
    "distance": DISTANCE_CHOICES,
    "language": LANGUAGE_CHOICES,
    "player_mode": PLAYER_MODE_CHOICES,
    "duration": DURATION_CHOICES,
    "age_group": AGE_GROUP_CHOICES,
    "allow_replays": ALLOW_REPLAYS_CHOICES,
}

PROPERTY_DEFAULTS = {
    "difficulty": DIFFICULTY_NORMAL,
    "distance": DISTANCE_MEDIUM,
    "language": LANGUAGE_RU,
    "player_mode": PLAYER_BOTH,
    "duration": DURATION_MEDIUM,
    "age_group": AGE_0,
    "allow_replays": ALLOW_REPLAYS_YES,
}