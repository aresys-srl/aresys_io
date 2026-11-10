---
icon: lucide/satellite
title: "SAR System"
tags:
    - sar
    - sar system
    - simulation
    - e2e
---

# SAR System { #sarsys data-toc-label="SAR System" }

A **SAR system** is the set of files and folders that define every parameter used during a SAR image acquisition.

It is described by three main components:

- **Timeline**: describes the behaviour of the radar instrument throughout the acquisition. It is divided into timeline periods that repeat over the acquisition and that can point to different swaths. Moreover each period stores per-echo information such as the indexes of the antenna pattern and the transmitted chirp.

- **Swath Parameters Table**: contains the radar parameters used in a specific swath, such as PRF, sampling frequency, SWST, SWL and transmitted power. The acquisition is split into parameter periods, whose start and stop times are expressed relative to a reference time.

- **Trajectory**: contains the navigation and attitude information of the platform carrying the radar. This includes the state vectors (position and velocity) and the attitude/pointing data over the acquisition time.

This module provides the functions to read/write the XML files representing these three components.
