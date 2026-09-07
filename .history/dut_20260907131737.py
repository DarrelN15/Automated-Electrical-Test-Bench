class SimulatedDUT:
    def __init__(self, serial_number, fault_mode=None):
        self.serial_number = serial_number
        self.fault_mode = fault_mode

        self.voltage_rails = {
            "12V": 12.08,
            "5V": 5.02,
            "3.3V": 3.31
        }

        self.apply_fault()

    def apply_fault(self):
        if self.fault_mode == "LOW_3V3":
            self.voltage_rails["3.3V"] = 3.01

        elif self.fault_mode == "HIGH_5V":
            self.voltage_rails["5V"] = 5.50

        elif self.fault_mode == "LOW_12V":
            self.voltage_rails["12V"] = 10.80

    def measure_voltage(self, rail):
        return self.voltage_rails[rail]