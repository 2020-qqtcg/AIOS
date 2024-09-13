from pyopenagi.agents.experiment.doraemon_agent.agent import DoraemonAgent
from pyopenagi.agents.experiment.doraemon_agent.moduler.planning.planning import Planning
from pyopenagi.agents.experiment.doraemon_agent.register.planning_register import agent_planning
from pyopenagi.utils.chat_template import Query


@agent_planning("normal")
class PlanningNormal(Planning):

    def plan(self, agent: DoraemonAgent) -> str:
        """Use plan straregy execute agent

        Args:
            agent: agent executing

        Returns: plan result

        """
        query = Query(
            messages=agent.messages.generate_context(), tools=None
        )
        response, start_times, end_times, waiting_times, turnaround_times = agent.get_response(query)

        agent.set_monitor_info(start_times, waiting_times, turnaround_times)

        return response.response_message
