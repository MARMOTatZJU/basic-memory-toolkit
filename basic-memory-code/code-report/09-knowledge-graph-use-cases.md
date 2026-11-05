# Knowledge graph usage cases

[Collection index](README.md)

This catalog contains **96 distinct graph-focused cases**.
All cases are authored proposals grounded in the inspected graph primitives.
They are not reports of deployed customer systems.

## Capability labels

| Label | Meaning |
| --- | --- |
| N | Current note, relation, search, and context tools support an agent-led workflow. No new core graph endpoint is essential. |
| A | The case needs added deterministic analysis, a graph snapshot, or a policy engine for a reliable complete answer. |
| I | The case needs an external connector or source preparation beyond the current note corpus. |

An N case can still need careful note design and human review.
No label means that the system has an automatic truth engine.

## Shared graph contract

A graph node is an indexed entity. A named edge comes from its source note.
`A -> depends_on -> B` means that A depends on B.
A context read can follow either direction, but the edge statement keeps its direction.

The shapes below are proposed domain vocabularies.
Basic Memory does not reserve labels such as `supports`, `verifies`, or `blocked_by`.
Use one label per concept in a project.

Evidence: [src/basic_memory/markdown/plugins.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/plugins.py), [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py), and [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py).

## Base prompt for graph work

> Use project `<project>`. Find the seed notes and read their content.
> Preserve relation labels and direction. Cite each source path used in the answer.
> Treat a link as an authored statement, not proof. Mark inference and missing evidence.
> Report depth limits, result limits, unresolved targets, and time filters.
> Do not claim completeness from a bounded context response.

For A cases, add this instruction:

> Use a graph snapshot and deterministic analysis for complete results. Record the snapshot identity and algorithm.

## Why graph structure adds value

A path can preserve an explanation across several notes.
An anti-join can expose missing support, ownership, or verification.
A reverse traversal can reveal decisions affected by changed evidence.
A typed join can compare results only when the dataset and method match.

These operations answer relationship questions that similarity ranking alone cannot answer.
The current context API offers bounded neighborhood retrieval.
An exact analysis service must implement the remaining algorithms.


## Engineering requirements and decisions

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G001 | **Requirement coverage**. `Requirement <- satisfies - Design <- implements - Change` | For requirement R, show linked designs, changes, and verification notes. Report each missing link. | N | A complete coverage audit needs explicit snapshot analysis. |
| G002 | **Decision rationale**. `Decision -> justified_by -> Experiment` | Explain why we chose this design. Read the linked experiments and rejected alternatives. | N | Read evidence content before accepting the rationale. |
| G003 | **Decision replacement**. `New Decision -> supersedes -> Old Decision` | Trace which decision replaced the old policy. Show unresolved branches in the replacement chain. | A | Compute chain order and detect forks. |
| G004 | **Alternative comparison**. `Decision -> considers -> Alternative -> has_tradeoff -> Constraint` | Compare the recorded alternatives against their linked constraints. Do not invent an unrecorded option. | N | Tradeoff labels are a local vocabulary. |
| G005 | **Test traceability**. `Test -> verifies -> Requirement` | List requirements without a linked verification note. Separate missing tests from tests without recorded results. | A | Use a directional anti-join and result-state checks. |
| G006 | **Change review context**. `Change -> modifies -> Component <- constrained_by - Decision` | Read constraints linked to these changed components. Prepare a review checklist with evidence paths. | N | A Git adapter must supply the changed components. |
| G007 | **Exception management**. `Exception -> waives -> Requirement; Exception -> approved_by -> Review` | Show active exceptions for this requirement. Include approving reviews and expiry evidence. | N | Use metadata or authored time to define active. |
| G008 | **Verification provenance**. `Result -> produced_by -> Run -> uses -> Configuration` | Trace this verification claim to its run, configuration, and recorded result. Flag missing artifacts. | N | External artifacts need stable references. |

## Architecture and dependency analysis

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G009 | **Change impact**. `Component A -> depends_on -> Component B` | If component B changes, find all recorded dependents. Preserve edge direction and show the search boundary. | A | Compute reverse transitive closure. |
| G010 | **Dependency cycles**. `Service -> depends_on -> Service` | Find dependency cycles among these services. Return a minimal example path for each cycle. | A | Use strongly connected components and cycle extraction. |
| G011 | **Service ownership**. `Service -> owned_by -> Team` | Find services without an owner relation. Show conflicting owner assignments separately. | A | Apply cardinality rules over the explicit graph. |
| G012 | **Shared bottleneck**. `Service -> depends_on -> Shared Resource` | Find shared resources with many dependent services. Explain each dependency path. | A | Degree or centrality is a prioritization signal only. |
| G013 | **API migration radius**. `Consumer -> calls -> API; Replacement -> replaces -> API` | List consumers of the retiring API. Group them by migration task and replacement readiness. | A | Add code-derived or maintained calls edges. |
| G014 | **Design consistency**. `Component -> uses_pattern -> Pattern -> constrained_by -> Rule` | Compare the patterns used by these components. Identify recorded conflicts with shared design rules. | N | Semantic conflict assessment needs source review. |
| G015 | **System boundary map**. `Component -> exchanges_data_with -> Component` | Build a boundary map from these interface notes. Preserve direction and data classifications. | N | The notes must include interface evidence. |
| G016 | **Failure propagation**. `Failure Mode -> affects -> Component; Component -> depends_on -> Component` | Trace recorded failure propagation paths from this component. Label uncertain links explicitly. | A | Graph connectivity does not prove physical causation. |

## Research claims and evidence

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G017 | **Claim support**. `Claim <- supports - Study` | Show the evidence linked to this claim. Separate direct measurements from interpretations. | N | Create claim notes when claims need independent identity. |
| G018 | **Conflicting findings**. `Study -> contradicts -> Claim <- supports - Study` | Compare supporting and conflicting evidence for this claim. State differences in method and scope. | N | Do not collapse disagreement into a vote count. |
| G019 | **Method transfer**. `Method -> used_by -> Experiment -> tests -> Hypothesis` | Find experiments that used this method for related hypotheses. Explain the transfer limits. | N | Relation direction must follow the chosen vocabulary. |
| G020 | **Research lineage**. `Method -> extends -> Method -> inspired_by -> Work` | Trace the recorded development of this method. Cite each intermediate source. | N | External citation retrieval needs a connector or prepared notes. |
| G021 | **Evidence gaps**. `Claim -> requires_evidence -> Evidence Need` | Find important claims without a resolved support path. Propose the next evidence collection step. | A | Check unresolved targets outside the resolved export. |
| G022 | **Replication targets**. `Study -> reports -> Result <- replicates - Study` | Find results with no linked replication. Rank candidates by recorded importance and uncertainty. | A | Ranking needs an explicit policy. |
| G023 | **Literature bridges**. `Paper -> studies -> Topic; Paper -> uses -> Method` | Find papers that connect these two topics through a shared method. Show both evidence paths. | A | Use a typed join or bounded path search. |
| G024 | **Dataset comparability**. `Result -> measured_on -> Dataset -> uses_protocol -> Protocol` | Compare these results only where datasets and protocols match. List non-comparable results separately. | A | Use exact identities and protocol metadata. |

## Organizations and project coordination

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G025 | **Commitment provenance**. `Commitment -> made_in -> Meeting; Commitment -> assigned_to -> Person` | Show commitments from this meeting, their owners, and linked delivery evidence. | N | Capture only explicit commitments. |
| G026 | **Task blockers**. `Task -> blocked_by -> Task` | Find tasks that block this objective. Separate direct blockers from indirect blockers. | A | Compute typed dependency closure. |
| G027 | **Handoff context**. `Checkpoint -> continues -> Checkpoint; Checkpoint -> advances -> Task` | Reconstruct this task handoff. Show the latest checkpoint and its unresolved decisions. | N | Verify the selected checkpoint against current state. |
| G028 | **Expert discovery**. `Person -> worked_on -> Project -> uses -> Technology` | Find people with recorded work on this technology. Show the supporting project notes. | N | This is evidence of recorded work, not a personnel rating. |
| G029 | **Responsibility gaps**. `Deliverable -> accountable_to -> Role -> filled_by -> Person` | Find deliverables without a complete responsibility path. Keep unfilled roles visible. | A | Use a two-hop completeness rule. |
| G030 | **Cross-team duplication**. `Project -> pursues -> Objective` | Find active projects linked to the same objective. Compare overlap before suggesting consolidation. | A | Shared objectives do not prove duplicated effort. |
| G031 | **Decision consultation**. `Decision -> affects -> Team; Review -> consulted -> Team` | Show affected teams without a linked consultation record. Do not infer consent from missing objections. | A | Requires explicit review and team records. |
| G032 | **Institutional history**. `Milestone -> enabled_by -> Decision -> informed_by -> Incident` | Explain how this milestone emerged from prior decisions and incidents. Cite the recorded paths. | N | Keep chronology separate from causal interpretation. |

## Product discovery and customer evidence

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G033 | **Feature evidence**. `Feature -> addresses -> Need <- reported_in - Interview` | Explain the evidence for this feature. Preserve interview context and contrary observations. | N | Prepared customer material must be authorized. |
| G034 | **Roadmap traceability**. `Initiative -> delivers -> Feature -> supports -> Objective` | Trace each roadmap initiative to its stated objective. Mark initiatives without a complete path. | A | Use directional coverage checks. |
| G035 | **Persona mismatch**. `Feature -> targets -> Persona; Interview -> represents -> Persona` | Find features whose evidence comes from a different persona. Explain the mismatch. | A | Persona labels need reviewed definitions. |
| G036 | **Experiment learning**. `Experiment -> tests -> Assumption; Result -> changes -> Decision` | Show which decisions changed after this experiment. Cite the recorded result and decision revisions. | N | An edge alone does not prove a change occurred. |
| G037 | **Feedback clusters**. `Feedback -> concerns -> Capability` | Group feedback through shared capabilities. Keep source counts separate from independent customer counts. | A | Deduplicate source and customer identities. |
| G038 | **Adoption barriers**. `Customer Need -> blocked_by -> Constraint; Feature -> removes -> Constraint` | Trace the constraints that block this need. Identify recorded features that address those constraints. | N | Avoid causal claims without evidence. |
| G039 | **Release explanation**. `Release -> includes -> Change -> addresses -> Need` | Explain this release through the customer needs its changes address. Cite the paths. | N | Prepared release and change records are required. |
| G040 | **Deprecation impact**. `Customer Workflow -> uses -> Capability; Capability -> retired_by -> Decision` | List recorded workflows affected by this retirement. Link each workflow to its owner and migration evidence. | A | Needs a complete and current workflow inventory. |

## Data and machine learning lineage

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G041 | **Dataset lineage**. `Dataset -> derived_from -> Dataset; Transform -> produces -> Dataset` | Trace this dataset to its source versions and transformation notes. Report every missing version. | N | Version identity must be explicit in notes. |
| G042 | **Model provenance**. `Model -> trained_on -> Dataset; Model -> uses -> Configuration` | Explain the provenance of this model result. Link the training data and configuration evidence. | N | Use an artifact store for model files. |
| G043 | **Evaluation leakage**. `Training Set -> contains -> Record; Evaluation Set -> contains -> Record` | Find shared records between these training and evaluation sets. Show exact identity matches. | A | Large record-level comparison belongs in a data engine. |
| G044 | **Metric definitions**. `Dashboard -> reports -> Metric -> computed_from -> Dataset` | Trace this dashboard metric to its definition and data sources. Flag competing definitions. | N | Live metric values require an external data source. |
| G045 | **Schema change impact**. `Column -> belongs_to -> Table; Pipeline -> reads -> Column` | Find pipelines affected by this column change. Show the supporting lineage paths. | A | A catalog adapter must maintain column-level edges. |
| G046 | **Reproducible benchmark**. `Result -> produced_by -> Run -> uses -> Environment` | Find runs that support this benchmark comparison. Exclude runs with incompatible environments. | A | Use explicit comparison rules. |
| G047 | **Data ownership**. `Dataset -> owned_by -> Team; Dataset -> subject_to -> Policy` | Show the owner and policy context for this dataset. Identify missing links for review. | N | This supplies context, not an authorization decision. |
| G048 | **Failure cohort analysis**. `Failure -> occurs_in -> Slice; Slice -> tests -> Capability` | Group model failures by linked slices and capabilities. Preserve example evidence. | A | Statistical analysis needs an external evaluator. |

## Operations, incidents, and security knowledge

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G049 | **Incident recurrence**. `Incident -> caused_by -> Failure Mode; Runbook -> mitigates -> Failure Mode` | Find similar recorded failure modes and their runbooks. Show evidence before suggesting a recovery step. | N | The operator must verify current system state. |
| G050 | **Mitigation coverage**. `Mitigation -> addresses -> Risk` | List risks without a linked mitigation. Separate absent mitigations from unverified mitigations. | A | Requires a reviewed risk inventory. |
| G051 | **Control evidence**. `Control -> supported_by -> Evidence; Evidence -> produced_by -> Review` | Trace this control to its evidence and review records. Mark stale evidence. | N | This is an evidence view, not a compliance determination. |
| G052 | **Alert context**. `Alert -> monitors -> Service; Service -> has_runbook -> Runbook` | Build a context packet for this alert from service notes and verified runbooks. | I | Needs an alert connector and service mapping. |
| G053 | **Vulnerability impact notes**. `Component -> uses -> Dependency; Finding -> affects -> Dependency` | Find recorded components linked to this affected dependency. Preserve version constraints from the supplied finding. | I+A | Needs current findings and an accurate dependency adapter. |
| G054 | **Recovery dependency order**. `Recovery Task -> requires -> Recovery Task` | Order the recorded recovery tasks by prerequisites. Stop if the dependency graph contains a cycle. | A | Use topological sorting over reviewed prerequisites. |
| G055 | **Configuration rationale**. `Setting -> chosen_by -> Decision -> informed_by -> Incident` | Explain why this setting exists. Read the linked incident and decision notes. | N | Verify the live value separately. |
| G056 | **Operational ownership transitions**. `Service -> handed_to -> Team; Handoff -> documents -> Service` | Find services whose ownership change lacks a handoff note. Show the missing evidence. | A | Time and ownership conventions need explicit rules. |

## Learning and curriculum graphs

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G057 | **Prerequisite planning**. `Topic -> requires -> Topic` | Build a study order for these topics from explicit prerequisite links. Report cycles and missing topics. | A | Use topological sorting and prerequisite closure. |
| G058 | **Concept explanation**. `Concept -> illustrated_by -> Example; Concept -> contrasts_with -> Concept` | Explain this concept through its examples and contrasts. Cite the supporting notes. | N | Examples must be reviewed for correctness. |
| G059 | **Misconception repair**. `Misconception -> corrected_by -> Explanation -> supported_by -> Example` | Find the recorded explanation for this misconception. Show the examples that support the correction. | N | Do not infer a learner diagnosis. |
| G060 | **Exercise selection**. `Exercise -> practices -> Skill; Skill -> requires -> Skill` | Select exercises for the stated skill gaps. Explain the prerequisite path for each choice. | A | Needs a selection rule and explicit learner evidence. |
| G061 | **Interdisciplinary study**. `Concept -> applies_to -> Domain` | Find concepts that connect these domains. Explain the recorded applications without inventing equivalence. | N | Review analogy quality. |
| G062 | **Course evidence coverage**. `Lesson -> teaches -> Objective; Assessment -> checks -> Objective` | Find objectives taught without assessment, and assessments without a teaching path. | A | Use directional anti-joins. |
| G063 | **Reading sequence**. `Book -> introduces -> Concept; Chapter -> requires -> Concept` | Suggest a reading sequence from introduced and required concepts. Mark optional branches. | A | A weighted plan needs an external planner. |
| G064 | **Knowledge decay review**. `Review Event -> checks -> Concept; Concept -> required_by -> Skill` | Prioritize concepts for review from recorded review history and dependent skills. Explain the priority rule. | A | Scheduling and memory models remain external. |

## Personal knowledge and practical projects

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G065 | **Home project decisions**. `Room -> uses -> Material; Decision -> selects -> Material` | Explain the recorded material choices for this room. Link each choice to constraints and source records. | N | User records supply the evidence. |
| G066 | **Equipment compatibility**. `Device -> requires -> Interface; Accessory -> provides -> Interface` | Compare the recorded compatibility requirements for these devices. Mark unverified matches. | A | Use exact specifications supplied by the user. |
| G067 | **Hobby trial analysis**. `Trial -> uses -> Technique; Trial -> produces -> Result` | Compare the outcomes of these techniques using recorded trials. Keep confounding changes visible. | N | Connectivity is not experimental control. |
| G068 | **Reading themes**. `Book -> explores -> Theme <- explored_by - Essay` | Find themes shared by these works. Cite passages recorded in the notes. | N | Keep interpretation separate from quotation. |
| G069 | **Personal project blockers**. `Goal -> requires -> Milestone; Milestone -> blocked_by -> Constraint` | Show the recorded blockers for this goal. Propose a next action for each unresolved constraint. | N | The user remains the source of personal priorities. |
| G070 | **Resource reuse**. `Project -> needs -> Resource; Resource -> available_at -> Location` | Find reusable resources for this project from the inventory notes. Mark uncertain availability. | N | Live availability requires updated records. |
| G071 | **Historical family archive**. `Person -> appears_in -> Document; Event -> occurred_at -> Place` | Connect the supplied archive records by person, event, and place. Preserve uncertain identity matches. | N | Identity resolution needs human review. |
| G072 | **Travel constraint map**. `Plan -> includes -> Activity; Activity -> requires -> Condition` | Find activities whose recorded prerequisites conflict with this plan. Preserve the source dates. | A | Current schedules require fresh sources. |

## Creative, literary, and historical analysis

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G073 | **Character relationships**. `Character -> allied_with -> Character; Event -> changes -> Relationship` | Trace how the supplied text changes this relationship. Cite chapters and distinguish interpretation. | N | Model relationship changes as notes when they need time. |
| G074 | **Plot dependencies**. `Event -> enabled_by -> Event` | Find events that make this plot turn possible. Mark inferred causal links for review. | A | Narrative causality requires interpretation. |
| G075 | **World-building consistency**. `Location -> governed_by -> Rule; Event -> occurs_in -> Location` | Find events that conflict with recorded world rules. Show both sources before proposing a revision. | N | Rules and exceptions need explicit note types. |
| G076 | **Symbol development**. `Passage -> uses -> Symbol; Symbol -> associated_with -> Theme` | Trace this symbol across the supplied chapters. Compare changes in its recorded meaning. | N | Do not substitute repeated keywords for interpretation. |
| G077 | **Historical source comparison**. `Source -> asserts -> Claim; Source -> produced_by -> Actor` | Compare source claims about this event. Preserve author perspective and source uncertainty. | N | This is source analysis, not automatic historical truth. |
| G078 | **Argument structure**. `Premise -> supports -> Conclusion; Objection -> challenges -> Premise` | Map the recorded argument and its objections. Identify unsupported premises. | A | Formal validity needs a separate logic representation. |
| G079 | **Creative reuse paths**. `Idea -> inspired_by -> Work; Draft -> develops -> Idea` | Find earlier ideas related to this draft. Show the recorded inspiration paths. | N | Preserve attribution. |
| G080 | **Timeline consistency**. `Event -> precedes -> Event; Character -> participates_in -> Event` | Find contradictory event orders in this story. Return the smallest conflicting chain. | A | Use partial-order analysis. |

## Graph curation and knowledge quality

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G081 | **Orphan integration**. `Note without relations -> candidate Topic` | Review isolated notes and propose useful typed links. Keep suggestions separate from accepted relations. | N | Use orphan data and semantic candidates. |
| G082 | **Duplicate identity review**. `Alias -> refers_to -> Entity` | Find possible duplicate entities and aliases. Show conflicting identities before proposing a merge. | A | Semantic similarity creates candidates, not merge authority. |
| G083 | **Broken reference repair**. `Source -> unresolved target name` | List unresolved targets and their source notes. Suggest exact repairs without silently changing meaning. | N | The resolved graph export is insufficient. |
| G084 | **Relation vocabulary drift**. `Source -> depends_on/needs/requires -> Target` | Find relation labels that may express the same concept. Propose a controlled vocabulary and migration map. | A | Human review must confirm semantic equivalence. |
| G085 | **Unsupported relation review**. `Relation Claim -> supported_by -> Evidence` | Find important relation claims without evidence notes. Prepare a review queue. | A | Reify important edges as claim notes. |
| G086 | **Hub overload**. `Hub -> links_to -> Many Notes` | Find hub notes whose generic links hide useful structure. Propose smaller topic hubs and typed links. | A | Use degree and sampled content review. |
| G087 | **Graph bridge candidates**. `Topic A -> shared Entity <- Topic B` | Find weakly connected topic groups and explain candidate bridge notes. Mark new links as proposals. | A | Community analysis requires an external algorithm. |
| G088 | **Deletion impact review**. `Source -> points_to -> Candidate Note` | Before archiving this note, show inbound references and unresolved-target risks. Preserve source meaning. | A | Archiving and deletion have different effects. |

## Temporal decisions, scenarios, and planning

| ID | Case and graph shape | Example prompt | Label | Added logic or limit |
| --- | --- | --- | --- | --- |
| G089 | **Policy applicability**. `Observation -> effective interval; Decision -> applies_to -> Component` | Find the recorded policy applicable on this date. Exclude undated assertions and show the source qualifier. | N | Use valid-time search before graph expansion. |
| G090 | **Policy overlap**. `Policy Claim -> applies_to -> Scope; Claim -> valid interval` | Find overlapping contradictory policy claims for the same scope. Present the exact intervals and evidence. | A | Valid-time retrieval alone does not detect contradiction. |
| G091 | **Decision review trigger**. `Assumption -> supports -> Decision; Evidence -> challenges -> Assumption` | Show decisions that depend on the challenged assumption. Prepare a review list without replacing decisions. | A | Compute typed reverse closure. |
| G092 | **Scenario branch**. `Scenario -> assumes -> Assumption; Plan -> valid_under -> Scenario` | Compare plans under these stated assumptions. Keep scenario conclusions separate from current facts. | N | Use explicit scenario metadata or separate projects. |
| G093 | **Plan prerequisites**. `Task -> requires -> Evidence; Task -> depends_on -> Task` | Identify the next tasks whose recorded prerequisites are satisfied. Explain every excluded task. | A | Readiness needs deterministic rules and current state. |
| G094 | **Decision experiment value**. `Unknown -> affects -> Decision; Experiment -> reduces -> Unknown` | Rank candidate experiments by the decisions they can inform. State the ranking assumptions. | A | Information-value scoring is new planner logic. |
| G095 | **Knowledge freshness routing**. `Fact -> reviewed_by -> Review; Fact -> supports -> Decision` | Find important decisions supported by facts with expired reviews. Produce a source-backed refresh queue. | A | Freshness is a policy, not an automatic truth signal. |
| G096 | **Graph-aware memory budget**. `Task -> needs -> Topic -> supported_by -> Evidence` | Build a small context packet for this task. Preserve evidence paths and report omitted branches. | A | Use a budgeted selector and explicit coverage report. |

## Recommended first prototypes

| Prototype | Why it is a useful first step | Acceptance question |
| --- | --- | --- |
| Decision rationale explorer | Small graphs can still preserve valuable evidence paths. | Can a reader find the actual reason without reading every session note? |
| Graph quality inspector | It improves the corpus needed by every later graph system. | Does it distinguish isolation, unresolved links, aliases, and duplicate identities? |
| Requirement verification map | Coverage has a clear testable meaning. | Does the result correctly identify every missing required path? |
| Research claim explorer | It separates source evidence from agent interpretation. | Can every factual claim lead back to a source note or document page? |
| Dependency impact analyzer | It demonstrates the benefit of exact directed algorithms. | Does it return the known reverse closure without unrelated neighbors? |
| Graph-aware resume assistant | It extends existing host continuity packages. | Does the resumed agent recover constraints and evidence under a fixed context budget? |

See [worked examples](10-knowledge-graph-worked-examples.md) for concrete notes and queries.
See [harness designs](12-harness-systems.md) for lifecycle and execution systems built around these cases.

## Cases that need more than graph storage

- A scheduler must trigger recurring reviews.
- A connector must obtain live code, incidents, customer feedback, or catalog data.
- A graph engine must compute cycles, shortest paths, closure, joins, or community structure.
- A review process must accept inferred relations and identity merges.
- A policy engine must determine permission, workflow readiness, or evidence sufficiency.
- A temporal store must preserve historic states if the application needs full graph snapshots through time.

Basic Memory can store the human-readable knowledge and many results of these operations.
The proposed system must supply the additional mechanisms.

Evidence for current boundaries: [src/basic_memory/api/v2/routers/knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/knowledge_router.py#L188), [src/basic_memory/picoschema/validator.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/picoschema/validator.py), and [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md).
