from system_role import system_role
from Local_Agent import LocalAgent
import re


# Implement function action that calculate operations of String type.
# e.g. calculate: "4 * 7 / 3"
def calculate(what):
    return eval(what)


# Implement function action that returns the mass of a planet in the solar system
def planet_mass(name):
    masses = {
        "Mercury": 0.33011,
        "Venus": 4.8675,
        "Earth": 5.972,
        "Mars": 0.64171,
        "Jupiter": 1898.19,
        "Saturn": 568.34,
        "Uranus": 86.813,
        "Neptune": 102.413,
    }
    return (masses[name], f"{name} has a mass of {masses[name]} × 10^24 kg")


known_actions = {"calculate": calculate, "planet_mass": planet_mass}
action_re = re.compile(r"^Action: (\w+): (.*)$")


def query_interactive():
    # Create the agent
    bot = LocalAgent(system_role)
    current_prompt = input("You: ")
    result = bot(current_prompt)
    while True:
        actions = [action_re.match(line) for line in result.split('\n') if action_re.match(line)]
        action, action_input = actions[0].groups()
        if not actions:
            break
        if actions[0].groups()[0] == "Answer":
            result = re.sub(r"Action: Answer:", "Final Answer:", result)
            print(f"Bot: {result}")
            # print(type(result))
            break
        # print(f"Actions: {actions}")
        # [<re.Match object; span=(0, 28), match='Action: planet_mass: Jupiter'>]
        # print(f"Actions: {actions}")

        # print(f"Mo: {actions[0].groups()}")
        # ('planet_mass', 'Jupiter')
        # ('Answer', 'The combined mass of Jupiter and Uranus is 1985.003 × 10^24 kg')

        print("Bot:", result)
        if action not in known_actions:
            print(f"Unknown action: {action}: {action_input}")
            break
        print(f" --> running {action} {action_input}")
        if action == "planet_mass":
            mass, observation = known_actions[action](action_input.strip())
            observation = f"Observation: {observation}"
            # print(f"{observation}")
            # print(f"mass: {mass}, description: {description}")
            # mass: 1898.19, description: Jupiter has a mass of 1898.19 × 10^24 kg
            observation = f"{observation}"
        else:
            observation = f"Observation: {known_actions[action](action_input)}"
        print(observation)
        current_prompt += f"\n{observation}"
        result = bot(current_prompt)
        print('------------------')
    # print("Final Answer:", result)


if __name__ == "__main__":
    query_interactive()

"""
the Output is as follows:

You: What is the combined mass of Jupiter and Uranus?
Bot: Step 1:
Thought: I need to find the masses of Jupiter and Uranus. Let’s start with Jupiter.
Action: planet_mass: Jupiter
PAUSE
 --> running planet_mass Jupiter
Observation: Jupiter has a mass of 1898.19 × 10^24 kg
------------------
Bot: Step 2:
Thought: Now I need to find the mass of Uranus.
Action: planet_mass: Uranus
PAUSE
 --> running planet_mass Uranus
Observation: Uranus has a mass of 86.813 × 10^24 kg
------------------
Bot: Step 3:
Thought: I need to calculate the sum of Jupiter's and Uranus’ masses.
Action: calculate: 1898.19 + 86.813
PAUSE
 --> running calculate 1898.19 + 86.813
Observation: 1985.0030000000002
------------------
Bot: Step 4:
Thought: The calculation is complete, I can now provide the final answer.
Final Answer: The combined mass of Jupiter and Uranus is 1985.003 × 10^24 kg

Process finished with exit code 0
"""
