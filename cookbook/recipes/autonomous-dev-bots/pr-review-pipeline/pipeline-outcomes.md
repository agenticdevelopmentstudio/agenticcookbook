
| Outcome | Description | Next action |
|---------|-------------|-------------|
| Accept | Passes all phases, high value | Human reviewer approves, PR is mergeable |
| Accept with refactoring | Has value, needs structural changes | Refactoring agent applies changes, pipeline reruns |
| Partial accept | Some parts valuable, others not | Proposal extracts good parts, rejects rest. Human decides. |
| Reject | No parts meet the bar | Detailed per-section rationale posted. Contributor can appeal. |
| Reject with appeal | Contributor disputes rejection | Human reviewer evaluates the appeal |

