---
icon: lucide/pencil-sparkles
title: "Usage"
tags:
    - pf
    - product folder
    - L1
    - L0
---

# Working with Product Folders

With `aresys_io`, you can create a Product Folder using `create_product_folder()`:

```python
from pathlib import Path

from aresys_io.product import create_product_folder

pf = create_product_folder(
    Path("path/to/pf"),
    overwrite_ok=False,
)
```

An existing Product Folder can be opened using `open_product_folder()`:

```python
from pathlib import Path

from aresys_io.product import open_product_folder

pf = open_product_folder(Path("path/to/pf"))
```

Both functions return a `ProductFolder` object.

### `ProductFolder` properties

The `ProductFolder` object provides the following properties:

- `name`: the product name.
- `path`: the path to the Product Folder.
- `manifest`: the path to the product manifest.
- `raster_extension`: the raster file extension, either `""` or `"tiff"`.
- `channel_ids`: the list of channel identifiers.
- `config_path`: the path to the configuration file.
- `overlay_path`: the path to the overlay (`.kmz`) file.

### `ProductFolder` methods

The following methods are available:

- `channel_metadata_path()`: retrieves the path of the metadata file for a given channel.
- `channel_data_path()`: retrieves the path of the raster file for a given channel.
- `channel_quicklook_path()`: retrieves the path of the quicklook file for a given channel and extension (`.jpg` or `.png`).
- `rename()`: changes the product name and/or its position.
- `delete()`: deletes the product.

!!! warning "Path existence"

    Methods that return a path **do not guarantee file existence**. The returned path can also be used to determine
    where a new file should be written.

**Only the manifest file is guaranteed to be present**. When a Product Folder is opened, consistency checks are performed
on its contents.

### Product Folder validation

Two free functions are provided for product validation:

- `is_product_folder()`: checks only for the presence of the manifest file.
- `is_valid_product_folder()`: additionally checks that every data file has a corresponding metadata file and vice versa.

Free-function versions of the `rename()` and `delete()` methods are also available:

- `rename_product_folder()`
- `delete_product_folder_content()`

## Channel management: retrieving file locations

You can access the list of channels currently available on disk through the `channel_ids` property of the `ProductFolder`.

The property contains **channel identifiers**, not channel indexes. For example, if a Product Folder contains channels
`0001` and `0016`, `channel_ids` returns:

```python
[1, 16]
```

This preserves the channel identifiers encoded in the filenames and allows channels to be identified without relying on
their ordering.

Other methods, such as `channel_metadata_path()` and `channel_data_path()`, expect the same channel identifiers.

To iterate over the channels, you can use `iter_channels()`, which also supports filtering by polarization and swath name.

For example:

```python
from aresys_io.product import open_product_folder

path_to_product = ...
product = open_product_folder(path_to_product)

print(product.channel_ids)
# For example: [1, 16]

# Retrieve the absolute path of the metadata XML file for channel 16.
ch16_metadata_path = product.channel_metadata_path(16)

# Retrieve the absolute path of the raster file for channel 16.
ch16_raster_path = product.channel_data_path(16)

# Retrieve the absolute path of the .kmz archive.
# No channel number is required because there is only one overlay file per product.
kmz_file = product.overlay_path
```

You can retrieve the path for any channel number, even if that channel does not currently exist:

```python
product.channel_metadata_path(150)
```

This returns the full path for channel 150 regardless of whether the file exists. This is useful when determining the
destination path for a new channel.

## Iterating over existing channels

The `iter_channels()` function returns a Python generator that yields the channel identifier and its associated metadata
object.

Raster data is not yielded, allowing channel iteration to remain lightweight. The raster can be retrieved using the
channel identifier.

`iter_channels()` supports filtering by swath name and/or polarization.

### Iterate over all channels

```python
from aresys_io.product import iter_channels, open_product_folder

path_to_product = ...
product = open_product_folder(path_to_product)

for channel_id, channel_metadata in iter_channels(product):
    raster_file = product.channel_data_path(channel_id)
    ...
```

### Filter by polarization

```python
for channel_id, channel_metadata in iter_channels(
    product,
    polarization="HH",
):
    ...
```

You can also provide multiple polarizations:

```python
for channel_id, channel_metadata in iter_channels(
    product,
    polarization=["HH", "VV"],
):
    ...
```

### Filter by swath

```python
for channel_id, channel_metadata in iter_channels(
    product,
    swath="S1",
):
    ...
```

The filtering strategy can be further customized using `iter_channels_generator()`.

## Reading channel metadata and data

Once you have retrieved the paths to the channel metadata and data files, you can read them using `read_metadata()` and
`read_raster_with_raster_info()`.

When using `iter_channels()`, metadata files are read automatically during iteration, and the resulting `MetaData` object
is yielded directly.

For example:

```python
from aresys_io.product import (
    iter_channels,
    open_product_folder,
    read_metadata,
    read_raster_with_raster_info,
)

path_to_product = ...
product = open_product_folder(path_to_product)

# Read the metadata for channel 3.
ch3_metadata = read_metadata(product.channel_metadata_path(3))

# Read the raster for channel 3.
ch3_raster = read_raster_with_raster_info(
    raster_file=product.channel_data_path(3),
    raster_info=ch3_metadata.raster_info,
)
```

Using `iter_channels()` avoids having to read the metadata separately:

```python
for channel_id, metadata in iter_channels(product):
    # The metadata object is already available.
    ch_raster = read_raster_with_raster_info(
        raster_file=product.channel_data_path(channel_id),
        raster_info=metadata.raster_info,
    )
```

## Writing channel metadata and raster data

Writing metadata and raster data follows a similar approach, using `write_metadata()` and `write_raster_with_raster_info()`.

For example, the metadata and raster of channel 3 can be copied to a new channel 9:

```python
from aresys_io.product import (
    open_product_folder,
    read_metadata,
    read_raster_with_raster_info,
    write_metadata,
    write_raster_with_raster_info,
)

path_to_product = ...
product = open_product_folder(path_to_product)

# Read the metadata for channel 3.
ch_metadata = read_metadata(product.channel_metadata_path(3))

# Copy the metadata to channel 9.
# Update the filename to match the new raster filename.
ch_metadata.raster_info.file_name = product.channel_metadata_path(9).name

# Other raster information fields can also be modified.
ch_metadata.swath_info.polarization = "VV"

# Write the metadata for channel 9.
write_metadata(
    metadata_obj=ch_metadata,
    metadata_file=product.channel_metadata_path(9),
)

# Read the raster for channel 3.
raster = read_raster_with_raster_info(
    raster_file=product.channel_data_path(3),
    raster_info=ch_metadata.raster_info,
)

# Write the raster to channel 9.
write_raster_with_raster_info(
    raster_file=product.channel_data_path(9),
    data=raster,
    raster_info=ch_metadata.raster_info,
)
```

## Creating new metadata

Use `create_new_metadata()` to create an empty metadata object.

The following example creates a new metadata object, populates it with raster and swath information, and writes both the
metadata and raster data to disk:

```python
import numpy as np

from perseo_core.timing import PreciseDateTime

from aresys_io.product import (
    create_new_metadata,
    metadata,
    write_metadata,
    write_raster_with_raster_info,
)

path_to_new_metadata = ...

# Create a new, empty metadata object.
new_metadata = create_new_metadata(
    num_metadata_channels=1,
    description="New metadata test",
)

# Create the raster information.
raster_info = metadata.RasterInfo(
    lines=8951,
    samples=2215,
    cell_type="FLOAT32",
    file_name="GRD_0001",
    header_offset_bytes=150,
    row_prefix_bytes=20,
    byteorder="LITTLEENDIAN",
    invalid_value=None,
    format_type=None,
)

# Create the swath information.
swath_info = metadata.SwathInfo(
    swath="S1",
    polarization="HV",
    acquisition_start_time=PreciseDateTime.now(),
)

# Add the information to the metadata object.
new_metadata.insert_element(raster_info)
new_metadata.insert_element(swath_info)

# Write the metadata to disk.
write_metadata(
    metadata_obj=new_metadata,
    metadata_file=path_to_new_metadata,
)

# Write the raster data to disk.
write_raster_with_raster_info(
    ch16_raster_path,
    np.zeros((8951, 2215)),
    raster_info,
)
```

## Metadata channels

A `MetaData` object contains a list of `MetaDataChannel` objects. The list can be accessed through the `channels` property.

For convenience, when accessing or modifying metadata directly through the `MetaData` object, the operation is performed
on the **first metadata channel** (`channels[0]`). This is particularly useful because most products contain only one
metadata channel.

The individual metadata channels can be accessed and modified either through the `channels` property or using the `[]`
operator:

```python
mtd.channels[1]
```

is equivalent to:

```python
mtd[1]
```

Similarly, the following:

```python
mtd.raster_info
```

is equivalent to:

```python
mtd[0].raster_info
```

or:

```python
mtd.channels[0].raster_info
```

This means that code written for products containing a single metadata channel can use the convenient top-level properties,
while products containing multiple metadata channels can explicitly access each channel when needed.

### Verifying Metadata Element Existence

To check whether a metadata element is present inside a `MetaDataChannel` object, you can use the ``in`` python keyword.

```python
if "RasterInfo" in mtd:
    print("raster_info is present")
```

For convenience, when checking the existence of a metadata element in a `MetaData` object, the operation is performed
on the **first metadata channel** (`channels[0]`).

This operation is particularly useful when working with multiple metadata elements, as it allows you to check whether
a specific element is present in the metadata without raising a `RuntimeError` exception if the requested element is not
present.

```python
if "AntennaInfo" not in channel_mtd:
    channel_mtd.antenna_info
```

This results in:

```bash
RuntimeError: The element AntennaInfo is not available in the current metadata channel
```

### Creating multiple metadata channels

You can create a `MetaData` object containing multiple metadata channels by specifying the desired number with `create_new_metadata()`.

For example, the following creates a metadata object containing two metadata channels, which can be useful for products
such as bistatic data:

```python
import numpy as np

from perseo_core.timing import PreciseDateTime

from aresys_io.product import (
    create_new_metadata,
    metadata,
    write_metadata,
    write_raster_with_raster_info,
)

path_to_new_metadata = ...

# Create a metadata object containing two metadata channels.
new_metadata = create_new_metadata(
    num_metadata_channels=2,
    description="New metadata test",
)

# Create the raster information.
raster_info = metadata.RasterInfo(
    lines=8951,
    samples=2215,
    cell_type="FLOAT32",
    file_name="GRD_0001",
    header_offset_bytes=150,
    row_prefix_bytes=20,
    byteorder="LITTLEENDIAN",
    invalid_value=None,
    format_type=None,
)

# Create the swath information.
swath_info = metadata.SwathInfo(
    swath="S1",
    polarization="HV",
    acquisition_start_time=PreciseDateTime.now(),
)

# Add the raster and swath information to the first metadata channel.
new_metadata.insert_element(raster_info)
new_metadata.insert_element(swath_info)

# Set the content ID of the second metadata channel.
new_metadata[1].content_id = "Tx"

# Add swath information to the second metadata channel.
new_metadata[1].insert_element(swath_info)
```

In this example:

- `new_metadata[0]` refers to the first metadata channel.
- `new_metadata[1]` refers to the second metadata channel.
- `new_metadata.channels` provides direct access to the complete list of metadata channels.
- `new_metadata[1].content_id = "Tx"` assigns a content identifier to the second channel.

You can therefore work with individual metadata channels when a product contains multiple channels, while retaining the
simpler top-level interface for single-channel products.
