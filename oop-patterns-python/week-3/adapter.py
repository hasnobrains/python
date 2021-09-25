#  Adapting Light to System.get_lightening

from mapping_adapter import MappingAdapter


class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены
        self.map[10][11] = 1  # Источники света
        self.map[15][22] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


system = System()
height = len(system.grid)
width = len(system.grid[0])
for i in range(height):
    for j in range(width):
        print(f"{system.grid[i][j]} ", end="")
    print("\n")

light = Light((0, 0))
adapter = MappingAdapter(light)
system.get_lightening(adapter)
