import csv
import json
import argparse
from pathlib import Path
from datetime import datetime

from dut import SimulatedDUT
from voltage_test import run_voltage_test

parser = argparse.ArgumentParser(
    description="Automated Electrical Test Bench"
)

parser.add_argument(
    "--serial",
    default="PCM-0001",
    help="Serial number of the device under test"
)

parser.add_argument(
    "--fault",
    choices=[
        "LOW_3V3",
        "HIGH_5V",
        "LOW_12V"
    ],
    default=None,
    help="Optional simulated hardware fault"
)

args = parser.parse_args()

serial_number = args.serial
fault_mode = args.fault

dut = SimulatedDUT(
    serial_number,
    fault_mode=fault_mode
)

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

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
run_metadata = {
    "serial_number": dut.serial_number,
    "device": config["device"],
    "timestamp": timestamp,
    "fault_mode": fault_mode if fault_mode else "NONE",
    "overall_result": overall_result
}

output_file = (
    results_directory
    / f"{dut.serial_number}_{timestamp}_results.csv"
)

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["Test Run Metadata"])
    writer.writerow(["serial_number", run_metadata["serial_number"]])
    writer.writerow(["device", run_metadata["device"]])
    writer.writerow(["timestamp", run_metadata["timestamp"]])
    writer.writerow(["fault_mode", run_metadata["fault_mode"]])
    writer.writerow(["overall_result", run_metadata["overall_result"]])

    writer.writerow([])

    fieldnames = [
        "test_name",
        "measured_value",
        "minimum",
        "maximum",
        "result"
    ]

    dict_writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames
    )

    dict_writer.writeheader()
    dict_writer.writerows(results)

print(f"Results saved to: {output_file}")