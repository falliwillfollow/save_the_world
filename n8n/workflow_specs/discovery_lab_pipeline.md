# Discovery Lab Pipeline

This workflow turns CIaC warnings into structured intervention candidates using local RAG and Ollama. n8n orchestrates the loop; CIaC validates artifacts and remains the source of truth.

## Trigger

Manual Trigger or Webhook.

## Inputs

```yaml
world_manifest_path: examples/world_manifests/civic_floor_80_v0.world.json
runtime_bundle_path: examples/generated/micro_commons_runtime_bundle.json
focus: all|care_health|governance_anticapture|labor_time|mobility_access|water_public_health|risk_resilience
discovery_output_path: examples/discovery/civic_floor_80_discovery_loop_v0.discovery.json
candidate_output_dir: candidate_interventions
```

## Workflow

```text
Manual Trigger / Webhook
  -> Execute Command: py -3.10 -m ciac discovery-loop {{$json.world_manifest_path}} --runtime {{$json.runtime_bundle_path}} --focus {{$json.focus}} --output {{$json.discovery_output_path}}
  -> Read DiscoveryLoopReport
  -> Split findings
  -> For each finding:
       -> Run retrieval_plan query against local vector store
       -> Build candidate-generation prompt from finding + retrieved context + evaluation_contract
       -> Ollama Chat Model generates 2-4 DiscoveryCandidateIntervention JSON objects
       -> Code node parses/repairs/splits JSON
       -> Write each candidate to candidate_interventions/<candidate_id>.json
  -> Execute Command: py -3.10 -m ciac validate candidate_interventions
  -> Execute simulation/comparison commands for simulation-ready candidates
  -> Write comparison artifacts to examples/discovery
  -> Notify user with ranked candidates, rejected candidates, and next missing assumptions
```

## RAG Query Inputs

Each `DiscoveryLoopReport.retrieval_plan[]` item contains:

```yaml
id:
domain:
query:
required_context:
```

The retriever should return snippets with:

```yaml
source_id:
path:
heading:
content:
confidence:
```

## Ollama Output Contract

The Ollama node must return JSON only:

```yaml
kind: DiscoveryCandidateIntervention
version: v0
id:
source_loop_id:
focus_domain:
title:
hypothesis:
intervention_type:
target_objects:
module_refs:
assumptions:
expected_effects:
risk_tradeoffs:
simulation_hooks:
rag_context:
status: generated
provisional: true
```

Invalid outputs should route to a repair branch once, then to a rejected-artifact branch if still invalid.

## CIaC Commands

Start the host bridge when running n8n in Docker:

```powershell
py -3.10 -m ciac discovery-bridge --host 0.0.0.0 --port 8791 --repo-root D:\Projects\CIaC
```

Generate discovery loop:

```powershell
py -3.10 -m ciac discovery-loop examples/world_manifests/civic_floor_80_v0.world.json --runtime examples/generated/micro_commons_runtime_bundle.json --focus all --output examples/discovery/civic_floor_80_discovery_loop_v0.discovery.json
```

Validate generated candidates:

```powershell
py -3.10 -m ciac validate candidate_interventions
```

Validate discovery artifacts:

```powershell
py -3.10 -m ciac validate examples/discovery
```

## Failure Branches

- CIaC validation fails: preserve invalid artifact under `candidate_interventions/rejected/` and notify.
- RAG returns no context: generate a `research_task` candidate instead of an operational candidate.
- Ollama returns prose-only response: retry once with the schema and JSON-only instruction.
- Candidate introduces hidden labor or survival-critical regression: reject and keep comparison artifact.

## Outputs

```yaml
discovery_loop_report:
candidate_interventions:
validation_status:
simulation_comparisons:
ranked_recommendations:
rejected_candidates:
missing_assumptions:
```

## Notes

- n8n does not promote interventions.
- Ollama does not certify safety or correctness.
- RAG context must be recorded in `rag_context.source_ids`.
- All promoted candidates must remain traceable to `source_loop_id`.
