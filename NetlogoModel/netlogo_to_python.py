from math import sqrt

class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    # equality method
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    # hash method
    def __hash__(self):
        return hash((self.x, self.y))
    def __str__(self):
        return str(self.x) + ";" + str(self.y)
    # distance method
    def distance_to(self, other) -> float:
        return sqrt((self.x-other.x)**2+(self.y-other.y)**2)
    
class Agent:
    def __init__(self, coordinates: Coordinates, population: int, copper: int, cattle: int):
        self.coordinates = coordinates
        self.population = population
        self.copper = copper
        self.cattle = cattle
    def __repr__(self):
        result = "Agent at: " + str(self.coordinates) + "\n"
        result += "Agent population: " + str(self.population) + "\n"
        result += "Agent copper: " + str(self.copper) + "\n"
        result += "Agent cattle: " + str(self.cattle)
        return result

class Patch:
    def __init__(self, coordinates: Coordinates, agent: Agent| None, copper: int, cattle: int):
        self.coordinates = coordinates
        self.agent = agent
        self.copper = copper
        self.cattle = cattle
    def __repr__(self):
        result = "Patch at: " + str(self.coordinates) + "\n"
        result += "Patch copper: " + str(self.copper) + "\n"
        result += "Patch cattle: " + str(self.cattle)
        if self.agent != None:
            result += "\nHaving:\n" + str(self.agent)
        return result

class _Patch:
    def __init__(self, coordinates: Coordinates, agent: int, copper: int, cattle: int):
        self.coordinates = coordinates
        self.agent = agent
        self.copper = copper
        self.cattle = cattle

class Step:
    def __init__(self, step_info: dict[Patch, set[tuple[Patch, float]]]):
        self.step_info = step_info

def parse_file(file_name: str) -> dict[int: Step]:
    result = dict()
    file = open(file_name, "r")
    patch_xcor = None
    agent_identifier = None
    patches = None
    current_step_number = 0
    for line in file:
        if line.startswith("Step: "):
            # enough to determine if we've parsed a patch
            if patch_xcor != None:
                patches[Coordinates(patch_xcor, patch_ycor)] = (_Patch(Coordinates(patch_xcor, patch_ycor), patch_agent, patch_copper, patch_cattle))
            # enough to determine if we've parsed an agent
            if agent_identifier != None:
                agents[agent_identifier] = Agent(Coordinates(agent_xcor, agent_ycor), agent_population, agent_copper, agent_cattle)
            # making a map of patches with agent references
            exact_patches = dict()
            if patches != None:
                for key, value in patches.items():
                    if value.agent != None:
                        exact_patches[key] = Patch(value.coordinates, agents[value.agent], value.copper, value.cattle)
                    else:
                        exact_patches[key] = Patch(value.coordinates, None, value.copper, value.cattle)
            # making an adjacency list (in our case it's a set) for each patch
            step_info = dict()
            for key, value in exact_patches.items():
                 adjacency_list = set()
                 if Coordinates(key.x+1, key.y+1) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x+1, key.y+1)], key.distance_to(Coordinates(key.x+1, key.y+1))))
                 if Coordinates(key.x+1, key.y) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x+1, key.y)], key.distance_to(Coordinates(key.x+1, key.y))))
                 if Coordinates(key.x+1, key.y-1) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x+1, key.y-1)], key.distance_to(Coordinates(key.x+1, key.y-1))))
                 if Coordinates(key.x, key.y+1) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x, key.y+1)], key.distance_to(Coordinates(key.x, key.y+1))))
                 if Coordinates(key.x, key.y-1) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x, key.y-1)], key.distance_to(Coordinates(key.x, key.y-1))))
                 if Coordinates(key.x-1, key.y+1) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x-1, key.y+1)], key.distance_to(Coordinates(key.x-1, key.y+1))))
                 if Coordinates(key.x-1, key.y) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x-1, key.y)], key.distance_to(Coordinates(key.x-1, key.y))))
                 if Coordinates(key.x-1, key.y-1) in exact_patches:
                     adjacency_list.add((exact_patches[Coordinates(key.x-1, key.y-1)], key.distance_to(Coordinates(key.x-1, key.y-1))))
                 step_info[value] = adjacency_list
            result[current_step_number] = Step(step_info)
            # resetting temp variables
            patches = dict()
            agents = dict()
            current_mode = None
            agent_identifier = None
            agent_xcor = None
            agent_ycor = None
            agent_population = None
            agent_copper = None
            agent_cattle = None
            patch_xcor = None
            patch_ycor = None
            patch_agent = None
            patch_copper = None
            patch_cattle = None
            current_step_number = int(line.replace("Step: ", ""))  
        # checking what we are parsing
        elif line == "Patch" or line == "Patch\n":
            # enough to determine if we've parsed a patch
            if patch_xcor != None:
                patches[Coordinates(patch_xcor, patch_ycor)] = (_Patch(Coordinates(patch_xcor, patch_ycor), patch_agent, patch_copper, patch_cattle))
            # enough to determine if we've parsed an agent
            if agent_identifier != None:
                agents[agent_identifier] = Agent(Coordinates(agent_xcor, agent_ycor), agent_population, agent_copper, agent_cattle)
            # resetting temp variables
            agent_identifier = None
            agent_xcor = None
            agent_ycor = None
            agent_population = None
            agent_copper = None
            agent_cattle = None
            patch_xcor = None
            patch_ycor = None
            patch_agent = None
            patch_copper = None
            patch_cattle = None
            current_mode = "Patch"
        elif line == "Agent" or line == "Agent\n":
            # enough to determine if we've parsed a patch
            if patch_xcor != None:
                patches[Coordinates(patch_xcor, patch_ycor)] = (_Patch(Coordinates(patch_xcor, patch_ycor), patch_agent, patch_copper, patch_cattle))
            # enough to determine if we've parsed an agent
            if agent_identifier != None:
                agents[agent_identifier] = Agent(Coordinates(agent_xcor, agent_ycor), agent_population, agent_copper, agent_cattle)
            # resetting temp variables
            agent_identifier = None
            agent_xcor = None
            agent_ycor = None
            agent_population = None
            agent_copper = None
            agent_cattle = None
            patch_xcor = None
            patch_ycor = None
            patch_agent = None
            patch_copper = None
            patch_cattle = None
            current_mode = "Agent"
        # agent ID at patch
        elif line.startswith("Agent: "):
            if current_mode == "Patch":
                patch_agent = int(line.replace("Agent: ", ""))
            elif current_mode == "Agent":
                raise Exception("Got agent ID while parsing agent ID at patch")
            else:
                raise Exception("Undefined if parsing Patch or Agent")
        # agent ID
        elif line.startswith("Identifier: "):
            if current_mode == "Agent":
                agent_identifier = int(line.replace("Identifier: ", ""))
            elif current_mode == "Patch":
                raise Exception("Got agent ID at patch while parsing agent ID")
            else:
                raise Exception("Undefined if parsing Patch or Agent")
        # X coordinate
        elif line.startswith("X coordinate: "):
            if current_mode == "Patch":
                patch_xcor = int(line.replace("X coordinate: ", ""))
            elif current_mode == "Agent":
                agent_xcor = int(line.replace("X coordinate: ", ""))
            else:
                raise Exception("Undefined if parsing Patch or Agent")
        # Y coordinate
        elif line.startswith("Y coordinate: "):
            if current_mode == "Patch":
                patch_ycor = int(line.replace("Y coordinate: ", ""))
            elif current_mode == "Agent":
                agent_ycor = int(line.replace("Y coordinate: ", ""))
            else:
                raise Exception("Undefined if parsing Patch or Agent")
        # agent population
        elif line.startswith("Population: "):
            if current_mode == "Agent":
                agent_population = int(line.replace("Population: ", ""))
            elif current_mode == "Patch":
                raise Exception("Got population while parsing agent")
            else:
                raise Exception("Undefined if parsing Patch or Agent")
        # copper
        elif line.startswith("Copper: "):
            if current_mode == "Patch":
                patch_copper = int(line.replace("Copper: ", ""))
            elif current_mode == "Agent":
                agent_copper = int(line.replace("Copper: ", ""))
            else:
                raise Exception("Undefined if parsing Patch or Agent")
        # cattle
        elif line.startswith("Cattle: "):
            if current_mode == "Patch":
                patch_cattle = int(line.replace("Cattle: ", ""))
            elif current_mode == "Agent":
                agent_cattle = int(line.replace("Cattle: ", ""))
            else:
                raise Exception("Undefined if parsing Patch or Agent")
        # ignoring kill messages
        elif line == "defender has killed the attacker" or line == "attacker has killed the defender" or "defender has killed the attacker\n" or line == "attacker has killed the defender\n":
            pass
        # ignoring empty lines
        elif line.replace("\t", "").replace(" ", "") == "" or line.replace("\t", "").replace(" ", "") == "\n":
            pass
        else:
            raise Exception("Unexpected line: "+line)
    return result

if __name__ == "__main__":
    adjacency_list_for_steps = parse_file("input.txt")
    for key, value in adjacency_list_for_steps[0].step_info.items():
        print("Base patch:", key, sep="\n")
        print("\nAdjacent patches:")
        for val in value:
            print(val[0])
            print("Distance:", val[1], end="\n\n") 
