# Reference systems

Profiles of example agentic systems: the question-answering bot used throughout the documentation, and the three worked examples in the [guide for AI developers](../../docs/implementation/for-ai-developers.md). A profile lists a system's capabilities, how each is used (authority, and whether its effects are irreversible or external), and its conditional components.

```bash
python skills/arc-assessment/scripts/arc.py --register arc-risk-register assess --profile examples/systems/fact-checker.yaml
```

The counts quoted in the developer guide are checked against these profiles by `skills/tests/test_arc_assessment.py`, so the guide cannot drift from the register. They are also the starting set for validating ARCvisor and the assessment skill against expert assessments; see [Keeping the register current](../../docs/arc_framework/keeping-current.md).
