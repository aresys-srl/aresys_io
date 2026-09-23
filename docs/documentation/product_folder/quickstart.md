---
icon: lucide/zap
title: "Quickstart"
tags:
    - pf
    - product folder
    - L1
    - L0
    - python
    - quickstart
    - example
---

# Quickstart example

The following is a complete, runnable example that demonstrates all the functionalities described above. Copy it into a
Python file and run it to start working with `aresys_io`.

```python
from pathlib import Path

import numpy as np
from perseo_core.timing import PreciseDateTime

from aresys_io.product import (
    create_new_metadata,
    create_product_folder,
    is_product_folder,
    is_valid_product_folder,
    iter_channels,
    metadata,
    open_product_folder,
    read_metadata,
    read_raster_with_raster_info,
    write_metadata,
    write_raster_with_raster_info,
)

PRODUCT_PATH = Path("example_product_folder")

LINES = 100
SAMPLES = 200


# -----------------------------------------------------------------------------
# 1. Create a Product Folder
# -----------------------------------------------------------------------------

print(f"Creating Product Folder: {PRODUCT_PATH}")

product = create_product_folder(
    PRODUCT_PATH,
    overwrite_ok=True,
)

print(f"Product name: {product.name}")
print(f"Product path: {product.path.absolute()}")
print(f"Manifest: {product.manifest.absolute()}")


# -----------------------------------------------------------------------------
# 2. Create metadata for channel 1
# -----------------------------------------------------------------------------

print("\nCreating metadata for channel 1...")

channel_1_metadata = create_new_metadata(
    num_metadata_channels=1,
    description="Example channel",
)

raster_info = metadata.RasterInfo(
    lines=LINES,
    samples=SAMPLES,
    cell_type="FLOAT32",
    file_name=product.channel_data_path(1).name,
    header_offset_bytes=0,
    row_prefix_bytes=0,
    byteorder="LITTLEENDIAN",
    invalid_value=None,
    format_type=None,
)

swath_info = metadata.SwathInfo(
    swath="S1",
    polarization="HH",
    acquisition_start_time=PreciseDateTime.now(),
)

channel_1_metadata.insert_element(raster_info)
channel_1_metadata.insert_element(swath_info)


# -----------------------------------------------------------------------------
# 3. Write channel 1 metadata and raster
# -----------------------------------------------------------------------------

print("Writing channel 1 metadata and raster...")

write_metadata(
    metadata_obj=channel_1_metadata,
    metadata_file=product.channel_metadata_path(1),
)

# Create some example raster data.
channel_1_raster = np.arange(
    LINES * SAMPLES,
    dtype=np.float32,
).reshape(LINES, SAMPLES)

write_raster_with_raster_info(
    raster_file=product.channel_data_path(1),
    data=channel_1_raster,
    raster_info=channel_1_metadata.raster_info,
)


# -----------------------------------------------------------------------------
# 4. Read channel 1 metadata and raster
# -----------------------------------------------------------------------------

print("\nReading channel 1...")

read_channel_1_metadata = read_metadata(product.channel_metadata_path(1))

read_channel_1_raster = read_raster_with_raster_info(
    raster_file=product.channel_data_path(1),
    raster_info=read_channel_1_metadata.raster_info,
)

print(f"Channel 1 metadata: {read_channel_1_metadata}")
print(f"Channel 1 raster shape: {read_channel_1_raster.shape}")
print(f"Channel 1 raster dtype: {read_channel_1_raster.dtype}")


# -----------------------------------------------------------------------------
# 5. Create channel 2 by copying channel 1 metadata
# -----------------------------------------------------------------------------

print("\nCreating channel 2...")

channel_2_metadata = read_metadata(product.channel_metadata_path(1))

# Update the metadata to point to channel 2's raster file.
channel_2_metadata.raster_info.file_name = product.channel_data_path(2).name

# Change the polarization as an example.
channel_2_metadata.swath_info.polarization = "VV"

write_metadata(
    metadata_obj=channel_2_metadata,
    metadata_file=product.channel_metadata_path(2),
)


# -----------------------------------------------------------------------------
# 6. Create and write channel 2 raster
# -----------------------------------------------------------------------------

channel_2_raster = channel_1_raster * 2

write_raster_with_raster_info(
    raster_file=product.channel_data_path(2),
    data=channel_2_raster,
    raster_info=channel_2_metadata.raster_info,
)


# -----------------------------------------------------------------------------
# 7. List available channels
# -----------------------------------------------------------------------------

print("\nAvailable channels:")

print(product.channel_ids)


# -----------------------------------------------------------------------------
# 8. Iterate over all channels
# -----------------------------------------------------------------------------

print("\nIterating over channels...")

for channel_id, channel_metadata in iter_channels(product):
    raster_path = product.channel_data_path(channel_id)

    raster = read_raster_with_raster_info(
        raster_file=raster_path,
        raster_info=channel_metadata.raster_info,
    )

    print(
        f"Channel {channel_id}: "
        f"polarization={channel_metadata.swath_info.polarization}, "
        f"shape={raster.shape}, "
        f"dtype={raster.dtype}"
    )


# -----------------------------------------------------------------------------
# 9. Iterate over channels with filtering
# -----------------------------------------------------------------------------

print("\nHH channels:")

for channel_id, channel_metadata in iter_channels(
    product,
    polarization="HH",
):
    print(f"Channel {channel_id}: polarization={channel_metadata.swath_info.polarization}")


print("\nVV channels:")

for channel_id, channel_metadata in iter_channels(
    product,
    polarization="VV",
):
    print(f"Channel {channel_id}: polarization={channel_metadata.swath_info.polarization}")


# -----------------------------------------------------------------------------
# 10. Validate the Product Folder
# -----------------------------------------------------------------------------

print("\nValidating Product Folder...")

print(f"Is Product Folder: {is_product_folder(PRODUCT_PATH)}")

print(f"Is valid Product Folder: {is_valid_product_folder(PRODUCT_PATH)}")


# -----------------------------------------------------------------------------
# 11. Re-open the Product Folder
# -----------------------------------------------------------------------------

print("\nRe-opening Product Folder...")

product = open_product_folder(PRODUCT_PATH)

print(f"Product path: {product.path}")
print(f"Channels: {product.channel_ids}")


# -----------------------------------------------------------------------------
# 12. Create a metadata object with multiple metadata channels
# -----------------------------------------------------------------------------

print("\nCreating a metadata object with multiple metadata channels...")

multi_channel_metadata = create_new_metadata(
    num_metadata_channels=2,
    description="Multi-channel metadata example",
)

# Create raster information for the first metadata channel.
raster_info = metadata.RasterInfo(
    lines=LINES,
    samples=SAMPLES,
    cell_type="FLOAT32",
    file_name="TX_GRD_0001",
    header_offset_bytes=0,
    row_prefix_bytes=0,
    byteorder="LITTLEENDIAN",
    invalid_value=None,
    format_type=None,
)

# Create swath information for the first metadata channel.
swath_info = metadata.SwathInfo(
    swath="S1",
    polarization="HH",
    acquisition_start_time=PreciseDateTime.now(),
)

# Add the information to the first metadata channel.
multi_channel_metadata.insert_element(raster_info)
multi_channel_metadata.insert_element(swath_info)

# The first metadata channel can be accessed directly.
print(f"First channel raster filename: {multi_channel_metadata[0].raster_info.file_name}")

# Configure the second metadata channel.
multi_channel_metadata[1].content_id = "Tx"
# Here you can add different information specific to the Tx metadata channel.
multi_channel_metadata[1].insert_element(swath_info)

print(f"Number of metadata channels: {len(multi_channel_metadata.channels)}")

print(f"Second channel content ID: {multi_channel_metadata[1].content_id}")

print(f"Second channel polarization: {multi_channel_metadata[1].swath_info.polarization}")

# The channels property provides direct access to the list.
for index, metadata_channel in enumerate(multi_channel_metadata.channels):
    print(f"Metadata channel {index}: content_id={metadata_channel.content_id}")


print("Done!")
```
