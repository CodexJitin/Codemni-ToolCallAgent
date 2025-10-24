
def init_ReasonCall_Agent(llm, agents):
    from agent.ReasonCall_Agent.agent import ReasonCall_Agent
    from agent.ReasonCall_Agent.prompt import prompt

    agents_list = ", ".join([agent.name for agent in agents])

    formatted_prompt = prompt.format(
        agents_list=agents_list,
        chat_history="{chat_history}",
    )

    return ReasonCall_Agent(
        llm=llm,
        prompt_template=formatted_prompt,
        agents=agents,
    )
    