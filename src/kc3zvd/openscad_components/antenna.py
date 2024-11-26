from dataclasses import dataclass

from openscad_components.base import Measurement


@dataclass
class Cable:
    category: str
    outer_diameter: Measurement
    min_bend_radius: Measurement

    @property
    def categories(self):
        return ["coax"]

    @property
    def radius(self) -> Measurement:
        return Measurement(self.outer_diameter.value / 2, self.outer_diameter.unit)

    @property
    def min_pitch(self) -> Measurement:
        return Measurement(self.outer_diameter.value, self.outer_diameter.unit)


@dataclass
class CoaxTrap:
    center_frequency: str
    cable: Cable
    turns: int
    diameter: Measurement
    min_pitch: Measurement
    min_wall_thickness: Measurement
    min_height: Measurement

    # TODO: Normalize all of these measurements!

    @property
    def pitch(self) -> Measurement:
        if self.min_pitch.value < self.cable.outer_diameter.value:
            p = Measurement(
                self.cable.outer_diameter.value, self.cable.outer_diameter.unit
            )
        else:
            p = Measurement(self.min_pitch.value, self.cable.outer_diameter.unit)

        return p

    @property
    def form_radius(self) -> Measurement:
        if self.diameter.value / 2 < self.cable.min_bend_radius.value:
            r = self.diameter.value / 2
        else:
            r = self.cable.min_bend_radius.value

        return r

    @property
    def wall_thickness(self) -> Measurement:
        if self.min_wall_thickness < ((self.cable.outer_diameter / 2) + 2):
            wt = self.cable.outer_diameter.value / 2
        else:
            wt = self.min_wall_thickness.value

        return wt

    @property
    def helix_height(self) -> Measurement:
        return self.pitch.value * self.turns


cables = {
    "rg8x": Cable("coax", Measurement(0.242, "in"), Measurement(2.4, "in")),
    "rg58": Cable("coax", Measurement(0.195, "in"), Measurement(1.5, "in")),
    "lmr195": Cable("coax", Measurement(0.195, "in"), Measurement(2, "in")),
    "lmr250": Cable("coax", Measurement(0.242, "in"), Measurement(2.5, "in")),
}


def normalize_measurements(measurements=cables, unit="mm"):
    for m in measurements:
        if measurements[m].outer_diameter.unit != unit:
            measurements[m].outer_diameter.convert(unit)


normalize_measurements()
