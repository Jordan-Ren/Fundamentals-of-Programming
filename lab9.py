"""6.009 Spring 2019 Lab 9 -- 6.009 Zoo"""

from math import ceil  # ONLY import allowed in this lab

# NO CUSTOM IMPORTS ALLOWED!

class Constants:
    """
    A collection of game-specific constants.

    You can experiment with tweaking these constants, but
    remember to revert the changes when running the test suite!
    """
    # width and height of keepers
    KEEPER_WIDTH = 31
    KEEPER_HEIGHT = 31

    # width and height of animals
    ANIMAL_WIDTH = 31
    ANIMAL_HEIGHT = 31

    # width and height of food
    FOOD_WIDTH = 11
    FOOD_HEIGHT = 11

    # width and height of rocks
    ROCK_WIDTH = 51
    ROCK_HEIGHT = 51

    # thickness of the path
    PATH_THICKNESS = 31

    # some other characters
    DEMON_WIDTH = 51
    DEMON_HEIGHT = 51
    DEMON_RADIUS = 75  # Only animals this close are affected.
    DEMON_MULTIPLIER = 2  # Animal speeds multiplied by this factor
    DEMON_PRICE = 100

    VHS_WIDTH = 31
    VHS_HEIGHT = 31
    VHS_RADIUS = 75
    VHS_MULTIPLIER = .5
    VHS_PRICE = 20

    EXPLOSION_HEIGHT = 101
    EXPLOSION_WIDTH = 101
    EXPLOSION_RADIUS = 100

    CRAZY_NAP_LENGTH = 20

    PSYCHO_COOLDOWN = 8

    TRAINEE_THRESHOLD = 20  # How many food hits must the trainee score,
    # before becoming a speedy zookeeper?
     # 💥	1f4a5
     #  💣	1f4a3
      #🤐	1f910
    TEXTURES = {
        'rock': '1f5ff',
        'animal': '1f418',
        'SpeedyZookeeper': '1f472',
        'ThriftyZookeeper': '1f46e',
        'OverreachingZookeeper': '1f477',
        'food': '1f34e',
        'Demon': '1f479',
        'VHS': '1f4fc',
        'TraineeZookeeper': '1f476',
        'CrazyZookeeper': '1f61c',
        'SleepingZookeeper': '1f634',
        'PsychopathicZookeeper': '1f910',
        'Bomb': '1f4a3',
        'Explosion': '1f4a5'
    }

    KEEPER_INFO = {'SpeedyZookeeper':
                       {'price': 250,
                        'range': 50,
                        'throw_speed_mag': 20},
                   'ThriftyZookeeper':
                       {'price': 100,
                        'range': 100,
                        'throw_speed_mag': 15},
                   'OverreachingZookeeper':
                       {'price': 150,
                        'range': 150,
                        'throw_speed_mag': 5},
                   'TraineeZookeeper':
                       {'price': 50,
                        'range': 100,
                        'throw_speed_mag': 5},
                   'CrazyZookeeper':
                       {'price': 100,
                        'range': 1000,
                        'throw_speed_mag': 50},
                    'PsychopathicZookeeper':
                       {'price': 100,
                        'range': 250,
                        'throw_speed_mag': 10}
                   }

################################################################################
##  Copy and paste your code from lab8 below EXCEPT for the Constants class.  ##
##  The Constants class above contains the changes needed for the lab.        ##
################################################################################

### lab8 code here ###
class NotEnoughMoneyError(Exception):
    """A custom exception to be used when insufficient funds are available
    to hire new zookeepers."""
    pass



################################################################################
################################################################################
# Static methods.

def distance(a, b):
    """Returns the Euclidian distance between the two tuple coordinates."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5



################################################################################
################################################################################

class Game:
    def __init__(self, game_info):
        """Initializes the game.

        `game_info` is a dictionary formatted in the following manner:
          { 'width': The width of the game grid, in an integer (i.e. number of pixels).
            'height': The height of the game grid, in an integer (i.e. number of pixels).
            'rocks': The set of tuple rock coordinates.
            'path_corners': An ordered list of coordinate tuples. The first
                            coordinate is the starting point of the path, the
                            last point is the end point (both of which lie on
                            the edges of the gameboard), and the other points
                            are corner ("turning") points on the path.
            'money': The money balance with which the player begins.
            'spawn_interval': The interval (in timesteps) for spawning animals
                              to the game.
            'animal_speed': The magnitude of the speed at which the animals move
                            along the path, in units of grid distance traversed
                            per timestep.
            'num_allowed_unfed': The number of animals allowed to finish the
                                 path unfed before the player loses.
          }
        """
        self.width = game_info['width']
        self.height = game_info['height']
        self.rocks = game_info['rocks']
        self.path_corners = game_info['path_corners']
        self.path = []
        #creates a list of all coordinates in order for the path
        for i in range(len(self.path_corners)-1):
            #if x are the same, path goes up
            if self.path_corners[i][0] == self.path_corners[i+1][0]:
                if self.path_corners[i+1][1] - self.path_corners[i][1] < 0:
                    for j in range(abs(self.path_corners[i+1][1] - self.path_corners[i][1])):
                        self.path.append((self.path_corners[i][0], self.path_corners[i][1] - j))
                else:
                    for j in range(abs(self.path_corners[i+1][1] - self.path_corners[i][1])):
                        self.path.append((self.path_corners[i][0], self.path_corners[i][1] + j))
            if self.path_corners[i][1] == self.path_corners[i+1][1]:
                if self.path_corners[i+1][0] - self.path_corners[i][0] < 0:
                    for j in range(abs(self.path_corners[i+1][0] - self.path_corners[i][0])):
                        self.path.append((self.path_corners[i][0] - j, self.path_corners[i][1]))
                else:
                    for j in range(abs(self.path_corners[i+1][0] - self.path_corners[i][0])):
                        self.path.append((self.path_corners[i][0] + j, self.path_corners[i][1]))
        self.path.append(self.path_corners[-1])

        self.money = game_info['money']
        # self.money = 1000
        self.spawn_interval = game_info['spawn_interval']
        self.time_to_spawn = 1
        self.animal_speed = game_info['animal_speed']
        self.num_allowed_unfed = game_info['num_allowed_unfed']
        self.formations = Formations()
        self.keeper_type = None
        self.status = 'ongoing'
        self.animals_fed = 0
        for rock in self.rocks:
            self.formations.add_formation_rock(rock)

    def check_game_status(self):
        if self.num_allowed_unfed < 0:
            self.status = 'defeat'

    def render(self):
        # print(self.formations.formations)
        return {'formations': self.formations.formations, 'money': self.money,
                'status': self.status, 'num_allowed_remaining': self.num_allowed_unfed}
################################################################################
################################################################################
#Timestep methods
    def formation_movement(self):
        animals_to_remove = []
        for animal in self.formations.animals:
            #animal movements
            #moves animal loc along path to new loc, if it is past the end,
            #then remove it and remove 1 from allowed unfed
            new_animal_speed = animal['speed']
            for demon in self.formations.demons:
                if distance(animal['loc'], demon['loc']) < Constants.DEMON_RADIUS:
                    new_animal_speed = (new_animal_speed * Constants.DEMON_MULTIPLIER)
            for VHS in self.formations.VHS:
                if distance(animal['loc'], VHS['loc']) < Constants.VHS_RADIUS:
                    new_animal_speed = (new_animal_speed * Constants.VHS_MULTIPLIER)
            new_animal_speed = ceil(new_animal_speed)
            animal['temp_speed'] = new_animal_speed
            for i in range(len(self.path)):
                if animal['loc'] == self.path[i]:
                    start_loc_index = i
            if start_loc_index + new_animal_speed < len(self.path):
                animal['loc'] = self.path[start_loc_index + new_animal_speed]
            else:
                # print("removed", animal);
                animals_to_remove.append(animal)
                self.num_allowed_unfed -= 1
        for animal in animals_to_remove:
            self.formations.remove_animal(animal)
        # print(self.formations)
        #food movements
        food_to_delete = []
        for food in self.formations.food:
            velocity = food['velocity']
            food['loc'] = (velocity * food['unit_x'] + food['loc'][0], velocity * food['unit_y'] + food['loc'][1])
            if food['loc'][0] < 0 or food['loc'][0] > self.width:
                food_to_delete.append(food)
                continue
            if food['loc'][1] < 0 or food['loc'][1] > self.height:
                food_to_delete.append(food)
        for thrown_food in food_to_delete:
            self.formations.formations.remove(thrown_food)
            self.formations.food.remove(thrown_food)

    def bomb_animal_collisions(self):
        food_to_delete = []
        animals_to_delete = []
        for food in self.formations.food:
            tag = False
            if food['texture'] == Constants.TEXTURES['Bomb']:
                for animal in self.formations.animals:
                    animal_center = animal['loc']
                    if abs(food['loc'][0] - animal_center[0]) < ((Constants.FOOD_WIDTH) + (Constants.ANIMAL_WIDTH))/2:
                        if abs(food['loc'][1] - animal_center[1]) < ((Constants.FOOD_HEIGHT) + (Constants.ANIMAL_HEIGHT))/2:
                            food['texture'] = Constants.TEXTURES['Explosion']
                            food['unit_x'] = 0
                            food['unit_y'] = 0
                            food['size'] = (Constants.EXPLOSION_WIDTH, Constants.EXPLOSION_HEIGHT)
                            tag = True
                            break
            if tag:
                continue
            if food['texture'] == Constants.TEXTURES['Explosion']:
                for animal in self.formations.animals:
                    if distance(animal['loc'], food['loc']) < Constants.EXPLOSION_RADIUS:
                        if animal not in animals_to_delete:
                            animals_to_delete.append(animal)
                            self.animals_fed += 1
                food_to_delete.append(food)
        for eaten_food in food_to_delete:
            if eaten_food in self.formations.food:
                self.formations.food.remove(eaten_food)
            if eaten_food in self.formations.formations:
                self.formations.formations.remove(eaten_food)
        for fed_animal in animals_to_delete:
            if fed_animal in self.formations.animals:
                self.formations.animals.remove(fed_animal)
            if fed_animal in self.formations.formations:
                self.formations.formations.remove(fed_animal)

    def food_animal_collisions(self):
        animals_to_delete = []
        food_to_delete = []
        for animal in self.formations.animals:
            animal_center = animal['loc']
            tag = False
            for food in self.formations.food:
                if food['texture'] == Constants.TEXTURES['food']:
                    if abs(food['loc'][0] - animal_center[0]) < ((Constants.FOOD_WIDTH) + (Constants.ANIMAL_WIDTH))/2:
                        if abs(food['loc'][1] - animal_center[1]) < ((Constants.FOOD_HEIGHT) + (Constants.ANIMAL_HEIGHT))/2:
                            if not tag:
                                if animal not in animals_to_delete:
                                    animals_to_delete.append(animal)
                                    self.animals_fed += 1
                            food_to_delete.append(food)
                            if food['keeper_type'] != None:
                                if food['fed'] == None:
                                    if food['keeper_type']['type'] == 'TraineeZookeeper':
                                        food['fed'] = True
                                        food['keeper_type']['threshold'] -= 1
                            tag = True
        for fed_animal in animals_to_delete:
            if fed_animal in self.formations.animals:
                self.formations.animals.remove(fed_animal)
            if fed_animal in self.formations.formations:
                self.formations.formations.remove(fed_animal)
        for eaten_food in food_to_delete:
            if eaten_food in self.formations.food:
                self.formations.food.remove(eaten_food)
            if eaten_food in self.formations.formations:
                self.formations.formations.remove(eaten_food)

    def find_collisions(self, loc, height, width):
        for rock in self.formations.rocks:
            if abs(rock['loc'][0] - loc[0]) * 2 < (Constants.ROCK_WIDTH + width):
                if abs(rock['loc'][1] - loc[1]) * 2< (Constants.ROCK_HEIGHT + height):
                    return False
        for new_keepers in self.formations.keepers:
            if abs(new_keepers['loc'][0] - loc[0]) * 2< (Constants.KEEPER_WIDTH + width):
                if abs(new_keepers['loc'][1] - loc[1]) * 2< (Constants.KEEPER_HEIGHT + height):
                    return False
        for demon in self.formations.demons:
            if abs(demon['loc'][0] - loc[0]) * 2< (Constants.DEMON_WIDTH + width):
                if abs(demon['loc'][1] - loc[1]) * 2< (Constants.DEMON_HEIGHT + height):
                    return False
        for VHS in self.formations.VHS:
            if abs(VHS['loc'][0] - loc[0]) * 2< (Constants.VHS_WIDTH + width):
                if abs(VHS['loc'][1] - loc[1]) * 2< (Constants.VHS_HEIGHT + height):
                    return False
        #I split the path up into rectangles with each rectangle being a segment
        #of the path. check each rectangle
        rectangle_corners = []
        for i in range(len(self.path_corners)-1):
            temp = []
            if self.path_corners[i][0] - self.path_corners[i+1][0] == 0:
                if self.path_corners[i][1] - self.path_corners[i+1][1] < 0:
                    x_start = self.path_corners[i][0] - (Constants.PATH_THICKNESS-1)/2
                    x_end = self.path_corners[i +1][0] + (Constants.PATH_THICKNESS-1)/2
                    y_start = self.path_corners[i][1] - (Constants.PATH_THICKNESS-1)/2
                    y_end = self.path_corners[i + 1][1] + (Constants.PATH_THICKNESS-1)/2
                else:
                    x_start = self.path_corners[i][0] - (Constants.PATH_THICKNESS-1)/2
                    x_end = self.path_corners[i +1][0] + (Constants.PATH_THICKNESS-1)/2
                    y_start = self.path_corners[i][1] + (Constants.PATH_THICKNESS-1)/2
                    y_end = self.path_corners[i + 1][1] - (Constants.PATH_THICKNESS-1)/2
            else:
                if self.path_corners[i][0] - self.path_corners[i+1][0] < 0:
                    x_start = self.path_corners[i][0] - (Constants.PATH_THICKNESS-1)/2
                    x_end = self.path_corners[i +1][0] + (Constants.PATH_THICKNESS-1)/2
                    y_start = self.path_corners[i][1] - (Constants.PATH_THICKNESS-1)/2
                    y_end = self.path_corners[i + 1][1] + (Constants.PATH_THICKNESS-1)/2
                else:
                    x_start = self.path_corners[i][0] + (Constants.PATH_THICKNESS-1)/2
                    x_end = self.path_corners[i +1][0] - (Constants.PATH_THICKNESS-1)/2
                    y_start = self.path_corners[i][1] - (Constants.PATH_THICKNESS-1)/2
                    y_end = self.path_corners[i + 1][1] + (Constants.PATH_THICKNESS-1)/2
            temp.append(x_start)
            temp.append(x_end)
            temp.append(y_end)
            temp.append(y_start)
            rectangle_corners.append(temp)
        for rectangle in rectangle_corners:
            if abs((rectangle[0] + rectangle[1])/2 - loc[0]) * 2 < (abs(rectangle[0] - rectangle[1]) + width):
                if abs((rectangle[2] + rectangle[3])/2 - loc[1]) * 2 < (abs(rectangle[2] - rectangle[3]) + height):
                    return False
        return True

    def throw_food(self, keeper):
        '''
        Determines the velocity, and destination for a new food formation.
        '''
        def find_animals_in_range(keeper):
            range = Constants.KEEPER_INFO[keeper['type']]['range']
            animals_to_check = []
            for animal in self.formations.animals:
                if distance(keeper['loc'], animal['loc']) <= range:
                    animals_to_check.append(animal)
            return animals_to_check
        def distance(a, b):
            """Returns the Euclidian distance between the two tuple coordinates."""
            return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
        animals_in_range = find_animals_in_range(keeper)
        if animals_in_range != []:
            furthest = 0
            furthest_animal = None
            #LEARN ENUMERATE
            for animal in range(len(animals_in_range)):
                for loc in range(len(self.path)):
                    if animals_in_range[animal]['loc'] == self.path[loc] and loc > furthest:
                        furthest = loc
                        furthest_animal = animals_in_range[animal]
            velocity = Constants.KEEPER_INFO[keeper['type']]['throw_speed_mag']
            smallest_time_steps = float('inf')
            smallest_time_coord = None
            for i in range(len(self.path)):
                if furthest < i:
                    timesteps_to_coord = (i - furthest)/furthest_animal['temp_speed']
                    radius = distance(keeper['loc'], self.path[i])
                    timesteps_from_food = (radius)/Constants.KEEPER_INFO[keeper['type']]['throw_speed_mag']
                    time = abs(timesteps_to_coord - timesteps_from_food)
                    if time < smallest_time_steps:
                        smallest_time_steps = time
                        smallest_time_coord = self.path[i]
            radi = distance(keeper['loc'], smallest_time_coord)
            unit_x = (smallest_time_coord[0] - keeper['loc'][0])/radi
            unit_y = (smallest_time_coord[1] - keeper['loc'][1])/radi
            if keeper['type'] == "PsychopathicZookeeper":
                self.formations.add_formation_food(keeper['loc'], velocity, unit_x, unit_y, keeper, smallest_time_coord)
            else:
                self.formations.add_formation_food(keeper['loc'], velocity, unit_x, unit_y, keeper)
            return True
        return False






################################################################################
################################################################################


    def timestep(self, mouse=None):
        # New spec for timestep(self, mouse):
        # (0. Do not take any action if the player is already defeated.)
        # 1. Compute the new speed of animals based on the presence of nearby VHS cassettes or demons.
        # 2. Compute any changes in formation locations and remove any off-board formations.
        # 3. Handle any food-animal collisions, and remove the fed animals and the eaten food.
        # 4. Upgrade trainee zookeeper if needed.
        # 5. Throw new food if possible.
        # 6. Spawn a new animal from the path's start if needed.
        # 7. Handle mouse input, which is the integer tuple coordinate of a player's click, the string label of a particular
        #   zookeeper type, or None.
        # 8. Redeem one dollar per animal fed this timestep.
        # 9. Check for the losing condition.
        #STEP 0
        # print(self.money, 'money')
        # print(self.formations.formation)
        if self.status == 'defeat':
            return None
        #STEP 1 and 2
        #Removes objects that are now off the screen
        self.formation_movement()
        formations_to_remove = []
        for formation_dict in self.formations.formations:
            if formation_dict['loc'][0] < 0 or formation_dict['loc'][0] > self.width:
                formations_to_remove.append(formation_dict)
                continue
            if formation_dict['loc'][1] < 0 or formation_dict['loc'][1] > self.height:
                formations_to_remove.append(formation_dict)
        for object in formations_to_remove:
            self.formations.formations.remove(object)
        #STEP 3 and 4
        self.bomb_animal_collisions()
        self.food_animal_collisions()
        for keeper in self.formations.keepers:
            if keeper['type'] == 'TraineeZookeeper':
                if keeper['threshold'] <= 0:
                    keeper['type'] = 'SpeedyZookeeper'
                    keeper['texture'] = '1f472'
        #STEP 5
        # print(self.formations.keepers)
        for keeper in self.formations.keepers:
            if keeper['type'] == 'SleepingZookeeper':
                keeper['threshold'] -= 1
                if keeper['threshold'] == 0:
                    keeper['type'] = 'CrazyZookeeper'
                    keeper['texture'] = '1f61c'
            elif keeper['type'] == 'PsychopathicZookeeper':
                if keeper['threshold'] > 0:
                    keeper['threshold'] -= 1
                if keeper['threshold'] == 0:
                    if self.throw_food(keeper):
                        keeper['threshold'] = Constants.PSYCHO_COOLDOWN
            else:
                if keeper['type'] == 'CrazyZookeeper':
                    if self.throw_food(keeper):
                        keeper['threshold'] = Constants.CRAZY_NAP_LENGTH
                        keeper['type'] = 'SleepingZookeeper'
                        keeper['texture'] = '1f634'
                else:
                    self.throw_food(keeper)
        #STEP 6
        self.time_to_spawn -= 1
        if self.time_to_spawn == 0:
            self.formations.add_formation_animal(self.path_corners[0], self.animal_speed)
            self.time_to_spawn = self.spawn_interval
        #STEP 7
        if type(mouse) == str:
            self.keeper_type = mouse
        if type(mouse) == tuple:
            if self.keeper_type in Constants.KEEPER_INFO:
                if Constants.KEEPER_INFO[self.keeper_type]['price'] <= self.money:
                    if self.find_collisions(mouse, Constants.KEEPER_WIDTH, Constants.KEEPER_HEIGHT):
                        self.money -= Constants.KEEPER_INFO[self.keeper_type]['price']
                        if self.keeper_type == 'TraineeZookeeper':
                            self.formations.add_formation_keeper(mouse, self.keeper_type, Constants.TRAINEE_THRESHOLD)
                        elif self.keeper_type == 'PsychopathicZookeeper':
                            self.formations.add_formation_keeper(mouse, self.keeper_type, 1)
                        else:
                            self.formations.add_formation_keeper(mouse, self.keeper_type, 0)
                        self.keeper_type = None
                else:
                    raise NotEnoughMoneyError
            elif self.keeper_type == 'Demon':
                if Constants.DEMON_PRICE <= self.money:
                    if self.find_collisions(mouse, Constants.DEMON_WIDTH, Constants.DEMON_HEIGHT):
                        self.formations.add_formation_demon(mouse)
                        self.money -= Constants.DEMON_PRICE
                        self.keeper_type = None
                else:
                    raise NotEnoughMoneyError
            elif self.keeper_type == 'VHS':
                if Constants.VHS_PRICE <= self.money:
                    if self.find_collisions(mouse, Constants.VHS_WIDTH, Constants.VHS_HEIGHT):
                        self.formations.add_formation_VHS(mouse)
                        self.money -= Constants.VHS_PRICE
                        self.keeper_type = None
                else:
                    raise NotEnoughMoneyError
        #STEP 8
        self.money += self.animals_fed
        self.animals_fed = 0
        #STEP 9
        self.check_game_status()






################################################################################
################################################################################
# TODO: Add additional classes here.
class Formations:
    def __init__(self):
        self.formations = []
        self.animals = []
        self.food = []
        self.keepers = []
        self.rocks = []
        self.demons = []
        self.VHS = []
    def add_formation_keeper(self, loc, type, threshold = None):
         new_formation = {}
         new_formation['loc'] = loc
         new_formation['size'] = (Constants.KEEPER_WIDTH, Constants.KEEPER_HEIGHT)
         new_formation['texture'] = Constants.TEXTURES[type]
         new_formation['type'] = type
         new_formation['threshold'] = threshold
         self.formations.append(new_formation)
         self.keepers.append(new_formation)
    def add_formation_food(self, loc, velocity, unit_x, unit_y, keeper_type = None, end = None, fed = None):
         new_formation = {}
         new_formation['loc'] = loc
         new_formation['size'] = (Constants.FOOD_WIDTH, Constants.FOOD_HEIGHT)
         if end != None:
             new_formation['texture'] = Constants.TEXTURES['Bomb']
         else:
            new_formation['texture'] = Constants.TEXTURES['food']
         new_formation['velocity'] = velocity
         new_formation['unit_x'] = unit_x
         new_formation['unit_y'] = unit_y
         new_formation['keeper_type'] = keeper_type
         new_formation['end'] = end
         new_formation['fed'] = fed
         self.food.append(new_formation)
         self.formations.append(new_formation)
    def add_formation_animal(self, loc, speed):
         new_formation = {}
         new_formation['loc'] = loc
         new_formation['size'] = (Constants.ANIMAL_WIDTH, Constants.ANIMAL_HEIGHT)
         new_formation['texture'] = Constants.TEXTURES['animal']
         new_formation['speed'] = speed
         new_formation['temp_speed'] = speed
         self.animals.append(new_formation)
         self.formations.append(new_formation)
    def add_formation_rock(self, loc):
         new_formation = {}
         new_formation['loc'] = loc
         new_formation['size'] = (Constants.ROCK_WIDTH, Constants.ROCK_HEIGHT)
         new_formation['texture'] = Constants.TEXTURES['rock']
         self.rocks.append(new_formation)
         self.formations.append(new_formation)
    def add_formation_demon(self, loc):
        new_formation = {}
        new_formation['loc'] = loc
        new_formation['size'] = (Constants.DEMON_WIDTH, Constants.DEMON_HEIGHT)
        new_formation['texture'] = Constants.TEXTURES['Demon']
        self.formations.append(new_formation)
        self.demons.append(new_formation)
    def add_formation_VHS(self, loc):
        new_formation = {}
        new_formation['loc'] = loc
        new_formation['size'] = (Constants.VHS_WIDTH, Constants.VHS_HEIGHT)
        new_formation['texture'] = Constants.TEXTURES['VHS']
        self.formations.append(new_formation)
        self.VHS.append(new_formation)
    def remove_animal(self, animal):
        if animal in self.animals:
            self.animals.remove(animal)
        if animal in self.formations:
            self.formations.remove(animal)

################################################################################
################################################################################
if __name__ == '__main__':
    pass
