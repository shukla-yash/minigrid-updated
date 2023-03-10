# minigrid-updated
Updated minigrid

Minigrid path: {path-to-miniconda3/anaconda}/envs/{Name-of-env}/lib/{python-version}/site-packages/minigrid


<div align='center'>
  Environment and its corresponding task automaton
  <img alt="Environment and its corresponding task automaton" src="assets/env_automaton.png">
</div>

Environmets:

(1) ```MiniGrid-NineRoomsEasyKey-v0``` - Get the EasyKey 

(2) ```MiniGrid-NineRoomsHardKey-v0``` - Get the HardKey

(3) ```MiniGrid-NineRoomsEasyKeyGoal-v0``` - Start with the EasyKey in inventory, and reach the goal. Agent start state is the room EasyKey is in.

(4) ```MiniGrid-NineRoomsHardKeyGoal-v0``` - Start with the HardKey in inventory, and reach the goal. Agent start state is the room HardKey is in.

(5) ```MiniGrid-NineRoomsKeyEasyDoor-v0``` - Start with the EasyKey in inventory, and open the door. Agent start state is the room EasyKey is in.

(6) ```MiniGrid-NineRoomsKeyHardDoor-v0``` - Start with the HardKey in inventory, and open the door. Agent start state is the room HardKey is in.

(7) ```MiniGrid-NineRoomsDoorGoal-v0``` - Start with the door opened, and reach the goal. Agent start state is to the right of the door.

(8) ```MiniGrid-NineRoomsKeyGoal-v0``` - Entire task. Get any key, open the door, and reach the goal.
