from Minigrid.minigrid.core.grid import Grid
from Minigrid.minigrid.core.world_object import Goal, Wall
from Minigrid.minigrid.minigrid_env import MiniGridEnv, MissionSpace
from Minigrid.minigrid.core.world_object import Door, Key
import random
import numpy as np
from PIL import Image


class DoorKeyCustom(MiniGridEnv):
    def __init__(
        self,
        size=6,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        self.key_pos = kwargs['key_pos']
        self.key_present = kwargs['key_present']
        self.door_locked = kwargs['door_locked']
        self.wall_column = kwargs['wall_column']
        self.door_coords = kwargs['door_coord']

        mission_space = MissionSpace(mission_func=self._gen_mission)

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            max_steps=256,
            # **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "grand mission"

    def _gen_grid(self, width, height):

        self.grid = Grid(width, height)

        self.grid.wall_rect(0, 0, width, height)

        self.put_obj(Goal(), width - 2, height - 2)

        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        
        for i in range(0, height):
            self.grid.set(self.wall_column, i, Wall())

        self.grid.set(self.door_coords[0], self.door_coords[1],
                      Door('yellow', is_locked=self.door_locked))
        self.grid.set(self.key_pos[0], self.key_pos[1], Key('yellow'))


class RandomCoordGenerator():

    def __init__(self, upper_bound) -> None:
        """Generatre unique coords"""
        
        self.ub = upper_bound
        self.visited = set()

    def generate(self):
        rand_cords = (random.randint(0, self.ub), random.randint(0, self.ub))
        while rand_cords in self.visited:
            rand_cords = (random.randint(0, self.ub),
                          random.randint(0, self.ub))

        self.visited.add(rand_cords)
        return rand_cords

    def reset(self):
        self.visited = set()


class RandomStateGenerator():

    def __init__(self, grid_size):
        self.size = grid_size
        self.atts = ['agent_loc', 'agent_orient', 'key_loc', 'key_present',
                     'door_locked', 'wall_col', 'door_coord']
        self.random_coord_gen = RandomCoordGenerator(upper_bound=self.size - 1)
        self.frame_name = f'frame_{random.randint}.png'

    def generate(self):

        d = {}
        for x in self.atts:
            if x in ('door_locked', 'key_present'):
                d[x] = bool(random.getrandbits(1))
                print(f"{x}: {d[x]}")
                continue
            if x == 'agent_orient':
                d[x] = 2
                print(f"{x}: {d[x]}")
                continue
                
            d[x] = self.random_coord_gen.generate()
            print(f"{x}: {d[x]}")

        # agent_loc_(1, 1)_agent_orient_3_key_loc_(1, 2)_key_present_True_door_open_False_wall_col_3_door_pos_in_wall_2
        self.env = DoorKeyCustom(
            size=self.size,
            agent_start_pos=d["agent_loc"],
            agent_start_dir=d["agent_orient"],
            key_pos=d["key_loc"],
            key_present=d['key_present'],
            door_locked=d['door_locked'],
            wall_column=d['door_coord'][0],
            door_coord=d['door_coord']
        )

        self.env.reset()

        frame = self.env.get_frame()
        img_obj = Image.fromarray(frame.astype(np.uint8))
        img_obj.save(
            f'{self.frame_name}')

        self.random_coord_gen.reset()


if __name__ == '__main__':
    state = RandomStateGenerator(grid_size=6)
    state.generate()
