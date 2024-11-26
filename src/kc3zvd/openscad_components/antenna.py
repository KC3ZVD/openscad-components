from openscad_components.base import Measurement
from dataclasses import dataclass

@dataclass
class Cable:
  category: str
  outer_diameter: Measurement
  min_bend_radius: Measurement

  @property
  def categories(self):
    return ['coax']
  
  @property
  def radius(self) -> Measurement:
    return Measurement(self.outer_diameter.value/2, self.outer_diameter.unit)
  
  @property
  def min_pitch(self) -> Measurement:
    return Measurement(self.outer_diameter.value, self.outer_diameter.unit)

  def __post_init__(self):
    assert self.category in self.categories

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
      return Measurement(self.cable.outer_diameter.value, self.cable.outer_diameter.unit)
    else:
      return Measurement(self.min_pitch.value, self.cable.outer_diameter.unit)
  
  @property
  def form_radius(self) -> Measurement:
    if self.diameter.value/2 < self.cable.min_bend_radius.value:
      return self.diameter.value/2
    else:
      return self.cable.min_bend_radius.value

  @property
  def wall_thickness(self) -> Measurement:
    if self.min_wall_thickness < ( (self.cable.outer_diameter/2) + 2):
      return self.cable.outer_diameter.value/2
    else:
      return self.min_wall_thickness.value

  @property 
  def helix_height(self) -> Measurement:
    return self.pitch.value * self.turns

cables = {
  'rg8x': Cable(
    'coax',
    Measurement(0.242,'in'),
    Measurement(2.4,'in')
  ),
  'rg58': Cable(
    'coax',
    Measurement(0.195,'in'),
    Measurement(1.5,'in')
  ),
  'lmr195': Cable(
    'coax',
    Measurement(0.195,'in'),
    Measurement(2,'in')
  ),
  'lmr250': Cable(
    'coax',
    Measurement(0.242,'in'),
    Measurement(2.5,'in')
  )
}

def normalize_measurements(dict=cables, unit='mm'):
  for item in dict:
    if dict[item].outer_diameter.unit != unit:
      dict[item].outer_diameter.convert(unit)

normalize_measurements()

