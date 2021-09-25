class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        height = len(grid)
        width = len(grid[0])
        self.adaptee.set_dim((width, height))
        lights = []
        obstacles = []
        for i in range(height):
            for j in range(width):
                if grid[i][j] == 1:
                    lights.append((j, i))
                elif grid[i][j] == -1:
                    obstacles.append((j, i))
        self.adaptee.set_obstacles(obstacles)
        self.adaptee.set_lights(lights)
        return self.adaptee.generate_lights()
