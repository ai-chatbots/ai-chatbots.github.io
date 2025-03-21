# aion_agents.py

class Agent:
    def __init__(self, name: str, prompt: str):
        """
        Initialize an agent with a name and a prompt.
        """
        self.name = name
        self.prompt = prompt

    def run(self, input_text: str, memory: dict = None) -> str:
        """
        Process the input text.
        In a real implementation, this method might call the OpenAI API
        using self.prompt and the input_text to produce a response.
        Here, we simulate a response.
        """
        # Dummy processing logic:
        response = f"[{self.name}]: Processed '{input_text}' with prompt '{self.prompt}'"
        return response


class Memory:
    def __init__(self):
        """
        Initialize a simple in-memory dictionary to store agent outputs.
        """
        self.data = {}

    def add(self, key: str, value: str):
        """
        Save the agent's output.
        """
        self.data[key] = value

    def get(self, key: str):
        """
        Retrieve the saved output for an agent.
        """
        return self.data.get(key, None)


class Controller:
    def __init__(self, agents: list):
        """
        Initialize the controller with a list of agents and a Memory instance.
        """
        self.agents = agents
        self.memory = Memory()

    def run(self, user_input: str) -> str:
        """
        Process the user input through each agent sequentially.
        Each agent's output is saved in memory and used as the input for the next agent.
        """
        current_input = user_input
        for agent in self.agents:
            output = agent.run(current_input, self.memory.data)
            self.memory.add(agent.name, output)
            current_input = output  # Pass the output to the next agent
        return current_input


# Example usage (if run as a script)
if __name__ == "__main__":
    researcher = Agent("Researcher", prompt="Gather relevant info")
    summarizer = Agent("Summarizer", prompt="Summarize the content")
    controller = Controller([researcher, summarizer])
    final_output = controller.run("What is GenAI?")
    print("Final Output:", final_output)
