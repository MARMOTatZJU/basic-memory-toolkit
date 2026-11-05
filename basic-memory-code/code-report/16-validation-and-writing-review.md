# Validation and writing review

[Collection index](README.md)

## Completed report checks

| Check | Result | Limit |
| --- | --- | --- |
| Source snapshot | Commit and central file fingerprints recorded. | The temporary checkout is a shallow snapshot. |
| Source links | All pinned repository targets resolve to a path in the checkout. | No separate HTTP availability check ran for each link. |
| Source line anchors | Every cited line falls inside its source file. | A valid line number alone does not prove a claim. |
| Internal links | Report navigation targets exist. | Example links inside code are illustrative. |
| Markdown fences | Code fences are balanced. | No separate Markdown rendering engine test ran. |
| General prompt catalog | 72 unique case IDs. | The prompts were not executed against a live knowledge base. |
| Graph prompt catalog | 96 unique case IDs. | Exact analysis cases require their stated added components. |
| Development catalog | 60 unique direction IDs. | Priorities and effort scores are survey judgments. |
| Harness catalog | 32 unique system IDs. | These designs are proposals. |
| MCP inventory | 40 exported decorated tools accounted for. | Configuration can hide registered tools. |
| HTTP inventory | 48 core route declarations accounted for. | Automatic framework routes and hosted-only routes are outside this count. |
| Standalone graph algorithm | The example passed closure, cycle, and empty-graph assertions. | This checks the authored example, not Basic Memory itself. |
| Source checkout | The surveyed repository remained clean. | No product code was changed. |

## Original survey execution status

Basic Memory was not installed or executed during the original survey.
The repository requires Python 3.12 or later. The available shell interpreter is Python 3.10.
No repository unit tests, integration tests, migrations, embedding downloads, or hosted tests ran.
Existing test files supplied static evidence only.

## Tutorial verification update: 2026-11-03

The later tutorial update installed and exercised Basic Memory 1.0.0 in isolated temporary directories.
All 54 Bash blocks in the final tutorial passed in order in a fresh environment.
Eighteen focused content and protocol assertions also passed.
A separate backup check confirmed SQLite integrity and copied content.

The checks covered text and semantic retrieval, graph context, updates, schemas, CSV import, MCP, and export.
The repository test suite was not run.
PDF/Office extras and desktop client setup remain outside the executed paths.
See [the tutorial](17-user-tutorial.md) and [its verification record](18-tutorial-validation-and-version-update.md) for the exact scope.

## Writing review

The requested ASD-STE100 skill supplied the writing controls.
The review used its essential rules, source boundary, and final checklist.
The narrative uses descriptions, interface references, procedures, and general explanations.

| Control | Review result |
| --- | --- |
| Stable terminology | Defined note, entity, observation, relation, project, harness, and projection. |
| Technical meaning | Preserved identifiers, field names, time axes, source versions, and interface limits. |
| Direct language | Used short sentences and visible actors in procedures. |
| Paragraph structure | Kept each narrative paragraph on one main topic. |
| Sentence length | A heuristic prose scan found no narrative candidates above 25 words. |
| Procedure form | Reviewed numbered steps for direct commands and clear conditions. |
| Tables and code | Preserved reference fragments and exact technical notation. |
| Source and proposal distinction | Labeled authored cases, proposed systems, and unverified runtime behavior. |
| Dictionary status | Official dictionary verification remains pending. |
| Independent domain review | Human review remains pending. |

The sentence scan is a readability aid. It is not the official ASD-STE100 counting or dictionary procedure.
Generated inventories preserve source descriptions and declarations as reference material.
They did not receive a controlled-dictionary rewrite.

The collection is an **STE-aligned draft**.
It does not claim ASD-STE100 compliance or certification.

## Review guidance

Before implementation, verify the selected tool contract against the running server.
Before publishing a technical specification, obtain domain and dictionary review.
For exact graph results, verify source completeness and snapshot consistency.
