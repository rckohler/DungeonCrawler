from Enums import*
from Conditionals import*


def debugPrint(s):
    global debug
    if debug:
        print (s)
#other effect functions
class OtherEffect:
    def __init__(self, name,enact):
        self.name = name
        self.enact = enact
def instagib(attacker, defender):
    debugPrint("your opponent is very very dead.")
def counterThwack(attacker,defender):
    pass
    #defender.attack(attacker)
#Talent Class and subsidiaries
class Talent:
    def __init__(self, name, type, description, prereqs, cost, condition, passive, dieEffects, otherEffects):
        self.type = type
        self.name = name
        self.description = description
        self.prereqs = prereqs
        self.cost = cost
        self.condition = condition
        self.dieEffects = dieEffects
        self.passive = passive
        self.otherEffects = otherEffects
class DieEffect:
    def __init__(self, dieType, changeInNumber, upgraded, downgraded):
        self.dieType = dieType
        self.changeInNumber = dieType
        self.upgraded = upgraded
        self.downgraded = downgraded
        self.changeInNumber = changeInNumber

    def applyEffect(self, diePool):
        s = diePool[0]
        s += self.changeInNumber
        m = diePool[1]
        l = diePool[2]
        if s < 0:
            m+=s
            s = 0
        if m < 0:
            l += m
            m = 0
        if l < 0:
            l = 0
        for k in range(self.upgraded):
            if s > 0:
                m += 1
                s -= 1
            elif m > 0:
                l += 1
                m -= 1

        for j in range(self.downgraded):
            if l > 0:
                l -= 1
                m += 1
            elif m > 0:
                m -= 1
                s += 1
        diePool = (s,m,l)
        return diePool
#Talent Descriptions
def createTalents():
    talents = {}
    name = "Heavy Weapon Expert"
    description = "Big bad ass with less finesse"
    prereqs = {"NONE"}
    cost = 5
    condition = c_meleeHeavyAttack
    passive = True
    effect1 = DieEffect(DieType.DAMAGE, 1,1,0)
    effect2 = DieEffect(DieType.ATTACK, 0, 0, 1)
    effects = {effect1, effect2}
    otherEffects = {}
    talentType = TalentType.OFFENSIVE
    heavyWeaponExpert = Talent(name, talentType, description, prereqs, cost, condition, passive, effects, otherEffects)

    name = "Executioner"
    description = "Violence"
    prereqs = {}
    cost = 5
    condition = c_crit1
    passive = True
    effects = {}
    otherEffect = OtherEffect("gib",instagib)
    otherEffects = {otherEffect}
    talentType = TalentType.CRITICAL
    executioner = Talent(name, talentType, description, prereqs, cost, condition, passive, effects, otherEffects)

    name = "Punishing Dodge"
    description = "Weave, duck and thwack."
    prereqs = {}
    cost = 5
    condition = c_crit1
    passive = True
    effects = {}
    otherEffect = OtherEffect("Counter madness",counterThwack)
    otherEffects = {otherEffect}
    talentType = TalentType.COUNTER
    punishingDodge = Talent(name, talentType, description, prereqs, cost, condition, passive, effects, otherEffects)

    talents = {TalentName.HEAVY_WEAPON_EXPERT: heavyWeaponExpert, TalentName.EXECUTIONER: executioner, TalentName.PUNISHING_DODGE:punishingDodge}
    return talents
