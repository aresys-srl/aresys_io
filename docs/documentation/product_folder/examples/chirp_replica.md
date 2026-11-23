---
icon: lucide/book-user
title: "Creating a new PF"
tags:
    - pf
    - product folder
    - L1
    - tutorial
    - examples
---

# Creating a new Chirp Replica product

This tutorial walks through the process of creating a new Product Folder, generating a chirp replica signal, and saving
the resulting data to disk.

Here is the download link for the following exercise as a Jupyter notebook that can be run locally.

<div class="download-buttons" markdown>

[:material-download: Download Jupyter Notebook](../../../assets/notebooks/chirp_replica.ipynb){ .md-button .button-green }

</div>

## Chirp generation

We first define a function to generate a customizable one-dimensional (1D) chirp signal. The function allows users to
configure the following parameters:

- **Number of samples**: Total length of the generated signal.
- **Sampling rate**: Number of samples acquired per second.
- **Start frequency**: Initial frequency of the chirp signal.
- **Start phase**: Initial phase of the signal.
- **Bandwidth**: Frequency range covered by the chirp.
- **Pulse length**: Duration of the chirp pulse.
- **Direction**: Frequency sweep direction (UP or DOWN).
- **Delay**: Time domain delay.

``` python
from typing import Literal

import numpy as np
import numpy.typing as npt


def generate_chirp(
    samples: int,
    sampling_frequency: float,
    start_frequency: float,
    bandwidth: float,
    pulse_length: float,
    direction: Literal["UP", "DOWN"],
    start_phase: float | None = None,
    delay: float | None = None,
) -> npt.NDArray[np.complex64]:
    """Generate a 1D chirp signal.

    Parameters
    ----------
    samples : int
        Length of the generated array.
    sampling_frequency : float
        Sampling frequency [Hz].
    start_frequency : float
        Chirp starting frequency [Hz].
    bandwidth : float
        Chirp bandwidth [Hz].
    pulse_length : float
        Pulse length [s].
    direction : Literal["UP", "DOWN"]
        Chirp direction.
    start_phase : float | None, optional
        Chirp starting phase [rad], if None it's set to 0.0, by default None
    delay : float | None. optional
        Time-domain delay [s], implemented through a linear phase in frequency,
        if None, it's set to 0.0, by default None

    Returns
    -------
    npt.NDArray[np.complex64]
        Chirp array of shape (samples,).
    """
    delay = delay or 0.0
    start_phase = start_phase or 0.0

    axis = np.arange(samples) / sampling_frequency

    direction_factor = 1 if direction == "UP" else -1
    chirp_rate = bandwidth / pulse_length

    # Generate the un-shifted chirp as the starting (reference) signal.
    chirp_axis = axis[axis <= pulse_length]
    chirp_phase_quadratic = np.pi * chirp_rate * chirp_axis**2
    chirp_phase_linear = 2 * np.pi * start_frequency * chirp_axis
    chirp_phase = direction_factor * chirp_phase_quadratic + chirp_phase_linear + start_phase

    chirp_signal = np.zeros(samples, dtype=np.complex64)
    chirp_signal[axis <= pulse_length] = np.exp(1j * chirp_phase)

    if delay:
        # Frequency-domain time shift: X(f) * exp(-j * 2π * f * delay).
        chirp_fft = np.fft.fft(chirp_signal)
        frequencies = np.fft.fftfreq(samples, d=1 / sampling_frequency)
        chirp_fft *= np.exp(-1j * 2 * np.pi * frequencies * delay)
        chirp_signal = np.fft.ifft(chirp_fft).astype(np.complex64)

    return chirp_signal
```

With the generation function defined, we can now use realistic parameter values to generate the chirp replica data.

``` python
bandwidth = 60e6  # Hz
pulse_length = 50.0e-06  # s
direction = "UP"
start_frequency = bandwidth / 2 if direction == "DOWN" else -bandwidth / 2  # Hz
sampling_rate = 1.1 * bandwidth  # Hz
delay = 10.0e-06  # s
samples = int((1.4 * pulse_length + delay) * sampling_rate)

chirp_data = generate_chirp(
    samples=samples,
    sampling_frequency=sampling_rate,
    start_frequency=start_frequency,
    bandwidth=bandwidth,
    pulse_length=pulse_length,
    direction=direction,
    delay=delay,
)
```

## Creating an empty Product Folder

Let's start by creating a new, empty Product Folder on disk. Next, we select a channel name and retrieve the corresponding
file paths for its metadata and raster data.

Note that this step only defines the folder structure and file paths; it does not create or write any files to disk.
The actual data and metadata must be explicitly persisted using the appropriate `write_*` functions.

``` python
from pathlib import Path

from aresys_io.product import create_product_folder

replica_path = Path("ChirpReplica")

chirp_pf = create_product_folder(pf_path=replica_path, overwrite_ok=True)

channel_id = 1
channel_metadata_file = chirp_pf.channel_metadata_path(channel_id)
channel_raster_file = chirp_pf.channel_data_path(channel_id)
```

## Creating a new Metadata object

Next, we define the metadata associated with our chirp replica, including additional information such as Swath and Polarization.

We then instantiate a new `Metadata` object and populate it with the metadata sections relevant to our Chirp Replica product.
Among these, `RasterInfo` is mandatory, as it describes the raster structure and dimensions of the data to be stored on disk.

!!! warning "Raster data must be 2D"

    Although the generated chirp replica is a one-dimensional array with shape `(N,)`, it must be stored as a **2D raster**,
    since Product Folder raster data follows a two-dimensional structure.

    To accommodate this requirement, the `RasterInfo` must specify:

    - **Number of lines:** `1`, corresponding to the single row in which the chirp replica will be stored.
    - **Number of samples:** `N`, corresponding to the length of the original chirp array.

    In other words, the resulting raster will have a shape of `(1, N)`, preserving all the samples of the original chirp replica.

``` python
from perseo_core.timing import PreciseDateTime

from aresys_io.product import (
    Pulse,
    RasterInfo,
    SwathInfo,
    create_new_metadata,
)

metadata = create_new_metadata()

raster_info = RasterInfo(
    lines=1,
    lines_start=0,
    lines_start_unit="s",
    lines_step=0,
    lines_step_unit="s",
    samples=samples,
    samples_start=0,
    samples_start_unit="s",
    samples_step=1 / sampling_rate,
    samples_step_unit="s",
    cell_type="FLOAT_COMPLEX",
    file_name=channel_raster_file.name,
    byte_order="LITTLEENDIAN",
)

swath = "S1"
polarization = "VV"
acquisition_start_time = PreciseDateTime.from_numeric_datetime(2026, 1, 1)
swath_info = SwathInfo(
    swath=swath,
    polarization=polarization,
    acquisition_start_time=acquisition_start_time,
)

pulse_info = Pulse(
    pulse_length=pulse_length,
    bandwidth=bandwidth,
    pulse_sampling_rate=sampling_rate,
    pulse_energy=1,
    pulse_start_frequency=start_frequency,
    pulse_start_phase=0,
    pulse_direction=direction,
)

metadata.insert_element(raster_info)
metadata.insert_element(swath_info)
metadata.insert_element(pulse_info)
```

## Writing Channel to disk

We can now persist both the metadata and the chirp replica data to disk. Once the write operations are complete, we can
validate the resulting Product Folder to ensure that it has been created correctly and complies with the expected structure.

Before writing the chirp replica, we must reshape the original one-dimensional array into a two-dimensional array with
shape `(1, N)`. This ensures that the data dimensions are consistent with the `RasterInfo` previously defined, allowing
the chirp replica to be correctly stored as a single-line raster.

``` python
from aresys_io.product import (
    is_valid_product_folder,
    write_metadata,
    write_raster_with_raster_info,
)

chirp_data_reshaped = chirp_data.reshape(1, -1)

write_metadata(metadata_obj=metadata, metadata_file=channel_metadata_file)
write_raster_with_raster_info(
    data=chirp_data_reshaped,
    raster_file=channel_raster_file,
    raster_info=raster_info,
)

assert is_valid_product_folder(replica_path)
```
