from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

"""
Intelligent Systems
Agent with pysc2
24/03/2020

Dante Flores Moreno     A01207543
Arturo Guevara Chávez   A01272373
Andrés Quiroz Duarte    A01400033

"""

# Creating the class of the agent
class ZergAgent(base_agent.BaseAgent):

    def unit_type_is_selected(self, obs, unit_type):    # Check if the selected unit types are the expected ones
        if (len(obs.observation.single_select) > 0 and
        obs.observation.single_select[0].unit_type == unit_type):
            return True
        
        if (len(obs.observation.multi_select) > 0 and
            obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]

    def step(self, obs):    # At the end of every step the agent must do an action
        super(ZergAgent, self).step(obs)
        spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
        if len(spawning_pools) == 0:
            if self.unit_type_is_selected(obs, units.Zerg.Drone):
                if (actions.FUNCTIONS.Build_SpawningPool_screen.id in 
                    obs.observation.available_actions):   # Check if we have enough resources to build a Spawning Pool
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_SpawningPool_screen("now", (x, y))   # Build a Spawning Pool at a random place

            drones = self.get_units_by_type(obs, units.Zerg.Drone)
            if len(drones) > 0:
                drone = random.choice(drones)

                return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))
        return actions.FUNCTIONS.no_op()


def main(unused_argv):
    agent = ZergAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name="Simple64",
                players=[sc2_env.Agent(sc2_env.Race.zerg),                              # First player: Our Agent
                    sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.very_easy)],    # Second player: A predefined bot
                agent_interface_format=features.AgentInterfaceFormat(                   # Screen and minimap setup
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True),                                            # Enable feature units
                step_mul=16,                                                            # Number of steps before the agent choose an action
                game_steps_per_episode=0,                                               # Length of the game
                visualize=True) as env:
                
                # Feed the agent and receive actions until the game ends
                agent.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent.reset()

                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    app.run(main)