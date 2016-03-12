from enum import Enum

class AttackType(Enum):
    MELEE = 1
    RANGED = 2
    MAGIC = 3
class TalentType(Enum):
    DEFENSIVE = 1
    OFFENSIVE = 2
    CRITICAL = 3
    COUNTER = 4
class DieType(Enum):
    ATTACK = 1
    DAMAGE =2
    CRITICAL = 3
    DODGE = 4
    ARMOR = 5
    COUNTER = 6
class Skills(Enum):
    MELEE_WEAPON = 1
    RANGED_WEAPON = 2
    MAGIC_WEAPON = 3
    TALKING = 4
    STEALTH = 5
    SMITH = 6
    TRACKING = 7
class TalentName(Enum):
    HEAVY_WEAPON_EXPERT = 1
    EXECUTIONER = 2
    PUNISHING_DODGE = 3
