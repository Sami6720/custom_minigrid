from Minigrid.minigrid.core.grid import Grid
from Minigrid.minigrid.core.world_object import Goal, Wall
from Minigrid.minigrid.minigrid_env import MiniGridEnv, MissionSpace
from Minigrid.minigrid.core.world_object import Door, Key


class DoorKeyCustom(MiniGridEnv):
    def __init__(
        self,
        size=6,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        max_steps: int | None = None,
        **kwargs,
    ):
        print(kwargs)
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        self.key_pos = kwargs['key_pos'] 
        self.key_present = kwargs['key_present']
        self.door_locked = kwargs['door_locked']
        self.wall_column = kwargs['wall_column']
        self.door_posn = kwargs['door_posn']

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

        self.grid.set(self.wall_column, self.door_posn, Door('yellow', is_locked=self.door_locked))
        self.grid.set(self.key_pos[0], self.key_pos[1], Key('yellow'))
