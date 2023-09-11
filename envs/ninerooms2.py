from __future__ import annotations

from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Door, Key, Lava
from minigrid.minigrid_env import MiniGridEnv
import numpy as np

class NineRoomsEnv(MiniGridEnv):

    """
    ## Description

    Classic four room reinforcement learning environment. The agent must
    navigate in a maze composed of four rooms interconnected by 4 gaps in the
    walls. To obtain a reward, the agent must reach the green goal square. Both
    the agent and the goal square are randomly placed in any of the four rooms.

    ## Mission Space

    "reach the goal"

    ## Action Space

    | Num | Name         | Action       |
    |-----|--------------|--------------|
    | 0   | left         | Turn left    |
    | 1   | right        | Turn right   |
    | 2   | forward      | Move forward |
    | 3   | pickup       | Unused       |
    | 4   | drop         | Unused       |
    | 5   | toggle       | Unused       |
    | 6   | done         | Unused       |

    ## Observation Encoding

    - Each tile is encoded as a 3 dimensional tuple:
        `(OBJECT_IDX, COLOR_IDX, STATE)`
    - `OBJECT_TO_IDX` and `COLOR_TO_IDX` mapping can be found in
        [minigrid/minigrid.py](minigrid/minigrid.py)
    - `STATE` refers to the door state with 0=open, 1=closed and 2=locked

    ## Rewards

    A reward of '1' is given for success, and '0' for failure.

    ## Termination

    The episode ends if any one of the following conditions is met:

    1. The agent reaches the goal.
    2. Timeout (see `max_steps`).

    ## Registered Configurations

    - `MiniGrid-FourRooms-v0`

    """

    def __init__(self, agent_pos=None, goal_pos=None, max_steps=500, task = 'room2easykey', **kwargs):
        self._agent_default_pos = agent_pos
        self._goal_default_pos = goal_pos

        self.size = 13
        self.task = task
        # print("task is: ", self.task)
        mission_space = MissionSpace(mission_func=self._gen_mission)

        super().__init__(
            mission_space=mission_space,
            width=self.size,
            height=self.size,
            max_steps=max_steps,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "ninerooms"

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        room_w = width // 3
        room_h = height // 3

        # For each row of rooms
        for j in range(0, 3):

            # For each column
            for i in range(0, 3):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                if i + 1 < 3:
                    self.grid.vert_wall(xR, yT, room_h)

                # Bottom wall and door
                if j + 1 < 3:
                    self.grid.horz_wall(xL, yB, room_w)

                if (i == 0 and j == 0) or (i == 0 and j == 1):
                    pos1 = (xR, self._rand_int(yT + 1, yB))
                    self.grid.set(*pos1, None)
                    pos = (self._rand_int(xL + 1, xR), yB)
                    self.grid.set(*pos, None)                         
                    if (i == 0 and j == 0):
                        doorpos = pos1

                if (i == 1 and j == 0) or (i == 1 and j == 1) or (i == 0 and j == 2) or (i == 1 and j == 2):
                    pos = (xR, self._rand_int(yT + 1, yB))
                    self.grid.set(*pos, None)
        # Start from room 1
        if self.task =='room2easykey' or self.task == 'room2hardkey' or self.task == 'room2goal' or self.task == 'room2door':
            agent_x = np.random.randint(low = 1, high = room_w-1)
            agent_y = np.random.randint(low = self.size - room_h, high = self.size-2)
            self._agent_default_pos = (agent_x, agent_y)
        # Start from easy key
        elif self.task == 'easykey2goal' or self.task == 'easykey2door' or self.task == 'easykey2hardkey' or self.task == 'easykey2room':
            agent_x = np.random.randint(low = self.size-room_h, high = self.size-2)
            agent_y = np.random.randint(low = self.size -room_w, high = self.size-2)
            self._agent_default_pos = (agent_x, agent_y)
        # Start from hard key
        elif self.task == 'hardkey2goal' or self.task == 'hardkey2door' or self.task == 'hardkey2easykey' or self.task == 'hardkey2room':
            agent_x = np.random.randint(low = 1, high = room_w-1)
            agent_y = np.random.randint(low = 1, high = room_h-1)
            self._agent_default_pos = (agent_x, agent_y)
        # Start from door
        elif self.task == 'door2goal' or self.task == 'door2room' or self.task == 'door2easykey' or self.task == 'door2hardkey':
            agent_x = np.random.randint(low = room_w + 1, high = self.size - room_w - 2)
            agent_y = np.random.randint(low = 1, high = room_h-1)
            self._agent_default_pos = (agent_x, agent_y)

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            self.grid.set(*self._agent_default_pos, None)
            # assuming random start direction
            self.agent_dir = self._rand_int(0, 4)
        else:
            self.place_agent()


        goal_x = np.random.randint(low = self.size - room_w, high = self.size-2)
        goal_y = np.random.randint(low = 1, high = room_h-1)
        self._goal_default_pos = (goal_x, goal_y)
        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        # # Place a door in the wall
        # doorIdx = self._rand_int(1, width - 2)
        self.doorLocked = Door("yellow", is_locked=True)
        self.doorUnlocked = Door("yellow", is_open=True) 
        if self.task == 'doorgoal':
            self.put_obj(self.doorUnlocked, doorpos[0], doorpos[1])
        else:
            self.put_obj(self.doorLocked, doorpos[0], doorpos[1])

        # Place a yellow key on the left side
        self.keyHard = Key("yellow", 'keyHard')
        self.keyEasy = Key("yellow", 'keyEasy')
        if self.task =='room2easykey' or self.task == 'room2hardkey' or self.task == 'room2goal':
            self.place_obj(obj=self.keyHard, top=(0, 0), size=(room_h, room_w-1))        
            self.place_obj(obj=self.keyEasy, top=(self.size-room_h, self.size-room_w), size=(room_h, room_w))        
        elif self.task == 'easykey2goal' or self.task == 'easykey2door' or self.task == 'easykey2hardkey' or self.task == 'easykey2room':
            self.place_obj(obj=self.keyHard, top=(0, 0), size=(room_h, room_w-1))        
        elif self.task == 'hardkey2goal' or self.task == 'hardkey2door' or self.task == 'hardkey2easykey' or self.task == 'hardkey2goal':
            self.place_obj(obj=self.keyEasy, top=(self.size-room_h, self.size-room_w), size=(room_h, room_w))        

        self.obstacle_type = Lava
        # self.grid.vert_wall(2, 7, 2, self.obstacle_type)
        # self.grid.vert_wall(3, 7, 2, self.obstacle_type)
        self.grid.horz_wall(2, 6, 9, self.obstacle_type)
        self.grid.set(*(4,5), None)
        self.grid.set(*(4,7), None)   
        self.grid.set(*(8,5), None)
        self.grid.set(*(8,7), None)           

        # #Bottom row all clear
        # self.grid.set(*(4,9), None)   
        # self.grid.set(*(4,10), None)   
        # self.grid.set(*(4,11), None)   
        # self.grid.set(*(8,9), None)   
        # self.grid.set(*(8,10), None)   
        # self.grid.set(*(8,11), None)           

        # #Above lava all clear
        # self.grid.set(*(1,4), None)
        # self.grid.set(*(2,4), None)           
        # self.grid.set(*(3,4), None)           

        # # Below lava center clear
        # self.grid.set(*(3,8), None)           