import sys

sys.path.append("E:\\my-projs\\research\\mga2\\mga")

if True:
    from PIL import Image
    import numpy as np
    import gymnasium as gym
    from doorkey_custom import DoorKeyCustom


class States():

    def __init__(self,
                 agent_loc=(1, 1),
                 agent_orient=3,
                 key_loc=(1, 2),
                 key_present=True,
                 door_locked=False,
                 wall_col=3,
                 door_pos_in_wall=2):

        self.env = DoorKeyCustom(
            size=6,
            agent_start_pos=agent_loc,
            agent_start_dir=agent_orient,
            key_pos=key_loc,
            key_present=key_present,
            door_locked=door_locked,
            wall_column=wall_col,
            door_posn=door_pos_in_wall
        )

        self.env.reset()
        self.frame_name = f'agent_loc_{agent_loc}_agent_orient_{agent_orient}_key_loc_{key_loc}_key_present_{key_present}_door_open_{door_locked}_wall_col_{wall_col}_door_pos_in_wall_{door_pos_in_wall}.png'

    def print_frame(self):

        frame = self.env.get_frame()

        img_obj = Image.fromarray(frame.astype(np.uint8))
        img_obj.save(
            f'{self.frame_name}')


if __name__ == '__main__':

    state = States()
    state.print_frame()
