from dut import SimulatedDUT


def test_nominal_dut_voltages():
    dut = SimulatedDUT("PCM-TEST")

    assert dut.measure_voltage("12V") == 12.08
    assert dut.measure_voltage("5V") == 5.02
    assert dut.measure_voltage("3.3V") == 3.31


def test_low_3v3_fault():
    dut = SimulatedDUT(
        "PCM-TEST",
        fault_mode="LOW_3V3"
    )

    assert dut.measure_voltage("3.3V") == 3.01


def test_high_5v_fault():
    dut = SimulatedDUT(
        "PCM-TEST",
        fault_mode="HIGH_5V"
    )

    assert dut.measure_voltage("5V") == 5.50


def test_low_12v_fault():
    dut = SimulatedDUT(
        "PCM-TEST",
        fault_mode="LOW_12V"
    )

    assert dut.measure_voltage("12V") == 10.80