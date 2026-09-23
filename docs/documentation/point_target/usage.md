---
icon: lucide/pencil-sparkles
title: "Usage"
tags:
    - point target
    - simulation
    - e2e
    - python
---

# Working with Point Target Binary

In `aresys_io`, point target binary products are managed primarily through the `PointSetProduct` class, alongside the
`NominalPointTarget` dataclass and conversion utilities.

All classes and functions can be imported from `aresys_io.product` or `aresys_io.product.point_target`:

```python
from aresys_io.product import (
    CoordinatesMemmap,
    NominalPointTarget,
    PointSetProduct,
    RCSMemmap,
    convert_array_to_point_target_structure,
)
```

## Opening and Creating Products

A point target product folder is accessed by instantiating `PointSetProduct` with the destination folder path and the
desired `open_mode`:

```python
from pathlib import Path
from aresys_io.product import PointSetProduct

product_path = Path("path/to/point_targets")

# Open an existing product in read mode (default)
product = PointSetProduct(product_path, open_mode="r")

# Or initialize a product in write mode
product_writer = PointSetProduct(product_path, open_mode="w")
```

### `PointSetProduct` Properties

- `product_path`: returns the `Path` to the product folder.
- `number_of_targets`: returns the total number of point targets available in the product (available in read mode `"r"`).

!!! info "Read mode validation"

    When opened in read mode (`"r"`), `PointSetProduct` verifies that:
    
    1. The directory exists.
    2. All 7 binary raster files and their 7 XML metadata files are present.
    3. Every metadata file defines `samples = 1`.
    4. The number of lines (`lines`) is identical across all metadata files.

## Writing Point Target Data

To write point target data to disk, open a `PointSetProduct` in write mode (`open_mode="w"`) and call `write_data()`:

```python
from pathlib import Path
import numpy as np
from aresys_io.product import PointSetProduct

product_path = Path("my_point_targets")
product = PointSetProduct(product_path, open_mode="w")

# Coordinates array: shape (N, 3) representing [X, Y, Z] in meters
coords = np.array(
    [
        [2197913.48, 1102055.63, 5865641.60],
        [2198000.00, 1102100.00, 5865700.00],
    ],
    dtype=np.float64,
)

# Polarimetric RCS array: shape (N, 4) representing [HH, HV, VH, VV]
rcs = np.array(
    [
        [1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j],
        [0.5 + 0.2j, 0.1 + 0.0j, 0.1 + 0.0j, 0.5 - 0.2j],
    ],
    dtype=np.complex128,
)

product.write_data(
    coords=coords,
    rcs=rcs,
    coords_data_type="FLOAT64",
    rcs_data_type="FLOAT_COMPLEX",
)
```

`write_data()` automatically:

1. Creates the target directory if it does not already exist.
2. Writes each coordinate axis to `PointTargetPosX`, `PointTargetPosY`, and `PointTargetPosZ`.
3. Writes each polarimetric scattering component to `PointTargetRCSHH`, `PointTargetRCSHV`, `PointTargetRCSVH`, and `PointTargetRCSVV`.
4. Writes the corresponding XML metadata files populated with `RasterInfo` elements.

### Supported Data Types

The following data types can be configured via parameters:

- `coords_data_type`: `"FLOAT64"` (default) or `"FLOAT32"`.
- `rcs_data_type`: `"FLOAT_COMPLEX"` (default, single precision complex) or `"DOUBLE_COMPLEX"`.

## Reading Point Target Data

### Reading All Targets

To read all point targets from an existing product, instantiate `PointSetProduct` in read mode and call `read_data()`:

```python
product = PointSetProduct(product_path, open_mode="r")

print(f"Total targets: {product.number_of_targets}")

coords, rcs = product.read_data()

print(f"Coordinates shape: {coords.shape}")  # (N, 3)
print(f"RCS shape: {rcs.shape}")  # (N, 4)
```

- `coords` is an `(N, 3)` NumPy array containing `[X, Y, Z]` positions.
- `rcs` is an `(N, 4)` NumPy array containing `[HH, HV, VH, VV]` complex RCS values.

### Windowed and Chunked Reading

For large datasets, you can read a subset of targets by specifying `start` and `num_points`:

```python
# Read 100 targets starting from index 50
sub_coords, sub_rcs = product.read_data(start=50, num_points=100)

print(sub_coords.shape)  # (100, 3)
print(sub_rcs.shape)  # (100, 4)
```

This performs block reading directly from the underlying binary files without loading unnecessary targets into memory.

## Memory-Mapped Reading

When dealing with massive point target collections (e.g., millions of scatterers in large distributed simulations),
`PointSetProduct` provides a context manager for memory-mapped access:

```python
with product.read_data_as_memmap() as (coords_mm, rcs_mm):
    # coords_mm is a CoordinatesMemmap instance
    print(coords_mm.x.shape)  # (N, 1)
    print(coords_mm.y.shape)  # (N, 1)
    print(coords_mm.z.shape)  # (N, 1)

    # rcs_mm is an RCSMemmap instance
    print(rcs_mm.HH.shape)  # (N, 1)
    print(rcs_mm.HV.shape)  # (N, 1)
    print(rcs_mm.VH.shape)  # (N, 1)
    print(rcs_mm.VV.shape)  # (N, 1)

    # Slice or inspect scatterers without copying full arrays into memory
    first_target_x = coords_mm.x[0, 0]
    first_target_hh = rcs_mm.HH[0, 0]
```

`read_data_as_memmap()` yields:

- `CoordinatesMemmap`: object containing `.x`, `.y`, and `.z` memory-mapped 2D arrays of shape `(N, 1)`.
- `RCSMemmap`: object containing `.HH`, `.HV`, `.VH`, and `.VV` memory-mapped 2D arrays of shape `(N, 1)`.

All open file handles and memory-mapped views are cleanly closed when exiting the `with` block.

## Converting to High-Level Nominal Point Targets

For object-oriented processing, `aresys_io` provides the `NominalPointTarget` dataclass:

```python
from aresys_io.product import NominalPointTarget

target = NominalPointTarget(
    xyz_coordinates=np.array([2197913.48, 1102055.63, 5865641.60]),
    rcs_hh=1.0 + 0j,
    rcs_hv=0.0 + 0j,
    rcs_vh=0.0 + 0j,
    rcs_vv=1.0 + 0j,
    delay=0.0,
)
```

### Batch Conversion with `convert_array_to_point_target_structure`

You can convert raw `coords` and `rcs` arrays into a dictionary mapping target identifiers to `NominalPointTarget`
instances using `convert_array_to_point_target_structure()`:

```python
from aresys_io.product import convert_array_to_point_target_structure

# Automatic string IDs ("0", "1", "2", ...)
targets_dict = convert_array_to_point_target_structure(coords, rcs)

# Or provide custom target identifiers
custom_ids = ["CR_01", "CR_02"]
targets_dict = convert_array_to_point_target_structure(
    coords,
    rcs,
    point_target_ids=custom_ids,
)

for target_id, target_obj in targets_dict.items():
    print(f"Target {target_id}:")
    print(f"  Coordinates: {target_obj.xyz_coordinates}")
    print(f"  HH: {target_obj.rcs_hh}, VV: {target_obj.rcs_vv}")
```

## Validation and Error Handling

`PointSetProduct` performs strict validation to prevent corrupted products:

- **Shape checks:** `coords` must have shape `(N, 3)` and `rcs` must have shape `(N, 4)`. A `RuntimeError` is raised if dimensions do not match.
- **Count consistency:** The number of rows in `coords` must match the number of rows in `rcs`.
- **Read bounds:** In `read_data()`, negative `start`, non-positive `num_points`, or ranges exceeding `number_of_targets` raise a `ValueError`.
- **Metadata verification:** When opening a product, inconsistency in `lines` or `samples != 1` across metadata files raises a `RuntimeError`.
