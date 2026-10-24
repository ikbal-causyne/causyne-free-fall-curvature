"""Reproduce the illustrative spherical-Earth estimates in the manuscript.

Copyright (c) 2026 Ikbal Fadilah. SPDX-License-Identifier: MIT.
No measurements are fitted or inferred by this script.
"""

from math import isclose, sqrt


GM = 3.98600435507e14  # m^3 s^-2, JPL DE440 Earth GM
R = 6.371e6  # m, NASA volumetric mean Earth radius
C = 299_792_458  # m s^-1, exact SI definition
H = 1.0  # m, radial probe/clock separation
ORBIT_HEIGHT = 400_000.0  # m, illustrative circular orbit
T = 1.0  # s, illustrative short drift time


def estimates(radius: float) -> dict[str, float]:
    g = GM / radius**2
    tidal_radial = 2 * GM * H / radius**3
    return {
        "g": g,
        "radial_tidal_acceleration": tidal_radial,
        "radial_tidal_ratio": tidal_radial / g,
        "one_second_radial_drift": 0.5 * tidal_radial * T**2,
    }


surface = estimates(R)
orbit = estimates(R + ORBIT_HEIGHT)
redshift_fraction = surface["g"] * H / C**2
orbit_speed = sqrt(GM / (R + ORBIT_HEIGHT))

assert isclose(surface["g"], 9.82025, rel_tol=1e-6)
assert isclose(surface["radial_tidal_acceleration"], 3.08280e-6, rel_tol=1e-5)
assert isclose(surface["radial_tidal_ratio"], 3.139e-7, rel_tol=1e-4)
assert isclose(redshift_fraction, 1.09265e-16, rel_tol=1e-5)
assert isclose(orbit["g"], 8.69425, rel_tol=1e-5)
assert isclose(orbit_speed, 7_672.6, rel_tol=1e-4)
assert isclose(surface["one_second_radial_drift"], 1.54140e-6, rel_tol=1e-5)
assert isclose(orbit["one_second_radial_drift"], 1.2840e-6, rel_tol=1e-4)

for name, values in (("surface", surface), ("400 km orbit", orbit)):
    print(name)
    for key, value in values.items():
        print(f"  {key}: {value:.9g}")
print(f"surface clock-rate fraction per meter: {redshift_fraction:.9g}")
print(f"illustrative orbit speed: {orbit_speed:.9g} m/s")
