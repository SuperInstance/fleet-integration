"""Tests for fleet integration scenarios."""

import pytest
from fleet_integration.scenarios import (
    Scenario1_TimeSecureFleet,
    Scenario2_FoldCompressGPU,
    Scenario3_DiscoveryPipeline,
    Scenario4_EisensteinVsPythagorean,
)


class TestScenario1_TimeSecureFleet:
    def setup_method(self):
        self.scenario = Scenario1_TimeSecureFleet()

    def test_runs_without_error(self):
        result = self.scenario.run()
        assert result['scenario'] == 'time_secure_fleet'
        assert result['n_devices'] == 8

    def test_spoofed_device_detected(self):
        """Device 3 is spoofed and must be flagged."""
        result = self.scenario.run()
        spoofed = result['spoofed_detected']
        assert len(spoofed) == 1
        assert spoofed[0]['device'] == 'device_3'
        assert spoofed[0]['honest'] is False

    def test_honest_devices_pass(self):
        """All non-spoofed devices must pass audit."""
        result = self.scenario.run()
        honest = [r for r in result['audit_results'] if r['honest']]
        assert len(honest) == 7

    def test_constraints_striped(self):
        result = self.scenario.run()
        assert result['constraints_striped'] == 7  # 7 constraints → 7 stripes

    def test_spoofed_high_deviation(self):
        result = self.scenario.run()
        spoofed = result['spoofed_detected'][0]
        assert spoofed['deviation_sigma'] > 3  # well beyond 3σ


class TestScenario2_FoldCompressGPU:
    def setup_method(self):
        self.scenario = Scenario2_FoldCompressGPU()

    def test_runs_without_error(self):
        result = self.scenario.run()
        assert result['scenario'] == 'fold_compress_gpu'

    def test_generator_count(self):
        """N=8 → N-1=7 transposition generators."""
        result = self.scenario.run()
        assert result['n_generators'] == 7

    def test_compression_ratio(self):
        """8! = 40320, divided by 7 generators → 5760."""
        result = self.scenario.run()
        assert result['n_states'] == 8
        assert result['full_space_size'] == 40320
        assert result['compression_ratio'] == 40320 / 7

    def test_betti_number(self):
        """Betti₁ = E - V + 1 = 7 - 8 + 1 = 0."""
        result = self.scenario.run()
        assert result['betti1'] == 0


class TestScenario3_DiscoveryPipeline:
    def setup_method(self):
        self.scenario = Scenario3_DiscoveryPipeline()

    def test_runs_without_error(self):
        result = self.scenario.run()
        assert result['scenario'] == 'discovery_pipeline'

    def test_discovery_type(self):
        result = self.scenario.run()
        assert result['discovery_type'] == 'norm_resonance'

    def test_surprise_preserved(self):
        result = self.scenario.run()
        assert abs(result['surprise'] - 0.87) < 1e-9

    def test_flux_opcodes_present(self):
        """Tile must contain at least 2 opcodes (T_PARITY + T_FOLD)."""
        result = self.scenario.run()
        assert result['flux_opcodes'] >= 2

    def test_published(self):
        result = self.scenario.run()
        assert result['published_to'] == 'fleet-discoveries'


class TestScenario4_EisensteinVsPythagorean:
    def setup_method(self):
        self.scenario = Scenario4_EisensteinVsPythagorean()

    def test_runs_without_error(self):
        result = self.scenario.run()
        assert result['scenario'] == 'eisenstein_vs_pythagorean'

    def test_eisenstein_density_advantage(self):
        """402 / 48 ≈ 8.4× density (spec says 6.8× but 402/48=8.375)."""
        result = self.scenario.run()
        density_str = result['density_advantage']
        density_val = float(density_str.replace('×', ''))
        assert density_val > 6.0  # at least 6×

    def test_margin_improvement(self):
        """2.4 / 0.35 ≈ 6.9× margin improvement."""
        result = self.scenario.run()
        margin_str = result['margin_improvement']
        margin_val = float(margin_str.replace('×', ''))
        assert margin_val > 5.0

    def test_direction_counts(self):
        result = self.scenario.run()
        assert result['pythagorean']['directions'] == 48
        assert result['eisenstein']['directions'] == 402

    def test_symmetries(self):
        result = self.scenario.run()
        assert 'D4' in result['pythagorean']['symmetry']
        assert 'D6' in result['eisenstein']['symmetry']


class TestAllScenarios:
    """Meta-test: all scenarios run cleanly in sequence."""

    def test_all_scenarios_run(self):
        scenarios = [
            Scenario1_TimeSecureFleet(),
            Scenario2_FoldCompressGPU(),
            Scenario3_DiscoveryPipeline(),
            Scenario4_EisensteinVsPythagorean(),
        ]
        results = []
        for s in scenarios:
            r = s.run()
            results.append(r)
            assert 'scenario' in r

        assert len(results) == 4
        names = [r['scenario'] for r in results]
        assert 'time_secure_fleet' in names
        assert 'fold_compress_gpu' in names
        assert 'discovery_pipeline' in names
        assert 'eisenstein_vs_pythagorean' in names
