"""Graceful mock implementations for fleet repos not available at runtime."""

import math

# ── physics_clock ──────────────────────────────────────────────

class ThermalClock:
    def read_ns(self):
        return 50000

class SiliconClock:
    def read_ns(self):
        return 49900

class PhysicsClock:
    def __init__(self, clocks=None):
        self.clocks = clocks or []

    def consensus_ns(self):
        if not self.clocks:
            return 50000
        return sum(c.read_ns() for c in self.clocks) // len(self.clocks)


# ── fleet_raid5 ────────────────────────────────────────────────

class ConstraintStriper:
    def __init__(self, n_devices=8):
        self.n_devices = n_devices

    def stripe(self, constraints):
        stripes = []
        for i, c in enumerate(constraints):
            stripes.append({
                'constraint': c,
                'device': i % self.n_devices,
                'parity': sum(range(i, i + self.n_devices)) % 256,
            })
        return stripes

class FleetSecurity:
    def audit(self, devices):
        return [{'device': d['device_id'], 'secure': True} for d in devices]


# ── temporal_flux ──────────────────────────────────────────────

class _Opcode:
    def __init__(self, name, code):
        self.name = name
        self.code = code

T_PARITY = _Opcode('T_PARITY', 0x01)
T_FOLD = _Opcode('T_FOLD', 0x02)


# ── fold_compression ──────────────────────────────────────────

class PermutationGenerator:
    def __init__(self, n):
        self.n = n
        self.generators = [(i, i + 1) for i in range(n - 1)]

    def evaluate(self, states, constraints):
        results = []
        current = list(states)
        for i, (a, b) in enumerate(self.generators):
            current[a], current[b] = current[b], current[a]
            results.append({
                'generator': (a, b),
                'state': list(current),
                'satisfied': constraints[a] if a < len(constraints) else 1,
            })
        return results


# ── insight_cfp_bridge ────────────────────────────────────────

class Discovery:
    def __init__(self, type, parameters, surprise, confidence, frontier_size, experiment, iteration):
        self.type = type
        self.parameters = parameters
        self.surprise = surprise
        self.confidence = confidence
        self.frontier_size = frontier_size
        self.experiment = experiment
        self.iteration = iteration

class CfpTile:
    def __init__(self, discovery_type, surprise_score, constraints, flux_opcodes):
        self.discovery_type = discovery_type
        self.surprise_score = surprise_score
        self.constraints = constraints
        self.flux_opcodes = flux_opcodes

class InsightCfpBridge:
    def encode_discovery(self, discovery):
        constraints = [
            {'type': 'norm_resonance', 'params': discovery.parameters},
            {'type': 'temporal_parity', 'opcode': 'T_PARITY'},
            {'type': 'fold_verify', 'opcode': 'T_FOLD'},
        ]
        return CfpTile(
            discovery_type=discovery.type,
            surprise_score=discovery.surprise,
            constraints=constraints,
            flux_opcodes=['T_PARITY', 'T_FOLD'],
        )
