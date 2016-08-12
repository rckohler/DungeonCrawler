import random
import pygame
from Specializations import *
import math
debug = False
gHits = 0
class PhysicalObject(pygame.sprite.Sprite):
    def __init__(self, color, width, height, xPos, yPos, allSpritesList):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos
        self.destinationX = xPos
        self.destinationY = yPos
        self.vx = 0
        self.vy = 0
        self.maxSpeed = 10
        allSpritesList.add(self)
    def setDestination(self,x,y):
        self.destinationX = x
        self.destinationY = y
        self.setVelocities()
    def setVelocities(self):
        dx = self.destinationX-self.rect.x
        dy = self.destinationY-self.rect.y
        d = math.pow(dx*dx+dy*dy,.5)
        if d > self.maxSpeed:
            self.vx = dx/d * self.maxSpeed
            self.vy = dy/d * self.maxSpeed
        else:
            self.rect.x = self.destinationX
            self.rect.y = self.destinationY
    def setVelocitiesToFedPoint(self,x,y):
        dx = self.destinationX-self.rect.x
        dy = self.destinationY-self.rect.y
        d = math.pow(dx*dx+dy*dy,.5)
        if d > self.maxSpeed:
            self.vx = dx/d * self.maxSpeed
            self.vy = dy/d * self.maxSpeed
        else:
            self.rect.x = self.destinationX
            self.rect.y = self.destinationY
    def moveByVelocities(self):
        dx = self.destinationX-self.rect.x
        dy = self.destinationY-self.rect.y
        d = math.pow(dx*dx+dy*dy,.5)
        if d < self.maxSpeed:
            self.rect.x = self.destinationX
            self.rect.y = self.destinationY
        else:
            self.rect.x += self.vx
            self.rect.y += self.vy
    def forcedMove(self,dx,dy):
        self.rect.x+= dx
        self.rect.y+= dy

    def getPotentialCollisions(self, nearOthers):
        newRect = self.rect
        newRect.x += self.vx
        newRect.y += self.vy
        potentialCollisions = []
        for other in nearOthers:
            if other.rect.colliderect(newRect):
                potentialCollisions.append(other)
        return potentialCollisions
    def findValidPath(self,nearOthers):
        potentialCollisions = self.getPotentialCollisions(nearOthers)
        pathFound = False
        newRect = self.rect
        if potentialCollisions == 0:
            pathFound = True
        radius = 10
        d = 1.0
        while not pathFound:
            xMod = math.sin(d)*radius
            yMod = math.cos(d)*radius
            self.setVelocitiesToFedPoint(self.rect.x+xMod, self.rect.y+yMod)
            newRect.x += self.vx
            newRect.y += self.vy
            potentialCollisions = self.getPotentialCollisions(nearOthers)
            if potentialCollisions == 0:
                pathFound = True
            else:
                d *=-1.5

    def update(self,nearOthers):

        self.moveByVelocities()
        self.setVelocities()
        self.findValidPath(nearOthers)
class Guy(PhysicalObject):
    def __init__(self, color, x, y, spriteList):
        super().__init__(color, 20, 20, x, y, spriteList)
        # position
        self.worldObjects = spriteList
        self.worldObjects.remove(self)
        self.name = "default name"
        self.xPos = x
        self.yPos = y
        self.weapon = Weapon("Dagger of Default", AttackType.MELEE,(1,0,0),[])
        #self.weapon = Weapon("Bad ass Axe of maiming", AttackType.MELEE,(1,1,2),[])
        self.armor = Armor("rags of the dissolute",AttackType.MELEE,(0,0,0),[])
        # attributes
        self.strength = 3
        self.agility = 3
        self.cunning = 3
        self.constitution = 2
        self.maxConstitution = self.constitution
        self.xp  = 0
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
        self.specializations = {}
        self.talents = {}
    def acquireSpecialization(self,enum,allSpecializations):
        potentialSpecialization = allSpecializations[enum]
        for specialization in self.specializations:
            if specialization == potentialSpecialization:
                print("invalid")
        else:
            self.specializations[enum] = allSpecializations[enum]
    def acquireTalent(self,enum,allTalents):
        self.talents[enum] = allTalents[enum]
    def attack(self, opponent):
        if self.weapon.type == AttackType.MELEE:
            attribute = self.strength
            rank = self.skills[Skills.MELEE_WEAPON].rank
        if self.weapon.type == AttackType.RANGED:
            attribute = self.agility
            rank = self.skills[Skills.RANGED_WEAPON].rank
        if self.weapon.type == AttackType.MAGIC:
            attribute = self.cunning
            rank = self.skills[Skills.MAGIC_WEAPON].rank
        attackDiePool = (attribute, 0, 0)
        damageDiePool = self.weapon.damagePool
        criticalDiePool = (self.cunning, 0, 0)
        s = attackDiePool[0]
        m = attackDiePool[1]
        l = attackDiePool[2]
        #upgrade 1 die per rank. prioritizes lower die
        for i in range(rank):
            if  s > 0:
                m += 1
                s -= 1
            elif m >0:
                l += 1
                m -= 1
            else:
                s += 1

        attackDiePool = (s,m,l)

        att = Attack(self, type, opponent)
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
        debugPrint(attacker.name + " attacks " + self.name)


        for key in self.talents:
            talent = self.talents[key]
            debugPrint("Talent applied:" +talent.name)
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
        x = results[2]
        self.handleCounters(attacker,results[5])
        if results[0]>results[1]:
            self.handleDamage(results[2]-results[3])



    def applyCombatTalentDieEffects(self,attack, diePool, dieType):
        ret = diePool
        for key in self.talents:
            talent = self.talents[key]
            if not talent.type == TalentType.CRITICAL and not talent.type == TalentType.COUNTER:
                if talent.condition(attack):
                    for effect in talent.dieEffects:
                        if effect.dieType == dieType:
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
    def handleDamage(self,damage):
    # REVISIT ME
        resilience = (int)(self.constitution*.5)
        for key in self.talents:
            talent = self.talents[key]
            for otherEffect in talent.otherEffects:
                if otherEffect.otherEffectType==TalentType.DAMAGE_SOAK:
                    x =otherEffect.enact
                    resilience+=x

        if damage > 0:
            damageRoll = random.randint(0,damage)
            debugPrint("Damage Roll = " + str(damageRoll) + ", resilience = " + str(resilience))

            if damageRoll >= resilience:
                self.constitution-=1
                if self.constitution<1:
                    print(self.name + " is dead.")
                else:
                    print(self.name + " was wounded.")


    def rollDice(self, attackDiePool, damageDiePool, critDiePool, armorDiePool, dodgeDiePool, counterDiePool):
        global globalAttack
        attack = 0
        debugPrint("DiePools:")

        debugPrint(" Attack :" + str(attackDiePool))
        debugPrint(" Damage:" + str(damageDiePool))
        debugPrint(" Critical:" + str(critDiePool))

        debugPrint(" Armor:" + str(armorDiePool))
        debugPrint(" Dodge:" + str(dodgeDiePool))
        debugPrint(" Counter:" + str(counterDiePool))

        for s in range(attackDiePool[0]):
            roll = random.randint(1, 10)
            if roll > 5: attack += 1
        for m in range(attackDiePool[1]):
            roll = random.randint(1, 10)
            if roll > 5: attack += 1
            if roll == 10: attack += 2

        for L in range(attackDiePool[2]):
            roll = random.randint(1, 10)
            if roll > 3: attack += 1
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

        debugPrint ("results: ")
        debugPrint(" Attack = " + str(attack))
        debugPrint(" Defense = " + str(defense))
        debugPrint(" Damage = " + str(damage))
        debugPrint(" Armor = " + str(armor))
        debugPrint(" Critical = " + str(crit))
        debugPrint(" Counter = " + str(counter))

        return attack, defense, damage, armor, crit, counter
    def moveTheWorldBasedOnGuyVelocity(self):
        for o in self.worldObjects:
            o.forcedMove(-1*self.vx,-1*self.vy)
    def update(self):
        self.moveTheWorldBasedOnGuyVelocity()

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

    def rankUp(self):
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

'''
#sloppy land
talents = createTalents()
allSpecializations = createSpecializations()



def reviveAbeAndBob():
    global abe,bob
    abe = Guy(1,2,3)
    abe.name = "abe"
    bob = Guy(1,2,3)
    bob.name = "bob"


    #abe.acquireSpecialization(SpecializationName.BARBARIAN,allSpecializations)

    #abe.acquireTalent(TalentName.HEAVY_WEAPON_EXPERT,talents)
        #by itself with three con brings win to 80%
    #abe.acquireTalent(TalentName.EXECUTIONER,talents)
        #by itself wtc bwt 80%
    #bob.acquireTalent(TalentName.IRON_SKIN,talents)
        #biswtcbwt 90%
    abe.acquireTalent(TalentName.PUNISHING_DODGE,talents)
        #tied strongly to levelling up melee skill
    abe.xp = 2000
    #abe.levelSkill(Skills.MELEE_WEAPON)


a = 0
b = 0
def mockCombat(guyA,guyB):
    global a,b
    r = random.randint(0,1)
    if r==0:
        first = guyA
        second = guyB
    else:
        first = guyB
        second = guyA
    while guyA.constitution>0 and guyB.constitution>0:

        first.attack(second)
        if second.constitution>0:
            second.attack(first)
    if guyA.constitution <1:
        a+=1
    else:
        b+=1

for i in range(1000):
    reviveAbeAndBob()
    mockCombat(abe,bob)

print ("Abe Deaths: " + str(a))
print ("Bob Deaths:" + str(b))
'''
