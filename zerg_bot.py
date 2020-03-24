from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features
from absl import app

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
    def step(self, obs):    # At the end of every step the agent must do an action
        super(ZergAgent, self).step(obs)
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
                    feature_dimensions=features.Dimensions(screen=84, minimap=64)),
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