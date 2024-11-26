import openscad_components.antenna as antenna
from openscad_components.base import Measurement

def test_coax_trap():
  for cable, specs in antenna.cables.items():

    trap = antenna.CoaxTrap(
      center_frequency="415.5Mhz",
      cable=antenna.cables[cable],
      turns=0,
      diameter=Measurement(
        value=10,
        unit='mm'
      ),
      min_pitch=Measurement(
        value=5,
        unit='mm'
      ),
      min_wall_thickness=Measurement(
        value=3,
        unit='mm'
      ),
      min_height=Measurement(
        value=50,
        unit='mm'
      )
    )
  
  print(f'Cable Type: {cable}')
  print(f'Cable Diameter: {specs.outer_diameter.value} {specs.outer_diameter.unit}')
  print(f'Cable Minimum Pitch: {specs.min_pitch.value} {specs.min_pitch.unit}')
  print(f'Trap Pitch: {trap.pitch.value} {trap.pitch.unit}')
  print('\n')
  assert trap.pitch.value >= specs.min_pitch.value
