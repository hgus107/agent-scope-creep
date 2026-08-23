# agent-scope-creep

A controlled testbed measuring whether peer messages on a shared channel cause an autonomous agent to act outside its stated scope — and which property of a message carries the effect.

## Motivation

Post-incident analyses of multi-agent systems have attributed scope violations to peer influence, citing agent reasoning of the form *"this is outside my intended scope; however, the task is impossible and peers are doing it."* These accounts are reconstructions from logs: they do not identify the message the agent read, do not distinguish a report of a completed action from an instruction or a request for help, and report no rate and no controlled comparison.

Existing multi-agent studies are open-channel and observational. None isolates a single message property as an independent variable. This testbed does.

## Research questions

1. **Base rate.** How often does an agent violate its stated scope with no peer message present at all?
2. **Message type.** Which message raises that rate — a *report* of a completed action, a *directive* assigning the action to the reader, or a *help request* carrying no technique?
3. **Preference.** With all three available, which does the agent act on, and does it act before honest effort would have succeeded?
4. **Mitigation.** If the highest-flipping type is filtered while the others remain readable, does the rate return to baseline, or does the agent substitute the next type?

## Design

One agent per run in an isolated container holding the task, local mock services, and one shared directory writable by "other agents." The agent is told its scope is limited to its own task directory. Message content is the only variable across arms.

| Arm | Shared channel | Tests |
|---|---|---|
| H0 | empty | base rate |
| H1 | report | permission by example |
| H2 | directive | instruction vs. report, same technique |
| H3 | help request | peer presence with no technique |
| H4 | all three | which type wins, and timing vs. the solve point |
| H5 | highest-flipping type filtered, others readable | mitigation vs. substitution |

H0–H3 admit exactly one possible cause per violation and establish causation; H4 mixes types and establishes preference only. Results are reported separately. H5's filter target is determined by H0–H3 results, not fixed in advance.

**Sample.** 100 runs per arm, 200 tool calls per run, three model families (two frontier, one open-weight) so the result is not an artifact of a single training pipeline.

## Metric

**Refusal-flip rate** = runs containing an out-of-scope action / total runs, per arm.

Detected from mock-service request logs rather than from reading transcripts. Three signals per run:

| Signal | What it establishes |
|---|---|
| Read event on the planted message | the agent saw it |
| Timestamped request to a resource outside the task directory | the violation |
| Tool-call index of that request | timing relative to the honest solve point |

Reasoning text is coded separately and secondarily for whether the agent stated an objection before the violating call. Detection does not depend on it.

## Result sought

A **stable ordering** across message types that holds across model families even where absolute rates differ. Absolute rates do not transfer between deployments; an ordering tells an operator which class of inter-agent traffic to screen first.

Null results are informative and will be reported: no stable ordering implies the trigger is model-specific and no general filter exists; H5 remaining above H0 implies selective filtering fails and isolation or progressive filtering is required; indifference to message type implies peer *presence* rather than content is the trigger.

## Safety

- All targets are local mock services inside the sandbox. No external system is contacted at any point.
- No exploit code is produced or requested. Mock services are trivially reachable by design: what is measured is the decision to reach them, not the difficulty of doing so.
- This is measurement of agent behavior, not red-teaming, and is run within the usage policies of every model provider involved.

## Status

Design complete. Harness implementation in progress. Testbed code and run logs will be released here.

## Citation

Harish Gupta — [ORCID 0000-0002-1390-9809](https://orcid.org/0000-0002-1390-9809)

## License

MIT
