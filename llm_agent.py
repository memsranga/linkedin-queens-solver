from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from dotenv import find_dotenv, load_dotenv
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import AgentExecutor, create_react_agent
import numpy as np


def solve_n_queens(board):
    load_dotenv(find_dotenv())

    llm = AzureChatOpenAI(model="gpt-4o",
                          temperature=1,
                          api_version="2023-03-15-preview",
                          verbose=True)

    template = """
    You are puzzle solver. Given a {grid_size}x{grid_size} grid, use PuLP to solve the puzzle.
    You should solve the puzzle for the constraints:
    1. Each row sum should be 1
    2. Each column sum should be 1
    3. Each number region sum should be 1
    4. Parwise sum of all adjacent cells, row wise, column wise and diagonally should be <= 1

    Form these constraints using PuLP and solve them for Binary category since all variables can be either 0 or 1.
    Dont give any explanation, execute the code and give me the final answer as 2d array with out any other characters.
    Grid:
    {grid}
    """

    prompt_template = ChatPromptTemplate.from_template(template)

    message = prompt_template.invoke({"grid_size": len(board), "grid": board})

    @tool
    def execute_python_tool(code):
        """
        A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.
        """
        python_repl = PythonREPLTool()
        return python_repl.invoke(code)

    tools = [execute_python_tool]

    prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}")""")

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({"input": message})
    # print(result)    # Original string representing the array
    array_string = result["output"].strip("`")

    # Convert the string to a Python list
    array_list = eval(array_string)

    # Replace 1s with 'Q' and convert to numpy array
    converted_array = np.array([['Q' if cell == 1 else 0 for cell in row] for row in array_list])

    # Display the result
    # print(converted_array)
    return converted_array
