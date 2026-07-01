from agentic_learning.agent_loop import AgentAction, AgentContext, AgentLoop, AgentOutput
from agentic_learning.evals import EvaluationCase, run_evaluation_suite
from agentic_learning.governance import GovernancePolicy


def plan(context: AgentContext):
    return [AgentAction(kind="write", detail=context.goal)]


def respond(context: AgentContext, actions):
    return AgentOutput(summary=f"Planned {len(actions)} action(s) for: {context.goal}", actions=actions)


def main() -> None:
    loop = AgentLoop()
    context = AgentContext(goal="learn agentic coding")
    output = loop.run(context, plan, respond)

    policy = GovernancePolicy(blocked_prefixes=("delete:",))
    review = policy.review("write:docs")

    report = run_evaluation_suite(
        [EvaluationCase(name="uppercase", input_text="hello", expected_output="HELLO")],
        runner=str.upper,
    )

    print(output.summary)
    print(review.decision.allowed)
    print(report.score)


if __name__ == "__main__":
    main()
