---
icon: lucide/zap
title: "Quickstart"
tags:
    - point target
    - simulation
    - e2e
    - python
    - quickstart
    - example
---

# Quickstart example

The following is a complete, runnable example that demonstrates all the functionalities described in the previous
sections. Copy it into a Python file and run it to start working with Point Target Binary products.

```python
import shutil
from pathlib import Path

import numpy as np

from aresys_io.product import (
    PointSetProduct,
    convert_array_to_point_target_structure,
)

PRODUCT_PATH = Path("example_point_targets")
NUM_TARGETS = 10


# -----------------------------------------------------------------------------
# 1. Synthesize point target data
# -----------------------------------------------------------------------------

print(f"Synthesizing {NUM_TARGETS} point targets...")

# Target coordinates: (N, 3) in Cartesian / ECEF coordinates [X, Y, Z]
base_coord = np.array([2197913.48, 1102055.64, 5865641.61])
offsets = np.arange(NUM_TARGETS)[:, np.newaxis] * 100.0
coords = base_coord + offsets

# Polarimetric RCS: (N, 4) complex scattering values [HH, HV, VH, VV]
# Simulating trihedral corner reflectors (co-pol = 1.0, cross-pol = 0.0)
rcs = np.zeros((NUM_TARGETS, 4), dtype=np.complex128)
rcs[:, 0] = 1.0 + 0.0j  # HH
rcs[:, 1] = 0.0 + 0.0j  # HV
rcs[:, 2] = 0.0 + 0.0j  # VH
rcs[:, 3] = 1.0 + 0.0j  # VV

print(f"Coordinates shape: {coords.shape}")
print(f"RCS shape: {rcs.shape}")


# -----------------------------------------------------------------------------
# 2. Write Point Target Binary product
# -----------------------------------------------------------------------------

print(f"\nWriting Point Target Binary product to: {PRODUCT_PATH.resolve()}")

prod_writer = PointSetProduct(PRODUCT_PATH, open_mode="w")
prod_writer.write_data(
    coords=coords,
    rcs=rcs,
    coords_data_type="FLOAT64",
    rcs_data_type="FLOAT_COMPLEX",
)

print("Product successfully created.")


# -----------------------------------------------------------------------------
# 3. Open and inspect product in read mode
# -----------------------------------------------------------------------------

print("\nOpening product in read mode...")

prod_reader = PointSetProduct(PRODUCT_PATH, open_mode="r")

print(f"Product path: {prod_reader.product_path}")
print(f"Number of targets: {prod_reader.number_of_targets}")


# -----------------------------------------------------------------------------
# 4. Read all data
# -----------------------------------------------------------------------------

print("\nReading all point target data...")

read_coords, read_rcs = prod_reader.read_data()

print(f"Read coordinates shape: {read_coords.shape}, dtype: {read_coords.dtype}")
print(f"Read RCS shape: {read_rcs.shape}, dtype: {read_rcs.dtype}")
print(f"First target position: {read_coords[0]}")
print(f"First target RCS: HH={read_rcs[0, 0]}, VV={read_rcs[0, 3]}")


# -----------------------------------------------------------------------------
# 5. Windowed / subset reading
# -----------------------------------------------------------------------------

print("\nReading a subset of targets (windowed read)...")

sub_coords, sub_rcs = prod_reader.read_data(start=2, num_points=4)

print(f"Subset coordinates shape: {sub_coords.shape}")
print(f"Subset RCS shape: {sub_rcs.shape}")


# -----------------------------------------------------------------------------
# 6. Memory-mapped reading
# -----------------------------------------------------------------------------

print("\nStreaming targets via memory mapping...")

with prod_reader.read_data_as_memmap() as (coords_mm, rcs_mm):
    print(f"X coordinate memmap shape: {coords_mm.x.shape}")
    print(f"HH RCS memmap shape: {rcs_mm.HH.shape}")

    # Access elements directly on disk without allocating full arrays
    for i in range(3):
        print(
            f"Target {i}: Pos=({coords_mm.x[i, 0]:.2f}, {coords_mm.y[i, 0]:.2f}, {coords_mm.z[i, 0]:.2f}) "
            f"| HH={rcs_mm.HH[i, 0]}"
        )


# -----------------------------------------------------------------------------
# 7. Convert to structured NominalPointTarget objects
# -----------------------------------------------------------------------------

print("\nConverting array data to NominalPointTarget dictionary...")

target_ids = [f"CR_{i:02d}" for i in range(NUM_TARGETS)]
targets_dict = convert_array_to_point_target_structure(
    coords=read_coords,
    rcs=read_rcs,
    point_target_ids=target_ids,
)

sample_id = "CR_00"
sample_target = targets_dict[sample_id]

print(f"Target ID: {sample_id}")
print(f"  Coordinates: {sample_target.xyz_coordinates}")
print(f"  RCS HH: {sample_target.rcs_hh}")
print(f"  RCS HV: {sample_target.rcs_hv}")
print(f"  RCS VH: {sample_target.rcs_vh}")
print(f"  RCS VV: {sample_target.rcs_vv}")
print(f"  Delay: {sample_target.delay}")


# -----------------------------------------------------------------------------
# 8. Clean up example product folder
# -----------------------------------------------------------------------------

if PRODUCT_PATH.exists():
    shutil.rmtree(PRODUCT_PATH)

print("\nDone!")
```
