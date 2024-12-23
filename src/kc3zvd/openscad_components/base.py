from dataclasses import dataclass

units = ["in", "mm"]

conversion_factors = {"mm": {"in": 1 / 25.4}, "in": {"mm": 25.4}}


@dataclass
class Component:
    @property
    def shape(self):
        # Models will be generated by the extending object
        pass

    def write_scad(self, filename: str, extension: str = "scad", directory: str = "."):
        with open(f"{directory}/{filename}.{extension}", "w") as f:
            f.write(str(self.shape))


@dataclass
class Measurement:
    value: float
    unit: str

    def __post_init__(self):
        self.value = float(self.value)  # weird things, force cast it

    def convert(self, target: str):
        self.value = self.value * conversion_factors[self.unit][target]
        self.unit = target
