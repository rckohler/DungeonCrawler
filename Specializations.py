from DC_Talents import*

class Specialization:
    def __init__(self, name, talentTree, careerSkills):
        self.talentTree = talentTree
        # when talents are purchased they are removed from the tree
        self.careerSkills = careerSkills
        self.name = name
    def addCareerSkills(self,guy):
        for key in self.careerSkills:
            skill = self.careerSkills[key]
          #  guy.skills{skill}


def createSpecializations():
    talents = createTalents()
    talentTree = [talents[TalentName.HEAVY_WEAPON_EXPERT]]
    careerSkills = [Skills.MELEE_WEAPON, Skills.TRACKING]
    barbarian = Specialization("Barbarian",talentTree,careerSkills)
    specializations = {SpecializationName.BARBARIAN:barbarian}
    return specializations
