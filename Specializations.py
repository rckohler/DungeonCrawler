from DC_Talents import*

class Specialization:
    def __init__(self, name, talentTree, careerSkills):
        self.talentTree = talentTree
        # when talents are purchased they are removed from the tree
        self.careerSkills = careerSkills
        self.name = name

talents = createTalents()
talentTree = [talents[TalentName.HEAVY_WEAPON_EXPERT]]
careerSkills = [Skills.MELEE_WEAPON, Skills.TRACKING]
Barbarian = Specialization("Barbarian",talentTree,careerSkills)