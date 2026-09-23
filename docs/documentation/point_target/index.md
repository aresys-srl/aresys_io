---
icon: lucide/crosshair
title: "Point Target Binary"
tags:
    - point target
    - simulation
    - e2e
    - calibration
    - python
---

# Point Target Binary { #targets data-toc-label="Point Target" }

The **Point Target Binary** format is the official Aresys format for storing and organizing artificial or real
point targets used throughout SAR simulation and calibration processing chains.

Each target is defined by its 3D spatial coordinates and its full polarimetric radar cross section (RCS). The format
stores discrete radar reflectors (such as corner reflectors, active radar calibrators, or synthetic point scatterers) and
it's mainly used in SAR end-to-end (E2E) simulators, performance assessment, and impulse response function (IRF) analysis.

Managing and working with this format is handled directly via `aresys_io.product` or in the dedicated module `aresys_io.product.point_target`.
Common operations include:

- creating and writing Point Target Binary products
- reading point target coordinates and polarimetric RCS values
- chunked and windowed reading for large simulation datasets
- memory-mapped access for zero-copy, efficient streaming of large scatterer fields
- converting arrays to structured nominal point target objects

## Product Structure

A Point Target Binary product is physically organized as a **folder** containing a fixed set of binary raster files
accompanied by corresponding XML metadata files.

A complete point target product consists of **7 binary raster files** and **7 matching XML annotation files**:

- **3 Coordinates rasters & metadata**: one for each spatial dimension ($X$, $Y$, and $Z$) in Cartesian coordinates (typically ECEF).
- **4 Radar Cross Section (RCS) rasters & metadata**: one for each linear polarization channel ($HH$, $HV$, $VH$, and $VV$) representing the complex scattering matrix.

Each binary file represents a 1D column raster containing the respective value for every point target in the dataset.

## Point Target Binary at a Glance

From a structural point of view, a Point Target Binary product folder is organized as follows:

```text
Point Target Folder/
├── PointTargetPosX          # X coordinate binary raster
├── PointTargetPosX.xml      # X coordinate metadata
├── PointTargetPosY          # Y coordinate binary raster
├── PointTargetPosY.xml      # Y coordinate metadata
├── PointTargetPosZ          # Z coordinate binary raster
├── PointTargetPosZ.xml      # Z coordinate metadata
├── PointTargetRCSHH         # HH polarization complex RCS binary raster
├── PointTargetRCSHH.xml     # HH polarization metadata
├── PointTargetRCSHV         # HV polarization complex RCS binary raster
├── PointTargetRCSHV.xml     # HV polarization metadata
├── PointTargetRCSVH         # VH polarization complex RCS binary raster
├── PointTargetRCSVH.xml     # VH polarization metadata
├── PointTargetRCSVV         # VV polarization complex RCS binary raster
└── PointTargetRCSVV.xml     # VV polarization metadata
```

All 7 raster files share the exact same number of lines ($N$, corresponding to the total number of point targets) and have
a single sample per line (`samples = 1`).

## Product Components

### Coordinates Rasters and Metadata

The **coordinates rasters** store the 3D position vector for each point target:

- `PointTargetPosX`: $X$ coordinate in meters.
- `PointTargetPosY`: $Y$ coordinate in meters.
- `PointTargetPosZ`: $Z$ coordinate in meters.

Positions are stored as floating-point values, using either single precision (`FLOAT32`) or double precision (`FLOAT64`).
Each raster has an associated XML annotation file containing a `RasterInfo` element describing the data layout, cell type,
number of lines ($N$), and byte order.

### RCS Rasters and Metadata

The **RCS rasters** store the complex scattering coefficients representing the full polarimetric scattering matrix for
each point target:

- `PointTargetRCSHH`: Horizontal transmit, Horizontal receive ($S_{HH}$).
- `PointTargetRCSHV`: Vertical transmit, Horizontal receive ($S_{HV}$).
- `PointTargetRCSVH`: Horizontal transmit, Vertical receive ($S_{VH}$).
- `PointTargetRCSVV`: Vertical transmit, Vertical receive ($S_{VV}$).

Scattering values are stored as complex numbers, using either single-precision complex (`FLOAT_COMPLEX`) or double-precision
complex (`DOUBLE_COMPLEX`). The corresponding XML files provide standard Aresys metadata for each polarization channel.

### Consistency Requirements

When opening a Point Target Binary product in read mode:

1. The folder must exist and be a valid directory.
2. All 7 binary raster files and all 7 XML metadata files must be present.
3. Every metadata file must specify `samples = 1`.
4. The number of lines (`lines`) must be consistent across all 7 metadata files, defining the total number of targets.

## High-Level Representation: Nominal Point Targets

While the binary product stores tabular data in separate rasters for performance and fast column access, `aresys_io`
also provides a high-level Python representation:

- `NominalPointTarget`: A dataclass encapsulating an individual target's 3D position vector ($X, Y, Z$), complex polarimetric
  scattering coefficients ($S_{HH}, S_{HV}, S_{VH}, S_{VV}$), and an optional delay.
- `convert_array_to_point_target_structure()`: A conversion utility to transform raw coordinate and RCS arrays into a
  keyed dictionary of `NominalPointTarget` instances.
