def run_voltage_test(dut, rail, minimum, maximum):
    measured_voltage = dut.measure_voltage(rail)

    passed = minimum <= measured_voltage <= maximum

    return {
        "test_name": f"{rail} Rail Voltage",
        "measured_value": measured_voltage,
        "minimum": minimum,
        "maximum": maximum,
        "result": "PASS" if passed else "FAIL"
    }