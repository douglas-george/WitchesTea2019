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
    DETECTOR0 = "DET0"
    DETECTOR1 = "DET1"
    DETECTOR2 = "DET2"
    DETECTOR3 = "DET3"
    DETECTOR4 = "DET4"
    DETECTOR5 = "DET5"
    DETECTOR6 = "DET6"
    DETECTOR7 = "DET7"
    DETECTOR8 = "DET8"
    DETECTOR9 = "DET9"
    DETECTOR10 = "DET10"


class Dessert(object):
    def __init__(self, dessertName, ingredientList):
        self.dessertName = dessertName
        self.ingredientList = ingredientList

    def __str__(self):
        return self.dessertName


class PoisonTester(object):
    @staticmethod
    def NotThePoison(theRealPoison, thisPoison, dessert):
        # DETECTOR0 is the visual inspection of the elements state...
        if Ingredient.DETECTOR0 in dessert.ingredientList:
            if (theRealPoison.state != thisPoison.state):
                return True

        # DETECTOR1 tastes sweet to those infected by blights, scourges, or venoms
        if Ingredient.DETECTOR1 in dessert.ingredientList:
            if (theRealPoison.variety == Poison.POISON_VARIETY_BLIGHT) or (
                    theRealPoison.variety == Poison.POISON_VARIETY_SCOURGE) or (
                    theRealPoison.variety == Poison.POISON_VARIETY_VENOM):
                if (thisPoison.variety != Poison.POISON_VARIETY_BLIGHT) and (
                        thisPoison.variety != Poison.POISON_VARIETY_SCOURGE) and (
                        thisPoison.variety != Poison.POISON_VARIETY_VENOM):
                    return True

        # DETECTOR2 and DETECTOR3 together has a minty flavor when consumed with an earth or fire poison
        if (Ingredient.DETECTOR2 in dessert.ingredientList) and (Ingredient.DETECTOR3 in dessert.ingredientList):
            if (theRealPoison.element == Poison.POISON_ELEMENT_EARTH) or (
                    theRealPoison.element == Poison.POISON_ELEMENT_FIRE):
                if (thisPoison.element != Poison.POISON_ELEMENT_EARTH) and (
                        thisPoison.element != Poison.POISON_ELEMENT_FIRE):
                    return True

        # DETECTOR4 has a distinct chocolate flavor to those afflicted with any poison
        if Ingredient.DETECTOR4 in dessert.ingredientList:
            pass

        # DETECTOR5 and DETECTOR6 taken together cause uncontrollable laughter in those afflicted with blights or venoms
        if (Ingredient.DETECTOR5 in dessert.ingredientList) and (Ingredient.DETECTOR6 in dessert.ingredientList):
            if (theRealPoison.variety == Poison.POISON_VARIETY_BLIGHT) or (
                    theRealPoison.variety == Poison.POISON_VARIETY_VENOM):
                if (thisPoison.variety != Poison.POISON_VARIETY_BLIGHT) and (
                        thisPoison.variety != Poison.POISON_VARIETY_VENOM):
                    return True

        # DETECTOR7 causes the infected person to sing, in an operatic voice, the variety of poison they are afflicted with
        if Ingredient.DETECTOR7 in dessert.ingredientList:
            if (theRealPoison.variety != thisPoison.variety):
                return True

        # DETECTOR7 causes the infected person to sing, in an operatic voice, if they are not afflicted with a scourge
        #if Ingredient.DETECTOR7 in dessert.ingredientList:
        #    if (theRealPoison.variety != Poison.POISON_VARIETY_SCOURGE) and (
        #            thisPoison.element == Poison.POISON_VARIETY_SCOURGE):
        #        return True

        # DETECTOR8 causes an incredibly and painfully spicy reaction to someone afflicted with earth or ether blights
        if Ingredient.DETECTOR8 in dessert.ingredientList:
            if ((theRealPoison.element == Poison.POISON_ELEMENT_EARTH) or (
                    theRealPoison.element == Poison.POISON_ELEMENT_ETHER)) and (
                    theRealPoison.variety == Poison.POISON_VARIETY_BLIGHT):
                if ((thisPoison.element != Poison.POISON_ELEMENT_EARTH) and (
                        thisPoison.element != Poison.POISON_ELEMENT_ETHER)) or (
                        thisPoison.variety != Poison.POISON_VARIETY_BLIGHT):
                    return True

        # DETECTOR9 causes drooling and foaming at the mouth for those afflicted with air venoms or fire toxins
        if Ingredient.DETECTOR9 in dessert.ingredientList:
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

        # DETECTOR10 causes _______________ in any afflicted with a fire, air, or ether poison in a gaseous or liquid state
        if Ingredient.DETECTOR10 in dessert.ingredientList:
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
    visualInspection = Dessert(dessertName="VisualInspection", ingredientList=[Ingredient.DETECTOR0, ])
    dessert1 = Dessert(dessertName="Dessert1",
                       ingredientList=[Ingredient.DETECTOR2, Ingredient.DETECTOR3, Ingredient.DETECTOR4])
    dessert2 = Dessert(dessertName="Dessert2",
                       ingredientList=[Ingredient.DETECTOR1, Ingredient.DETECTOR3, Ingredient.DETECTOR6])
    dessert3 = Dessert(dessertName="Dessert3", ingredientList=[Ingredient.DETECTOR2, Ingredient.DETECTOR3])
    dessert4 = Dessert(dessertName="Dessert4",
                       ingredientList=[Ingredient.DETECTOR3, Ingredient.DETECTOR5, Ingredient.DETECTOR6])
    dessert5 = Dessert(dessertName="Dessert5",
                       ingredientList=[Ingredient.DETECTOR1, Ingredient.DETECTOR3, Ingredient.DETECTOR7])
    dessert6 = Dessert(dessertName="Dessert6", ingredientList=[Ingredient.DETECTOR5, Ingredient.DETECTOR7])
    dessert7 = Dessert(dessertName="Dessert7", ingredientList=[Ingredient.DETECTOR9])
    dessert8 = Dessert(dessertName="Dessert8", ingredientList=[Ingredient.DETECTOR10])

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



