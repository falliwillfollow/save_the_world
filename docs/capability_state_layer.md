# Capability State Layer

The capability state layer lets CIaC model non-resource civic conditions without pretending they produce water, food, or energy.

Resource simulation still tracks physical flows: source, use, storage, reserve release, reserve refill, curtailment, maintenance, labor, failures, and unmet demand. Capability simulation sits beside it and tracks provisional civic-floor conditions such as privacy, hidden labor, governance legitimacy, anti-capture protection, high-need support, mobility access, legal-finance resilience, maintenance readiness, skill redundancy, social opt-out protection, and graceful degradation.

## Capability Effects

Patterns can optionally declare `capability_effects`:

```yaml
capability_effects:
  governance_anticapture:
    due_process_defined: true
    emergency_power_sunset_defined: true
    capture_risk_delta: -2
    role_backup_coverage_delta: 0.10
```

Effects are additive and provisional. They are collected during compile, applied at simulation start, recorded in a ledger, and exported in runtime bundles.

## Domains

The v0 domains are:

- `dignity_privacy`
- `labor_time`
- `governance_anticapture`
- `care_health`
- `mobility_access`
- `legal_land_finance`
- `maintenance_repair`
- `education_skill`
- `social_cultural`
- `risk_resilience`
- `materials_fabrication`

## Gates

The capability gate returns `pass`, `warn`, or `fail` for selected domains. Unknowns usually warn. Safety-critical missing capability can fail when a module that depends on it is active, such as a governance module without due process or a resilience module without a dependency graph.

## What It Does Not Prove

Capability scores are provisional modeling aids. They do not prove real-world dignity, safety, legal validity, health outcomes, consent, accessibility compliance, resident trust, or anti-capture success. They expose assumptions and blockers for review.

## Adding Effects

Add only effects the pattern can actually represent. Prefer explicit boolean support flags, bounded coverage deltas, count deltas, and risk deltas. Keep professional review, resident consent, and real-world validation outside the simulator authority.
