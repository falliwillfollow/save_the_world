# CIaC Research Loop Materialization

CIaC can now move a research-loop result into a draft model artifact without manual file editing.

## Flow

1. The world UI runs `POST /api/research-loop`.
2. The viewer server sends the discovery report to the configured n8n webhook.
3. n8n retrieves local CIaC context, calls Ollama, and returns candidate interventions.
4. CIaC writes:
   - `candidate_interventions/*.json`
   - `patch_proposals/*.json`
   - `examples/discovery/*viewer_research.run.json`
5. The UI `Draft` button calls `POST /api/materialize-patch`.
6. CIaC turns the selected `PatchProposal` into a provisional `CivicPattern` under the patch target path, such as `patterns/care_health/*.yaml`, plus a `PatchMaterializationReport`.
7. The UI `Test` button calls `POST /api/analyze-materialized-patch`.
8. CIaC compares the current generated model against a candidate model with the draft pattern selected, then writes a `PatchImpactReport`.
9. The UI enables `Promote` only when the impact report shows modeled capability improvement without survival-resource or excessive labor regression.

## Guardrails

Materialization does not auto-select the new pattern into an active site profile. The generated pattern remains:

- `status: draft`
- `provisional: true`
- explicitly provisional for legal, health, labor, governance, and any domain-specific risks
- dependent on local health, privacy, consent, professional-boundary, and safety review

This keeps discovery useful without pretending the model has certified real-world safety or legality.

## CLI

```powershell
py -3.10 -m ciac materialize-patch patch_proposals\patch_care_health_resident_controlled_medication_continuity_kit_v1.json --overwrite --output examples\discovery\patch_care_health_resident_controlled_medication_continuity_kit_v1.materialization.json
```

If `--candidate` is omitted, CIaC loads `candidate_interventions/<source_candidate_id>.json`.

## Promotion Criteria

Before adding the new pattern id to a site profile, run at least:

- schema validation for the materialized pattern and report
- compile with the target site profile after external dependencies are represented
- normal-year simulation
- relevant stress scenarios from the patch proposal
- labor-burden comparison to ensure work was not shifted into hidden resident burden

The viewer promotion action updates generated model artifacts, not source truth:

- `examples/generated/micro_commons_plan.json`
- `examples/generated/micro_commons_simulation.json`
- `examples/generated/micro_commons_runtime_bundle.json`
- `examples/world_manifests/civic_floor_80_v0.world.json`

Source-profile promotion should remain a separate governance/review step once local evidence dependencies are actually resolved.
