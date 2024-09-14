from pyopenagi.agents.experiment.doraemon_agent.module.action.action import Action
from pyopenagi.agents.experiment.doraemon_agent.module.action.action_tool import ActionTool
from pyopenagi.agents.experiment.doraemon_agent.module.planning.planning import Planning
from pyopenagi.agents.experiment.doraemon_agent.register.planning_register import agent_planning
from pyopenagi.utils.chat_template import Query
from pyopenagi.utils.logger import AgentLogger

DESC = """Nothing else need to do."""

@agent_planning("normal", DESC)
class PlanningNormal(Planning):

    name: str = "normal"

    def plan(self, agent, logger: AgentLogger) -> str:
        """Use plan straregy execute agent

        Args:
            agent: agent executing
            logger: logger to log

        Returns: plan result

        """
        from pyopenagi.agents.experiment.doraemon_agent.agent import DoraemonAgent
        assert isinstance(agent, DoraemonAgent)

        tools = agent.tools if agent.tools else None
        query = Query(
            messages=agent.messages.generate_context(), tools=tools
        )
        response, start_times, end_times, waiting_times, turnaround_times = agent.get_response(query)

        agent.set_monitor_info(start_times, waiting_times, turnaround_times)

        if response.tool_calls:
            action_tool: Action = agent.take_action("tool")
            assert isinstance(action_tool, ActionTool)

            action_result, tool_call_id = action_tool.run(response)
            agent.messages.generate_context(role="tool", content=action_result, tool_call_id=tool_call_id)
        else:
            agent.messages.generate_context(role="assistant", content=response.response_message)

        content = agent.messages.last_message()["content"]
        logger.log(f"{content}\n", "info")
        return response.response_message
