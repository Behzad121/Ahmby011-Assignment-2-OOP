'''
File: ahmby011.py
Description: This is assignment 2 - implementation.
Author: Ahmad Behzad
StudentID: 110354886
EmailID: ahmby011
This is my own work as defined by the University's Academic Misconduct Policy.
'''

from abc import ABC, abstractmethod

"""
Abstract class for reagents.
This class is used to define reagents.
It defines what the reagents in the system should have.
"""
class Reagent(ABC):
    def __init__(self, name, potency):
        self.__name = name
        self.__potency = potency

    def getName(self):
        return self.__name

    def getPotency(self):
        return self.__potency

    def setPotency(self, potency):
        self.__potency = potency

    @abstractmethod
    def refine(self):
        pass

"""
Herb inherits from the abstract class Reagent.
This class is used to expand the purpose of Reagent.
This is where the refinement of herbs or reagents are and their grimy status.
"""
class Herb(Reagent):
    def __init__(self, name, potency, grimy = True):
        super().__init__(name, potency)
        self.__grimy = grimy
    
    def refine(self):
        self.setGrimy(False)
        self.setPotency (self.getPotency() * 2.5)
        return f"The herb '{self.getName()}' has been refined. Potency has been multiplied by 2.5, now it's {self.getPotency()}."

    def getGrimy(self):
        return self.__grimy
    
    def setGrimy(self, grimy = False):
        self.__grimy = grimy
        return f"The herb '{self.getName()}' has been set to grimy: {self.__grimy}."


"""
This is catalyst and inherits from the abstract class Reagent.
The purpose of catalysts is to add refinement capabilities to reagents.
It gets the potency and the quality of the catalysts.
"""
class Catalyst(Reagent):
    def __init__(self, name, potency, quality):
        super().__init__(name, potency)
        self.__quality = quality

    def refine(self):
        if self.__quality < 8.9:
            self.__quality += 1.1
            self.setPotency(self.getPotency() + 1.1)    
            return f"{self.__name} has been refined. The quality has been increased to {self.__quality}."
        else:
            self.__quality = 10
            return f"The catalyst '{self.__name}', has reached quality level 10. It cannot be refined any further."
    
    def getQuality(self):
        return self.__quality


"""
This clas establishes what is required for different types of potions.
It sets the requirements for the its subclasses.
"""
class Potion(ABC):
    def __init__(self, name, stat, boost):
        self.__name = name
        self.__stat = stat
        self.__boost = boost

    @abstractmethod
    def calculateBoost(self):
        pass

    def getName(self):
        return self.__name
    
    def getStat(self):
        return self.__stat
    
    def getBoost(self):
        return self.__boost
    
    def setBoost(self, boost):
        self.__boost = boost

"""
SuperPotion is a subclass of Potion. 
It expands on the its parent class requirements.
The goal of it is to calculate the boost of the potion created with herb and catalyst.
"""
class SuperPotion(Potion):
    def __init__(self, name, stat, boost, herb, catalyst):
        super().__init__(name, stat, boost)
        self.__herb = herb
        self.__catalyst = catalyst
    
    def calculateBoost(self):
        return round((self.__herb.getPotency() + (self.__catalyst.getPotency() * self.__catalyst.getQuality())) * 1.5, 2)

    def getHerb(self):
        return self.__herb

    def getCatalyst(self):
        return self.__catalyst

"""
This is another subclass of Potion.
This is where a potion and reagent are mixed and the potency and boost are calculated.
"""
class ExtremePotion(Potion):
    def __init__(self, name, stat, boost, reagent, potion):
        super().__init__(name, stat, boost)
        self.__reagent = reagent
        self.__potion = potion

    def calculateBoost(self):
        return round((self.__reagent.getPotency() * self.__potion.getBoost()) * 3.0, 2)

    def getReagent(self):
        return self.__reagent
    
    def getPotion(self):
        return self.__potion


"""
Laboratory is where the potions, herbs and catalysts are stored.
"""
class Laboratory:
    def __init__(self):
        self.__potions = []
        self.__herbs = []
        self.__catalysts = []

    """mixPotion allows the potions to be created by mixing primary ingredients and secondary ingredients.
    based on the ingredients, it will either create a super potion or extreme potion.
    if the ingredients are incompatible or wrong the it will raise an error."""
    def mixPotion(self, name, type, stat, primaryIngredient, secondaryIngredient):
        potion = None
        if primaryIngredient.lower() == 'herb':
            primary = self.__herbs
        elif primaryIngredient.lower() == 'catalyst':
            primary = self.__catalysts
        else:
            raise ValueError("Incorrect primary ingredient for potion mixing.")

        if secondaryIngredient.lower() == 'catalyst':
            secondary = self.__catalysts
        elif secondaryIngredient.lower() == 'potion':
            secondary = self.__potions
        else:
            raise ValueError("Incorrect secondary ingredient for potion mixing.")
        
        if type.lower() == 'super potion':
            potion = SuperPotion(name, stat, 0, primary, secondary)
        elif type.lower() == 'extreme potion':
            potion = ExtremePotion(name, stat, 0, primary, secondary)

        if potion:
            self.__potions.append(potion)
            return potion
        else:
            raise ValueError("Incorrect potion type.")


    """
    This is where reagents are added in the laboratory.
    """
    def addReagent(self, reagent, amount):
        if isinstance(reagent, Herb):    
            for _ in range(amount):
                self.__herbs.append(Herb(reagent.getName(), reagent.getPotency(), reagent.getGrimy()))
        elif isinstance(reagent, Catalyst):
            for _ in range(amount):
                self.__catalysts.append(Catalyst(reagent.getName(), reagent.getPotency(), reagent.getQuality()))


"""
This is the alchemist who creates the potions with the help of a recipe.
"""
class Alchemist:

    """
    These are the attributes and what they contain.
    """
    def __init__(self, attack, strength, defense, magic, necromancy, laboratory, recipes):
        self.__attack = 0
        self.__strength = 0
        self.__defense = 0
        self.__magic = 0
        self.__necromancy = 0
        self.__laboratory = laboratory()
        self.__recipes = {
            'Super Attack': ['Irit', 'Eye of Newt'],
            'Super Strength': ['Kwuarm', 'Limpwurt Root'],
            'Super Defence': ['Cadantine', 'White Berries'],
            'Super Magic': ['Lantadyme', 'Potato Cactus'],
            'Super Ranging': ['Dwarf Weed', 'Wine of Zamorak'],
            'Super Necromancy': ['Arbuck', 'Blood of Orcus'],
            'Extreme Attack': ['Avantoe', 'Super Attack'],
            'Extreme Strength': ['Dwarf Weed', 'Super Strength'],
            'Extreme Defence': ['Lantadyme', 'Super Defence'],
            'Extreme Magic': ['Ground Mud Rune', 'Super Magic'],
            'Extreme Ranging': ['Grenwall Spike', 'Super Ranging'],
            'Extreme Necromancy': ['Ground Miasma Rune', 'Super Necromancy']
        }

    def getLaboratory(self):
        return self.__laboratory
    
    def getRecipes(self):
        return self.__recipes
    
    """
    mixPotion takes in name, type, stat, primary ingredient, and secondary ingredient for a potion.
    Calls the mixPotion method of the laboratory to create a potion.
    """
    def mixPotion(self, name, type, stat, primaryIngredient, secondaryIngredient):
        potion = self.__laboratory.mixPotion(name, type, stat, primaryIngredient, secondaryIngredient)
        return potion
    
    """
    The effects of the potion are calculated and the stat is shown to the Alchemist. It makes sure it is not over 100.
    """
    def drinkPotion(self, potion):
        boost = potion.calculateBoost()
        stat = potion.getStat()
        current_stat = getattr(self, f"__{stat.lower()}")
        setattr(self, f"__{stat.lower()}", min(100, current_stat+boost))
        potion.setBoost(boost)
        return f"{stat}'s {stat.lower()} increased by {boost}."
 
    def collectReagent(self, reagent, amount):
        self.__laboratory.addReagent(reagent, amount)


    """
    Iterates through the catalysts and herbs in the laboratory and prints the refine methods.
    """
    def refineReagents(self):
        for potion in self.__laboratory.getPotions():
            if isinstance(potion, ExtremePotion):
                reagent = potion.getReagent()
                reagent.refine()
                potion.calculateBoost()
            for catalyst in self.__laboratory.getCatalysts():
                print(catalyst.refine())