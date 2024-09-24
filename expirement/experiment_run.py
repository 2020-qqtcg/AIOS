from expirement.agent.experiment_agent import ExpirementAgent
from aios.utils.utils import parse_global_args
from aios.hooks.llm import useKernel, useFIFOScheduler
from expirement.agent.interpreter import InterpreterAgent
from pyopenagi.agents.agent_process import AgentProcessFactory

AGENT_TYPE_MAPPING = {
    "interpreter": InterpreterAgent,
}


def prepare_llm():
    parser = parse_global_args()
    args = parser.parse_args()

    llm = useKernel(
        llm_name=args.llm_name,
        max_gpu_memory=args.max_gpu_memory,
        eval_device=args.eval_device,
        max_new_tokens=args.max_new_tokens,
        log_mode=args.llm_kernel_log_mode,
        use_backend=args.use_backend
    )

    start_scheduler, stop_scheduler = useFIFOScheduler(
        llm=llm,
        log_mode=args.scheduler_log_mode,
        get_queue_message=None
    )

    return start_scheduler, stop_scheduler


def creat_agent(process_factory: AgentProcessFactory, agent_type: str) -> ExpirementAgent:
    agent = AGENT_TYPE_MAPPING[agent_type](process_factory)
    return agent


def run_agent(agent: ExpirementAgent, single_data) -> str:
    input_str = single_data["text"]
    agent.run(input_str)


def main(agent_type: str):
    strat_scheduler, stop_scheduler = prepare_llm()
    process_factory = AgentProcessFactory()

    strat_scheduler()
    agent = creat_agent(process_factory, agent_type)
    agent.run("")


if __name__ == '__main__':
    main("interpreter")
