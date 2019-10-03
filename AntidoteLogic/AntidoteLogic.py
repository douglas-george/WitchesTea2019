from itertools import permutations


class Poison(object):
    POISON_STATE_GAS = "GAS"
    POISON_STATE_LIQUID = "LIQUID"
    POISON_STATE_SOLID = "SOLID"

    POISON_VARIETY_TOXIN = "TOXIN"
    POISON_VARIETY_VENOM = "VENOM"
    POISON_VARIETY_BLIGHT = "BLIGHT"
    POISON_VARIETY_SCOURGE = "SCOURGE"

    POISON_ELEMENT_EARTH = "EARTH"
    POISON_ELEMENT_AIR = "AIR"
    POISON_ELEMENT_FIRE = "FIRE"
    POISON_ELEMENT_WATER = "WATER"
    POISON_ELEMENT_ETHER = "ETHER"

    def __init__(self, poisonName, state, variety, element):
        self.poisonName = poisonName
        self.state = state
        self.variety = variety
        self.element = element

    def __str__(self):
        return "({}: {}, {}, {})".format(self.poisonName, self.state, self.variety, self.element)


class Ingredient(object):
    D0_VISUAL_INSPECTION = "DET0"
    D1_BANEBERRY = "DET1"
    D2_BILLYWIG_STING_SLIME = "DET2"
    D3_MOONDEW = "DET3"
    D4_HALIWINKLES = "DET4"
    D5_LACEWINGS = "DET5"
    D6_BULBADOX_JUICE = "DET6"
    D7_HORKLUMP_JUICE = "DET7"
    D8_PEARL_DUST = "DET8"
    D9_DRAGONFLY_THORAX = "DET9"
    D10_LICHEN_POWDER = "DET10"


class Dessert(object):
    def __init__(self, dessertName, ingredientList):
        self.dessertName = dessertName
        self.ingredientList = ingredientList

    def __str__(self):
        return self.dessertName


class PoisonTester(object):
    @staticmethod
    def NotThePoison(theRealPoison, thisPoison, dessert):
        # D0_VISUAL_INSPECTION is the visual inspection of the elements state...
        if Ingredient.D0_VISUAL_INSPECTION in dessert.ingredientList:
            if (theRealPoison.state != thisPoison.state):
                return True

        # D1_BANEBERRY makes things taste bitter to those who have been poisoned with a toxin (sweet to those infected by blights, scourges, or venoms)
        if Ingredient.D1_BANEBERRY in dessert.ingredientList:
            if (theRealPoison.variety == Poison.POISON_VARIETY_BLIGHT) or (
                    theRealPoison.variety == Poison.POISON_VARIETY_SCOURGE) or (
                    theRealPoison.variety == Poison.POISON_VARIETY_VENOM):
                if (thisPoison.variety != Poison.POISON_VARIETY_BLIGHT) and (
                        thisPoison.variety != Poison.POISON_VARIETY_SCOURGE) and (
                        thisPoison.variety != Poison.POISON_VARIETY_VENOM):
                    return True

        # D2_BILLYWIG_STING_SLIME and D3_MOONDEW together have a minty flavor when consumed with an earth or fire poison, cinammon for water or ether, garlic for air
        if (Ingredient.D2_BILLYWIG_STING_SLIME in dessert.ingredientList) and (Ingredient.D3_MOONDEW in dessert.ingredientList):
            if (theRealPoison.element == Poison.POISON_ELEMENT_EARTH) or (
                    theRealPoison.element == Poison.POISON_ELEMENT_FIRE):
                if (thisPoison.element != Poison.POISON_ELEMENT_EARTH) and (
                        thisPoison.element != Poison.POISON_ELEMENT_FIRE):
                    return True

        # D4_HALIWINKLES has a distinct chocolate flavor to those afflicted with any poison
        if Ingredient.D4_HALIWINKLES in dessert.ingredientList:
            pass

        # D5_LACEWINGS and D6_BULBADOX_JUICE taken together cause uncontrollable laughter in those afflicted with blights or venoms
        if (Ingredient.D5_LACEWINGS in dessert.ingredientList) and (Ingredient.D6_BULBADOX_JUICE in dessert.ingredientList):
            if (theRealPoison.variety == Poison.POISON_VARIETY_BLIGHT) or (
                    theRealPoison.variety == Poison.POISON_VARIETY_VENOM):
                if (thisPoison.variety != Poison.POISON_VARIETY_BLIGHT) and (
                        thisPoison.variety != Poison.POISON_VARIETY_VENOM):
                    return True

        # D7_HORKLUMP_JUICE causes the infected person to sing, in an operatic voice, the variety of poison they are afflicted with
        if Ingredient.D7_HORKLUMP_JUICE in dessert.ingredientList:
            if (theRealPoison.variety != thisPoison.variety):
                return True

        # D8_PEARL_DUST causes an incredibly and painfully spicy reaction to someone afflicted with earth or ether blights
        if Ingredient.D8_PEARL_DUST in dessert.ingredientList:
            if ((theRealPoison.element == Poison.POISON_ELEMENT_EARTH) or (
                    theRealPoison.element == Poison.POISON_ELEMENT_ETHER)) and (
                    theRealPoison.variety == Poison.POISON_VARIETY_BLIGHT):
                if ((thisPoison.element != Poison.POISON_ELEMENT_EARTH) and (
                        thisPoison.element != Poison.POISON_ELEMENT_ETHER)) or (
                        thisPoison.variety != Poison.POISON_VARIETY_BLIGHT):
                    return True

        # D9_DRAGONFLY_THORAX causes drooling and foaming at the mouth for those afflicted with air venoms or fire toxins
        if Ingredient.D9_DRAGONFLY_THORAX in dessert.ingredientList:
            if (theRealPoison.element == Poison.POISON_ELEMENT_AIR) and (
                    theRealPoison.variety == Poison.POISON_VARIETY_VENOM):
                if (thisPoison.element != Poison.POISON_ELEMENT_AIR) or (
                        thisPoison.variety != Poison.POISON_VARIETY_VENOM):
                    return True

            if (theRealPoison.element == Poison.POISON_ELEMENT_FIRE) and (
                    theRealPoison.variety == Poison.POISON_VARIETY_TOXIN):
                if (thisPoison.element != Poison.POISON_ELEMENT_FIRE) or (
                        thisPoison.variety != Poison.POISON_VARIETY_TOXIN):
                    return True

        # D10_LICHEN_POWDER tastes like bananas* in any afflicted with a fire, air, or ether poison in a gaseous or liquid state
        if Ingredient.D10_LICHEN_POWDER in dessert.ingredientList:
            if ((theRealPoison.element == Poison.POISON_ELEMENT_FIRE) or (
                    theRealPoison.element == Poison.POISON_ELEMENT_AIR) or (
                        theRealPoison.element == Poison.POISON_ELEMENT_ETHER)) and (
                    (theRealPoison.state == Poison.POISON_STATE_GAS) or (
                    theRealPoison.state == Poison.POISON_STATE_LIQUID)):
                if ((thisPoison.element != Poison.POISON_ELEMENT_FIRE) and (
                        thisPoison.element != Poison.POISON_ELEMENT_AIR) and (
                            thisPoison.element != Poison.POISON_ELEMENT_ETHER)) or (
                        (thisPoison.state != Poison.POISON_STATE_GAS) and (
                        thisPoison.state != Poison.POISON_STATE_LIQUID)):
                    return True


if __name__ == "__main__":
    visualInspection = Dessert(dessertName="VisualInspection", ingredientList=[Ingredient.D0_VISUAL_INSPECTION, ])

    dessert1 = Dessert(dessertName="Dessert1",
                       ingredientList=[Ingredient.D2_BILLYWIG_STING_SLIME, Ingredient.D4_HALIWINKLES])

    dessert2 = Dessert(dessertName="Dessert2",
                       ingredientList=[Ingredient.D1_BANEBERRY, Ingredient.D3_MOONDEW, Ingredient.D6_BULBADOX_JUICE])

    dessert3 = Dessert(dessertName="Dessert3",
                       ingredientList=[Ingredient.D2_BILLYWIG_STING_SLIME, Ingredient.D3_MOONDEW])

    dessert4 = Dessert(dessertName="Dessert4",
                       ingredientList=[Ingredient.D3_MOONDEW, Ingredient.D5_LACEWINGS, Ingredient.D6_BULBADOX_JUICE])

    dessert5 = Dessert(dessertName="Dessert5",
                       ingredientList=[Ingredient.D1_BANEBERRY, Ingredient.D3_MOONDEW])

    dessert6 = Dessert(dessertName="Dessert6",
                       ingredientList=[Ingredient.D8_PEARL_DUST])

    dessert7 = Dessert(dessertName="Dessert7",
                       ingredientList=[Ingredient.D5_LACEWINGS, Ingredient.D7_HORKLUMP_JUICE])

    dessert8 = Dessert(dessertName="Dessert8",
                       ingredientList=[Ingredient.D10_LICHEN_POWDER])

    dessertList = []
    dessertList.append(dessert1)
    dessertList.append(dessert2)
    dessertList.append(dessert3)
    dessertList.append(dessert4)
    dessertList.append(dessert5)
    dessertList.append(dessert6)
    dessertList.append(dessert7)
    dessertList.append(dessert8)

    poisonList = []
    poisonId = 1
    for state in [Poison.POISON_STATE_SOLID, Poison.POISON_STATE_LIQUID, Poison.POISON_STATE_GAS]:
        for variety in [Poison.POISON_VARIETY_TOXIN, Poison.POISON_VARIETY_VENOM, Poison.POISON_VARIETY_BLIGHT,
                        Poison.POISON_VARIETY_SCOURGE]:
            for element in [Poison.POISON_ELEMENT_EARTH, Poison.POISON_ELEMENT_AIR, Poison.POISON_ELEMENT_FIRE,
                            Poison.POISON_ELEMENT_WATER, Poison.POISON_ELEMENT_ETHER]:
                poisonList.append(
                    Poison(poisonName="Poison{}".format(poisonId), state=state, variety=variety, element=element))
                poisonId += 1

    thePoison = Poison(poisonName="ThePoison!", state=Poison.POISON_STATE_GAS, variety=Poison.POISON_VARIETY_VENOM,
                       element=Poison.POISON_ELEMENT_FIRE)

    #permutations = list(permutations(dessertList))
    permutations = [dessertList,]

    minToSolve = 100000000
    brokenLogic = False
    for permutation in permutations:
        for element in permutation:
            print("{}, ".format(element), end='')
        print("")

        dessertOrder = list(permutation)
        dessertOrder.insert(0, visualInspection)

        numDessertsToSolve = None

        possiblePoisons = poisonList

        for dessertIndex, dessert in enumerate(dessertOrder):
            newPossiblePoisonList = []
            for possiblePoison in possiblePoisons:
                if PoisonTester.NotThePoison(theRealPoison=thePoison, thisPoison=possiblePoison, dessert=dessert):
                    pass
                else:
                    newPossiblePoisonList.append(possiblePoison)

            possiblePoisons = newPossiblePoisonList

            if (len(possiblePoisons) == 1) and (numDessertsToSolve is None):
                numDessertsToSolve = (dessertIndex + 1)

            if (len(possiblePoisons) == 0):
                brokenLogic = True

        if (len(possiblePoisons) > 1):
            brokenLogic = True

        if not brokenLogic and (numDessertsToSolve < minToSolve):
            minToSolve = numDessertsToSolve

        '''        
        if numDessertsToSolve < 5:
            print(numDessertsToSolve, brokenLogic)
            for dessert in dessertOrder:
                print("\t{}".format(dessert))
        else:
            print(numDessertsToSolve, brokenLogic)
        '''

    print(minToSolve, brokenLogic)



