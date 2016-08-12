from Enums import*
from Conditionals import*
debug = True

def debugPrint(s):
    global debug
    if debug:
        print (s)
class OtherEffect:
    def __init__(self, name,enact,effectType):
        self.name = name
        self.otherEffectType = effectType
        self.enact = enact
#other effect functions
def instagib(attacker, defender):
    defender.constitution=0
    print("instagibbed")
def counterThwack(defender,attacker):
    print ("counter thwack: Thwacker = " + defender.name + " Thwackee = " + attacker.name)
    defender.attack(attacker)
def constantValue(n):
    return n
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
    name = "Heavy Weapon Expert"
    description = "Big bad ass with less finesse"
    prereqs = []
    cost = 5
    condition = c_meleeHeavyAttack
    passive = True
    effect1 = DieEffect(DieType.DAMAGE, 2, 2,0)
    effect2 = DieEffect(DieType.ATTACK, 0, 0, 1)
    effects = [effect1, effect2]
    otherEffects = []
    talentType = TalentType.OFFENSIVE
    heavyWeaponExpert = Talent(name, talentType, description, prereqs, cost, condition, passive, effects, otherEffects)

    name = "Executioner"
    description = "Violence"
    prereqs = {}
    cost = 5
    condition = c_crit1
    effect1 = DieEffect(DieType.DAMAGE, 2, 2,0)
    passive = True
    effects = {effect1}
    otherEffect = OtherEffect("gib",instagib,False)
    otherEffects = [otherEffect]
    talentType = TalentType.CRITICAL
    executioner = Talent(name, talentType, description, prereqs, cost, condition, passive, effects, otherEffects)

    name = "Punishing Dodge"
    description = "Weave, duck and thwack."
    prereqs = []
    cost = 5
    condition = c_crit1
    passive = True
    effects = []
    otherEffect = OtherEffect("Counter madness",counterThwack,False)
    otherEffects = [otherEffect]
    talentType = TalentType.COUNTER
    punishingDodge = Talent(name, talentType, description, prereqs, cost, condition, passive, effects, otherEffects)

    name = "Iron Skin"
    description = "Cliche I know."
    prereqs = []
    cost = 5
    condition = none
    passive = True
    effects = []
    otherEffect = OtherEffect("Resilience",constantValue(1),TalentType.DAMAGE_SOAK)
    otherEffects = [otherEffect]
    talentType = TalentType.DAMAGE_SOAK
    ironSkin = Talent(name, talentType, description, prereqs, cost, condition, passive, effects, otherEffects)

    talents = {
        TalentName.HEAVY_WEAPON_EXPERT: heavyWeaponExpert,
        TalentName.EXECUTIONER: executioner,
        TalentName.PUNISHING_DODGE:punishingDodge,
        TalentName.IRON_SKIN:ironSkin
    }
    return talents
