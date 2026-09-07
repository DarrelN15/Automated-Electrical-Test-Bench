from dut import SimulatedDUT
from voltage_test import run_voltage_test


def test_voltage_within_limits_passes():
    dut = SimulatedDUT("PCM-TEST")

    result = run_voltage_test(
        dut,
        "12V",
        11.4,
        12.6
    )

    assert result["result"] == "PASS"
    assert result["measured_value"] == 12.08


def test_voltage_below_limit_fails():
    dut = SimulatedDUT(
        "PCM-TEST",
        fault_mode="LOW_3V3"
    )

    result = run_voltage_test(
        dut,
        "3.3V",
        3.135,
        3.465
    )

    assert result["result"] == "FAIL"
    assert result["measured_value"] == 3.01


def test_voltage_above_limit_fails():
    dut = SimulatedDUT(
        "PCM-TEST",
        fault_mode="HIGH_5V"
    )

    result = run_voltage_test(
        dut,
        "5V",
        4.75,
        5.25
    )

    assert result["result"] == "FAIL"
    assert result["measured_value"] == 5.50