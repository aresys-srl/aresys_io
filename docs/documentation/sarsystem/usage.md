---
icon: lucide/pencil-sparkles
title: "Usage"
tags:
    - sar
    - sar system
    - timeline table
    - swath parameters table
    - trajectory
---

# Read and write SAR system parameters

This page shows how to read and write the files of a SAR system using the main functions of the `aresys_io.sarsystem` module.

All the functions are imported directly from the package:

```python
from aresys_io.sarsystem import (
    read_sat_table,
    read_swath_table,
    read_timeline_table,
    read_trajectory,
    write_swath_table_xml,
    write_timeline_table_xml,
    write_trajectory_xml,
)
```

## Expected folder structure

The examples below assume a SAR system folder organised as follows (here `Stripmap_TerraSARX_Rome`, acquisition mode `StripmapSM`, swath `StripmapSM_SS1`):

```text
Stripmap_TerraSARX_Rome/
├── AcquisitionModes/
│   └── StripmapSM/
│       └── TimelineTable.xml
├── Swaths/
│   └── StripmapSM_SS1/
│       ├── SwathParameterTable.xml
│       ├── Antenna/
│       └── Chirp/
└── Trajectory/
    └── Trajectory.xml
```

## Reading the SAR system tables in a single call

`read_sat_table` reads the timeline and all the swath parameter tables of an acquisition mode in a single call. It takes the path of the SAR system folder and the name of the acquisition mode.

```python
from pathlib import Path

sarsystem_folder = Path("Stripmap_TerraSARX_Rome")
sat_table = read_sat_table(sarsystem_folder, "StripmapSM")

timeline_table = sat_table.timeline_table  # TimeLine
swath_tables = sat_table.swath_table  # dict: beam id -> SwathTable
```

The swath tables are stored in a dictionary whose keys are the beam IDs listed in the timeline, so you can look up the table of each beam:

```python
beam_id = timeline_table.steering_velocity_list[0].beam_id
swath_table = swath_tables[beam_id]  # SwathTable
```

## Reading a single component

Each component can also be read on its own, by passing the path of its XML file.

### Timeline

```python
timeline_table = read_timeline_table(
    "Stripmap_TerraSARX_Rome/AcquisitionModes/StripmapSM/TimelineTable.xml"
)

# beam used in the first period of the acquisition cycle
print(timeline_table.acquisition_cycle[0].beam_id)  # "StripmapSM_SS1"
```

### Swath parameters table

```python
swath_table = read_swath_table(
    "Stripmap_TerraSARX_Rome/Swaths/StripmapSM_SS1/SwathParameterTable.xml"
)

# radar parameters of the first parameter period
period = swath_table.parameter_period[0]
print(period.prf)  # pulse repetition frequency [Hz]
print(period.swst)  # sampling window start time [s]
print(period.swl)  # sampling window length [s]
```

### Trajectory

```python
trajectory = read_trajectory("Stripmap_TerraSARX_Rome/Trajectory/Trajectory.xml")

positions = trajectory.state_vector.position  # array of shape (N, 3)
velocities = trajectory.state_vector.velocity  # array of shape (N, 3)
rotations = trajectory.attitude_info.rotation  # one attitude per state vector
```

The number of attitude samples is always equal to the number of state vectors.

## Writing the XML files

The `write_*` functions save the in-memory components (timeline table, swath parameters table, and trajectory) back to XML files. Each function takes an object of the same type that the corresponding `read_*` function returns, and converts it into the matching XML file.

```python
from pathlib import Path

output = Path("output_folder")
output.mkdir(exist_ok=True)

# trajectory: pass the output folder, the file is named Trajectory.xml
write_trajectory_xml(trajectory, output)

# swath table: pass the output folder, the file is named SwathParameterTable.xml
write_swath_table_xml(swath_table, output)

# timeline: pass the full path of the output file
write_timeline_table_xml(timeline_table, output / "TimelineTable.xml")
```

!!! note
    `write_trajectory_xml` and `write_swath_table_xml` expect a **folder** and use the default file name, while `write_timeline_table_xml` expects the **full file path**.

### Round trip example

```python
trajectory = read_trajectory("Trajectory.xml")
write_trajectory_xml(trajectory, "output_folder")

assert read_trajectory("output_folder/Trajectory.xml") == trajectory
```

## Summary

| Function | Input | Returns / writes |
| --- | --- | --- |
| `read_sat_table(folder, acq_mode)` | SAR system folder, acquisition mode name | `SatTable` (timeline + swath tables) |
| `read_timeline_table(file)` | `TimelineTable.xml` path | `TimeLine` |
| `read_swath_table(file)` | `SwathParameterTable.xml` path | `SwathTable` |
| `read_trajectory(file)` | `Trajectory.xml` path | `Trajectory` |
| `write_timeline_table_xml(timeline, file)` | `TimeLine`, output file path | `TimelineTable.xml` |
| `write_swath_table_xml(swath_table, folder)` | `SwathTable`, output folder | `SwathParameterTable.xml` |
| `write_trajectory_xml(trajectory, folder)` | `Trajectory`, output folder | `Trajectory.xml` |