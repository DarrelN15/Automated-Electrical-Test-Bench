import csv
from pathlib import Path

from dut import SimulatedDUT
from voltage_test import run_voltage_test

dut = SimulatedDUT("PCM-0001")

test_limits = [
    ("12V", 11.4, 12.6),
    ("5V", 4.75, 5.25),
    ("3.3V", 3.135, 3.465)
]

results = []

for rail, minimum, maximum in test_limits:
    result = run_voltage_test(
        dut,
        rail,
        minimum,
        maximum
    )

    results.append(result)


print(f"Testing DUT: {dut.serial_number}\n")

for result in results:
    print(
        f"{result['test_name']}: "
        f"{result['measured_value']:.2f} V -> "
        f"{result['result']}"
    )


overall_result = (
    "PASS"
    if all(result["result"] == "PASS" for result in results)
    else "FAIL"
)

print(f"\nOverall Result: {overall_result}")