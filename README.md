# fleet-integration — Prove It Works


## Meta

**Domain:** agent-coordination
**Depends on:** —
**Depended by:** —
**Implements:** Integration tests and working examples that compose multiple fleet repos togethe...
**Related:** —


Four integration scenarios that compose multiple fleet repos into
working systems. Each scenario demonstrates a real use case.

## Scenarios

1. **Time-Secure Fleet** — physics-clock + fleet-raid5 + temporal-flux
   8 devices, one spoofed. Detected in 500ms. No crypto.

2. **Fold-Compress GPU** — fold-compression + physics-clock
   8! = 40320 states compressed to 7 generators.
   GPU evaluates all in one kernel. Timing IS verification.

3. **Discovery Pipeline** — insight-cfp-bridge + temporal-flux
   Insight engine discovers norm resonance → auto-encodes as FLUX tile
   → publishes to PLATO → fleet verifies in seconds.

4. **Eisenstein vs Pythagorean** — snap-lut + snap-lut-eisenstein
   Side-by-side: 48 vs 402 directions. 2.4° vs 0.35° margin.
   Same BRAM. 8.4× density advantage confirmed.

## Run

```bash
python -m fleet_integration.run_all
```

## Test

```bash
pytest tests/ -v
```

## Composable With

Everything. This is the integration proof.

## License

Apache 2.0
