from agentic_learning.governance import GovernancePolicy


def test_governance_allows_safe_action() -> None:
    policy = GovernancePolicy(blocked_prefixes=("delete:", "publish:"))

    decision = policy.evaluate("write:docs")

    assert decision.allowed is True
    assert decision.reasons == ()


def test_governance_blocks_disallowed_action() -> None:
    policy = GovernancePolicy(blocked_prefixes=("delete:", "publish:"))

    decision = policy.evaluate("delete:all")

    assert decision.allowed is False
    assert decision.reasons == ("blocked prefix: delete:",)
