def c_meleeHeavyAttack(attack):
    ret = True ### broken for testing
    if attack.attackType == "MELEE" and attack.weapon == "HEAVY":
        ret = True
    return ret
def c_crit1(critRoll):
    ret = False
    if critRoll > 0:
        ret = True
    return ret
def c_crit2(critRoll):
    ret = False
    if critRoll > 1:
        ret = True
    return ret
def none(crap):
    return True
