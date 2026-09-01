class SimulatedDUT:
    def __init__(self, serial_number):
        self.serial_number = serial_number

        self.voltage_rails = {
            "12V": 12.08,
            "5V": 5.02,
            "3.3V": 3.01
        }

    def measure_voltage(self, rail):
        return self.voltage_rails[rail]

