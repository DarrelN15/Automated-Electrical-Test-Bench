import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

from dut import SimulatedDUT
from voltage_test import run_voltage_test


def parse_arguments():
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

    return parser.parse_args()


def load_config():
    with open("test_config.json", "r") as config_file:
        return json.load(config_file)


def run_test_sequence(dut, config):
    results = []

    for test in config["tests"]:
        result = run_voltage_test(
            dut,
            test["rail"],
            test["minimum"],
            test["maximum"]
        )

        results.append(result)

    return results


def calculate_overall_result(results):
    if all(result["result"] == "PASS" for result in results):
        return "PASS"

    return "FAIL"


def save_results(
    dut,
    config,
    results,
    overall_result,
    fault_mode
):
    results_directory = Path("results")
    results_directory.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    output_file = (
        results_directory
        / f"{dut.serial_number}_{timestamp}_results.csv"
    )

    run_metadata = {
        "serial_number": dut.serial_number,
        "device": config["device"],
        "timestamp": timestamp,
        "fault_mode": fault_mode if fault_mode else "NONE",
        "overall_result": overall_result
    }

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

    return output_file


def main():
    args = parse_arguments()
    config = load_config()

    dut = SimulatedDUT(
        args.serial,
        fault_mode=args.fault
    )

    results = run_test_sequence(
        dut,
        config
    )

    print(f"Testing DUT: {dut.serial_number}\n")

    for result in results:
        print(
            f"{result['test_name']}: "
            f"{result['measured_value']:.2f} V -> "
            f"{result['result']}"
        )

    overall_result = calculate_overall_result(results)

    print(f"\nOverall Result: {overall_result}")

    output_file = save_results(
        dut,
        config,
        results,
        overall_result,
        args.fault
    )

    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()