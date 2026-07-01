from agentic_learning.evals import EvaluationCase, run_evaluation_suite


def test_evaluation_suite_reports_pass_and_failures() -> None:
    report = run_evaluation_suite(
        [
            EvaluationCase(name="ok", input_text="a", expected_output="A"),
            EvaluationCase(name="bad", input_text="b", expected_output="C"),
        ],
        runner=str.upper,
    )

    assert report.total == 2
    assert report.passed == 1
    assert report.failed_cases == ("bad",)
    assert report.score == 0.5
