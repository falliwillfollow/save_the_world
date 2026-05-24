# Candidate Interventions

This directory is the default output target for n8n/Ollama discovery candidates.

Artifacts must use kind `DiscoveryCandidateIntervention` and validate with:

```powershell
py -3.10 -m ciac validate candidate_interventions
```

Generated candidates should remain provisional until CIaC simulation/comparison artifacts show that they reduce a warning without introducing hidden labor, survival-critical unmet demand, privacy regression, accessibility regression, public-health ambiguity, or governance capture risk.
