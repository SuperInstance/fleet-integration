"""CLI runner for all fleet integration scenarios."""

import json
from fleet_integration.scenarios import (
    Scenario1_TimeSecureFleet,
    Scenario2_FoldCompressGPU,
    Scenario3_DiscoveryPipeline,
    Scenario4_EisensteinVsPythagorean,
)


SCENARIOS = [
    ("1. Time-Secure Fleet", Scenario1_TimeSecureFleet),
    ("2. Fold-Compress GPU", Scenario2_FoldCompressGPU),
    ("3. Discovery Pipeline", Scenario3_DiscoveryPipeline),
    ("4. Eisenstein vs Pythagorean", Scenario4_EisensteinVsPythagorean),
]


def main():
    print("═" * 60)
    print("  fleet-integration — Prove It Works")
    print("═" * 60)
    print()

    all_results = {}
    for label, cls in SCENARIOS:
        print(f"▶ {label}")
        try:
            result = cls().run()
            all_results[label] = result
            print(f"  ✓ OK — {json.dumps(result, indent=2)[:200]}")
        except Exception as e:
            all_results[label] = {'error': str(e)}
            print(f"  ✗ FAILED — {e}")
        print()

    print("═" * 60)
    passed = sum(1 for v in all_results.values() if 'error' not in v)
    print(f"  {passed}/{len(SCENARIOS)} scenarios passed")
    print("═" * 60)

    return 0 if passed == len(SCENARIOS) else 1


if __name__ == '__main__':
    raise SystemExit(main())
