import random
from DC_Talents import *
debug = True

class DrawableObject():
    # pygame stuff
    pass
class Guy(DrawableObject):
    def __init__(self, x, y, xp):
        # position
        self.xPos = x
        self.yPos = y
        self.weapon = Weapon("Dagger of Default", AttackType.MELEE,(1,0,0),[])
        self.armor = Armor("rags of the dissolute",AttackType.MELEE,(1,0,0),[])
        # attributes
        self.strength = 1
        self.agility = 1
        self.cunning = 1
        self.constitution = 1
        self.xp  = xp
        # skills
        self.skills={
            Skills.MELEE_WEAPON :Skill("Melee Weapon", 0, True),
            Skills.RANGED_WEAPON:Skill("Ranged Weapon", 0, False),
            Skills.MAGIC_WEAPON :Skill("Magic", 0, False),
            Skills.SMITH:Skill("Smithing", 0, True),
            Skills.STEALTH:Skill("Stealth", 0, True),
            Skills.TALKING:Skill("Social", 0, True),
            Skills.TALKING:Skill("Tracking", 0, True)
        }
        self.specializations = []
        self.talents = {}
    def attack(self, opponent):
        if self.weapon.type == AttackType.MELEE:
            attribute = self.strength
            rank = self.skills[Skills.MELEE_WEAPON].rank

        if self.weapon.type == AttackType.RANGED:
            attribute = self.agility
        if self.weapon.type == AttackType.MAGIC:
            attribute = self.cunning
        attackDiePool = (attribute, 0, 0)
        damageDiePool = self.weapon.damagePool
        criticalDiePool = (self.cunning, 0, 0)
        s = attackDiePool[0]
        m = attackDiePool[1]
        l = attackDiePool[2]
        for i in range(rank):
            if  s > 0:
                m += 1
                s -= 1
            elif attackDiePool[0] > 0:
                l += 1
                m -= 1
            else:
                s += 1
        attackDiePool = (s,m,l)
        att = Attack(self, type, opponent)
        for key in self.talents:
            talent = talents[key]
            attackDiePool = self.applyCombatTalentDieEffects(att, attackDiePool, DieType.ATTACK)
            damageDiePool = self.applyCombatTalentDieEffects(att, damageDiePool, DieType.DAMAGE)
            criticalDiePool = self.applyCombatTalentDieEffects(att, criticalDiePool, DieType.CRITICAL)
        opponent.defend(self, att, attackDiePool, damageDiePool, criticalDiePool)
    def levelSkill(self,skillEnum):
        skill = self.skills[skillEnum]
        if self.xp>skill.pointsForRankup():
            self.xp-=skill.pointsForRankup()
            skill.rankUp()
    def defend(self, attacker, att, attackDiePool, damageDiePool, criticalDiePool):
        armorDiePool = self.armor.armorPool
        dodgeDiePool = (self.agility, 0, 0)
        counterDiePool = (self.cunning, 0, 0)

        for key in self.talents:
            talent = self.talents[key]
            if talent.type == TalentType.DEFENSIVE:
                self.applyCombatTalentDieEffects(talent, att, attackDiePool, DieType.ATTACK)
                self.applyCombatTalentDieEffects(talent, att, damageDiePool, DieType.DAMAGE)
                self.applyCombatTalentDieEffects(talent, att, criticalDiePool, DieType.CRITICAL)
                self.applyCombatTalentDieEffects(talent, att, armorDiePool, DieType.ARMOR)
                self.applyCombatTalentDieEffects(talent, att, dodgeDiePool, DieType.DODGE)
                self.applyCombatTalentDieEffects(talent, att, counterDiePool, DieType.COUNTER)

        results = self.rollDice(attackDiePool,damageDiePool,criticalDiePool,armorDiePool,dodgeDiePool,counterDiePool)
        #attack, defense, damage, armor, crit, counter
        attacker.handleCriticals(self,results[4])
        self.handleCounters(attacker,results[5])
    def applyCombatTalentDieEffects(self,attack, diePool, dieType):
        ret = diePool
        for key in self.talents:
            talent = self.talents[key]
            if not talent.type == TalentType.CRITICAL and not talent.type == TalentType.COUNTER:
                if talent.condition(attack):
                    for effect in talent.dieEffects:
                        if effect == dieType:
                            ret = effect.applyEffect(diePool)
        return ret

    def handleCriticals(self, defender, critValue):
        for key in self.talents:
            talent = self.talents[key]
            if talent.type == TalentType.CRITICAL:
                if talent.condition(critValue):
                    for effect in talent.otherEffects:
                        effect.enact(self,defender)
    def handleCounters(self, attacker, counterValue):
        for key in self.talents:
            talent = self.talents[key]
            if talent.type == TalentType.COUNTER:
                    if talent.condition(counterValue):
                        for effect in talent.otherEffects:
                            effect.enact(self,attacker)
    def rollDice(self, attackDiePool, damageDiePool, critDiePool, armorDiePool, dodgeDiePool, counterDiePool):
        attack = 0
        for s in range(attackDiePool[0]):
            roll = random.randint(1, 10)
            if roll > 5: attack += 1
        for m in range(attackDiePool[1]):
            roll = random.randint(1, 10)
            if roll > 5: attack += 1
            if roll == 10: attack += 2

        for L in range(attackDiePool[2]):
            roll = random.randint(1, 10)
            if roll > 5: attack += 1
            if roll > 8: attack += 2

        defense = 0
        for s in range(dodgeDiePool[0]):
            roll = random.randint(1, 10)
            if roll > 5: defense += 1
        for m in range(dodgeDiePool[1]):
            roll = random.randint(1, 10)
            if roll > 5: defense += 1
            if roll == 10: defense += 2

        for L in range(dodgeDiePool[2]):
            roll = random.randint(1, 10)
            if roll > 5: defense += 1
            if roll > 8: defense += 2

        damage = 0
        for s in range(damageDiePool[0]):
            roll = random.randint(1, 6)
            if roll > 4: damage += 1
        for m in range(damageDiePool[1]):
            roll = random.randint(1, 6)
            if roll > 3: damage += 1
        for L in range(damageDiePool[2]):
            roll = random.randint(1, 6)
            if roll > 2: damage += 1

        armor = 0
        for s in range(armorDiePool[0]):
            roll = random.randint(1, 6)
            if roll > 4: armor += 1
        for m in range(armorDiePool[1]):
            roll = random.randint(1, 6)
            if roll > 3: armor += 1
        for L in range(armorDiePool[2]):
            roll = random.randint(1, 6)
            if roll > 2: armor += 1

        crit = 0
        for s in range(critDiePool[0]):
            roll = random.randint(1, 20)
            if roll == 20: crit += 1
        for m in range(critDiePool[1]):
            roll = random.randint(1, 20)
            if roll > 18: crit += 1
        for L in range(critDiePool[2]):
            roll = random.randint(1, 20)
            if roll > 15: crit += 1
        counter = 0
        for s in range(counterDiePool[0]):
            roll = random.randint(1, 20)
            if roll == 20: counter += 1
        for m in range(counterDiePool[1]):
            roll = random.randint(1, 20)
            if roll > 18: counter += 1
        for L in range(counterDiePool[2]):
            roll = random.randint(1, 20)
            if roll > 15: counter += 1

        debugPrint("Attack = " + str(attack))
        debugPrint("Defense = " + str(defense))
        debugPrint("Damage = " + str(damage))
        debugPrint("Armor = " + str(armor))
        debugPrint("Critical = " + str(crit))
        debugPrint("Counter = " + str(counter))

        return (attack, defense, damage, armor, crit, counter)
    def move(self):
        print("crap")
class Weapon:
    def __init__(self, name, type, damagePool, effects):
        self.name = name
        self.type = type
        self.damagePool = damagePool
        self.effects = effects
class Armor:
    def __init__(self, name, type, armorPool, effects):
        self.name = name
        self.type = type
        self.armorPool = armorPool
        self.effects = effects
class Skill:
    def __init__(self, name, rank, career):
        self.name = name
        self.rank = rank
        self.career = career

    def rankUp(self, ):
        self.rank += 1

    def pointsForRankup(self):
        cost = self.rank * 5
        if not self.career:
            cost += 5
        return cost

    def gainAsCareerSkill(self):
        self.career = True

class Attack:
    #this is a baby class and if it doesn't grow it will be replaced.
    def __init__(self, attacker, attackType, defender):
        self.weapon = attacker.weapon
        self.attackType = attackType
def debugPrint(s):
    global debug
    if debug:
        print (s)

talents = createTalents()
abe = Guy(1,2,30)
bob = Guy(1,2,3)
abe.talents[TalentName.HEAVY_WEAPON_EXPERT]=talents[TalentName.HEAVY_WEAPON_EXPERT]
abe.talents[TalentName.PUNISHING_DODGE]=talents[TalentName.PUNISHING_DODGE]
bob.talents[TalentName.PUNISHING_DODGE]=talents[TalentName.PUNISHING_DODGE]
abe.levelSkill(Skills.MELEE_WEAPON)
abe.levelSkill(Skills.MELEE_WEAPON)
abe.attack(bob)