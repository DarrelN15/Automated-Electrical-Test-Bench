import csv
import json
from pathlib import Path

from dut import SimulatedDUT
from voltage_test import run_voltage_test

dut = SimulatedDUT("PCM-0001")

with open("test_config.json", "r") as config_file:
    config = json.load(config_file)

results = []

for test in config["tests"]:
    rail = test["rail"]
    minimum = test["minimum"]
    maximum = test["maximum"]

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

results_directory = Path("results")
results_directory.mkdir(exist_ok=True)

output_file = results_directory / f"{dut.serial_number}_results.csv"

with open(output_file, "w", newline="") as csvfile:
    fieldnames = [
        "test_name",
        "measured_value",
        "minimum",
        "maximum",
        "result"
    ]

    writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to: {output_file}")