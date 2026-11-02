# Migrating from ArePyTools

This guide maps the current ArePyTools I/O workflow (the `ProductFolder2`-based API introduced in ArePyTools 1.6) to `aresys_io`. It focuses on APIs currently provided by `aresys_io`; it is not a complete replacement map for every module in ArePyTools.

> [!IMPORTANT]
> `aresys_io` is **not a drop-in replacement**. The distribution and import names change, module paths and several method signatures change, and not every ArePyTools feature has an equivalent here. Migrate and test each workflow explicitly rather than relying on a global import rename.

## Migrating the ArePyTools I/O workflow

The migration is primarily a change in package and API boundaries.

### Module map

| ArePyTools I/O module | `aresys_io` entry point | Migration note |
| --- | --- | --- |
| `arepytools.io.productfolder2` | `aresys_io.product` | `ProductFolder2` is now `ProductFolder`; use `open_product_folder()` / `create_product_folder()`. |
| `arepytools.io.channel_iteration` | `aresys_io.product` | `iter_channels()` remains, yielding channel IDs and metadata. |
| `arepytools.io.metadata` | `aresys_io.product` | Metadata element models, fields, and value types have changed. |
| `arepytools.io.io_support` | Metadata-aware helpers in `aresys_io.product` | Prefer `read_raster_with_raster_info()` and `write_raster_with_raster_info()` for normal Product Folder workflows. Low-level core functions remain available for specialized use. |
| `arepytools.io.point_target_binary` | `aresys_io.product` | Binary point-target workflows remain, with changed argument types and error behavior. |
| `arepytools.io.point_target_file` | Removed | Support for the separate point-target XML format was removed because the format is considered obsolete. |

The normal Product Folder workflow is path-based: open or create the folder, obtain channel paths, and explicitly call metadata/raster functions. The folder object does not keep a read/write mode that controls those operations. Channel IDs are the identifiers in the product filenames (for example, `1` and `16`), not zero-based positions in an in-memory list.

### Open a product and read its channels

The same task in the current ArePyTools workflow and `aresys_io` looks like this:

```python
# ArePyTools 1.6+ I/O API
from arepytools.io import iter_channels, open_product_folder, read_raster_with_raster_info

product = open_product_folder(product_path)
channel_ids = product.get_channels_list()

for channel_id, channel_metadata in iter_channels(product):
    raster = read_raster_with_raster_info(
        raster_file=product.get_channel_data(channel_id),
        raster_info=channel_metadata.get_raster_info(),
    )
```

```python
# aresys_io
from aresys_io.product import iter_channels, open_product_folder, read_raster_with_raster_info

product = open_product_folder(product_path)
channel_ids = product.channel_ids

for channel_id, channel_metadata in iter_channels(product):
    raster = read_raster_with_raster_info(
        raster_file=product.channel_data_path(channel_id),
        raster_info=channel_metadata.raster_info,
    )
```

Filtering with `iter_channels()` is still supported. For example, the new polarization values are string literals such as `"HH"` and `"VV"` (rather than ArePyTools enum members or values such as `"H/H"`); the `swath` filter remains a string.

### Write metadata and raster data

When copying a channel to a new channel ID, update the metadata field that names the raster and write the metadata and raster explicitly. In `aresys_io`, `RasterInfo.file_name` replaces the old `filename` field, while raster I/O remains metadata-aware:

```python
from aresys_io.product import read_metadata, write_metadata, write_raster_with_raster_info

source_id = 3
destination_id = 9
metadata = read_metadata(product.channel_metadata_path(source_id))
data = read_raster_with_raster_info(
    raster_file=product.channel_data_path(source_id),
    raster_info=metadata.raster_info,
)

metadata.raster_info.file_name = product.channel_data_path(destination_id).name
write_metadata(
    metadata_obj=metadata,
    metadata_file=product.channel_metadata_path(destination_id),
)
write_raster_with_raster_info(
    raster_file=product.channel_data_path(destination_id),
    data=data,
    raster_info=metadata.raster_info,
)
```

For new metadata, `create_new_metadata()` and `insert_element()` remain available, but construct elements with the current model's field names and values. See the [metadata section](#3-metadata-model-and-xml-io) for an example.

### Quick comparison

| ArePyTools 1.6+ API | `aresys_io` API |
| --- | --- |
| `open_product_folder(path)` | `open_product_folder(path)` |
| `product.get_channels_list()` | `product.channel_ids` |
| `product.get_channel_metadata(channel_id)` | `product.channel_metadata_path(channel_id)` |
| `product.get_channel_data(channel_id)` | `product.channel_data_path(channel_id)` |
| `metadata.get_raster_info()` | `metadata.raster_info` |
| `read_raster_with_raster_info(file, raster_info)` | Same operation; update import and use the new metadata model. |
| `write_metadata(metadata_obj, metadata_file)` | Same operation; update metadata fields and values as needed. |
| `write_raster_with_raster_info(file, data, raster_info)` | Same operation; metadata-aware write offset is now `write_offset`. |
| `iter_channels(product, polarization="H/H")` | `iter_channels(product, polarization="HH")` |

The detailed sections below document the behavior and compatibility changes by functional area. The deprecated ArePyTools `channel.Channel` and legacy `productfolder.ProductFolder` classes are not the source API for this workflow; see [I/O functionality without a direct replacement](#7-io-functionality-without-a-direct-replacement) for those legacy abstractions.

### Enum values

Enums have been removed from the Product Metadata API: fixed-choice metadata fields now use string literals. For example, replace the old `EPolarization.hh` channel filter with the literal `"HH"`:

```python
# ArePyTools
from arepytools.io.metadata import EPolarization

for channel_id, channel_metadata in iter_channels(
    product,
    polarization=EPolarization.hh,
):
    ...

# aresys_io
for channel_id, channel_metadata in iter_channels(
    product,
    polarization="HH",
):
    ...
```

The same enum-to-literal change applies to the dataset's looking direction. `DataSetInfo.side_looking` now accepts `"RIGHT"` or `"LEFT"`:

```python
# ArePyTools
dataset_info.side_looking = ESideLooking.right_looking

# aresys_io
dataset_info.side_looking = "RIGHT"
```

Enums remain in the SAR System API, including `aresys_io.sarsystem.AttitudeType` and `OrbitDirection`. Use string values for metadata fields and enum types where the SAR System API expects them.

### Exception handling

Exception types can also differ. Some specialized ArePyTools exceptions are replaced by built-in exceptions such as `ValueError` or `RuntimeError` in `aresys_io`; the exact type depends on the operation. Review `try`/`except` blocks and update them to catch the documented exceptions, rather than assuming old custom exception classes remain available.

## 2. Product Folder

The replacement object is `ProductFolder` rather than `ProductFolder2`. Its accessors are properties or path-oriented methods, rather than the old `get_*` methods.

| ArePyTools | `aresys_io` |
| --- | --- |
| `ProductFolder2.pf_name` | `ProductFolder.name` |
| `get_channels_list()` | `channel_ids` |
| `get_channel_data(channel_id)` | `channel_data_path(channel_id)` |
| `get_channel_metadata(channel_id)` | `channel_metadata_path(channel_id)` |
| `arepytools.io.get_channel_quicklook(product, ext, channel_id)` | `product.channel_quicklook_path(ext, channel_id)` |
| `get_config_file()` | `config_path` |
| `get_overlay_file()` | `overlay_path` |

A typical access pattern becomes:

```python
# ArePyTools
from arepytools.io import create_product_folder, read_metadata

product = create_product_folder(product_path)
raster_path = product.get_channel_data(1)
metadata = read_metadata(product.get_channel_metadata(1))
raster_info = metadata.get_raster_info()
```

```python
# aresys_io
from aresys_io.product import create_product_folder, read_metadata

product = create_product_folder(product_path)
raster_path = product.channel_data_path(1)
metadata = read_metadata(product.channel_metadata_path(1))
raster_info = metadata.raster_info
```

`create_product_folder()` is still available. Its description argument is now named `description`; `description` and `overwrite_ok` are keyword-only. Raster extensions are string literals (for example, `""` and `".tiff"`) rather than `RasterExtensions` enum members. Review code that depends on specialized Product Folder exceptions; those failure cases are generally represented by built-in exceptions such as `RuntimeError` in the new API.

## 3. Metadata model and XML I/O

The metadata format is still read and written as XML, and the common functions `create_new_metadata()`, `read_metadata()`, and `write_metadata()` remain available. The in-memory API has changed: metadata elements are Pydantic models, and `MetaData` contains channels accessed by index. The former channel-append and metadata-channel-list workflow is not source-compatible.

| ArePyTools pattern | `aresys_io` pattern |
| --- | --- |
| `metadata.get_raster_info()` | `metadata.raster_info` (first channel) |
| Access another channel's raster info | `metadata[index].raster_info` |
| `RasterInfo(filename=..., celltype=..., byteorder=...)` | `RasterInfo(file_name=..., cell_type=..., byte_order=...)` |
| `set_lines_axis(...)` / `set_samples_axis(...)` | Assign the corresponding `lines_*` / `samples_*` fields directly. |
| Construct a metadata element and populate required fields later | Pass all required fields when constructing that element. |
| Enum-backed values | String literals validated by the model |

### Required model fields and raster axes

> [!IMPORTANT]
> In the new metadata models, every field without a default is required at construction. This applies across element types, not only `DataSetInfo`: an old workflow that created an empty element and populated it afterward will fail if required constructor fields were omitted. Check the current model fields for each element and provide actual product values; do not invent placeholders for missing metadata.

For example, `DataSetInfo` requires the following fields at construction. The values below are illustrative; substitute values from the actual product:

```python
from aresys_io.product.metadata import DataSetInfo

dataset_info = DataSetInfo(
    sensor_name="SENSOR",
    description="Example product",
    acquisition_mode="MODE",
    image_type="IMAGE_TYPE",
    projection="PROJECTION",
    acquisition_station="STATION",
    processing_center="CENTER",
    processing_software="SOFTWARE",
    fc_hz=5.405e9,
    side_looking="RIGHT",
)
```

The required `DataSetInfo` fields are `sensor_name`, `description`, `acquisition_mode`, `image_type`, `projection`, `acquisition_station`, `processing_center`, `processing_software`, `fc_hz`, and `side_looking`. Other fields may remain optional according to the current model. Fixed-choice values such as `side_looking` are strings, not enum members.

`SwathInfo` is another example: its `swath`, `polarization`, and `acquisition_start_time` fields must be supplied, while fields with defaults can be omitted:

```python
from aresys_io.product.metadata import SwathInfo

swath_info = SwathInfo(
    swath="IW1",
    polarization="VV",
    acquisition_start_time=acquisition_start_time,  # a PreciseDateTime value
)
```

`RasterInfo.set_lines_axis()` and `set_samples_axis()` were also removed. Set the axis fields directly, preserving the corresponding values and units:

```python
raster_info.lines_start = lines_start
raster_info.lines_start_unit = lines_start_unit
raster_info.lines_step = lines_step
raster_info.lines_step_unit = lines_step_unit

raster_info.samples_start = samples_start
raster_info.samples_start_unit = samples_start_unit
raster_info.samples_step = samples_step
raster_info.samples_step_unit = samples_step_unit
```

For example:

```python
from aresys_io.product import create_new_metadata, metadata, write_metadata

md = create_new_metadata(num_metadata_channels=1, description="Example")
md.insert_element(
    metadata.RasterInfo(
        lines=100,
        samples=200,
        cell_type="FLOAT32",
        file_name="Channel_1",
        byte_order="LITTLEENDIAN",
    )
)
write_metadata(metadata_obj=md, metadata_file="Channel_1.xml")
```

Check every renamed field when constructing metadata elements. Values can also change representation: for example, polarization strings use values such as `"HH"` rather than legacy forms such as `"H/H"`. Use the literal values accepted by the current element model and validate existing XML with representative products.

## 4. Raster I/O

For normal Product Folder workflows, use the metadata-aware helpers rather than low-level core raster functions. The `RasterInfo` associated with a channel provides the dimensions, data type, byte order, and file-layout details needed to read or write its raster.

```python
from aresys_io.product import (
    read_metadata,
    read_raster_with_raster_info,
    write_raster_with_raster_info,
)

channel_metadata = read_metadata(product.channel_metadata_path(channel_id))
raster_info = channel_metadata.raster_info
raster_path = product.channel_data_path(channel_id)

data = read_raster_with_raster_info(
    raster_file=raster_path,
    raster_info=raster_info,
)

write_raster_with_raster_info(
    raster_file=output_path,
    data=data,
    raster_info=raster_info,
)
```

`read_raster_with_raster_info()` also accepts `block_to_read` when only a raster window is needed. For partial writes, `write_raster_with_raster_info()` accepts `write_offset`. Direct use of `aresys_io.core.raster_io` and `DataLayout` is intended for specialized cases where the metadata-aware helpers are not suitable.

> [!NOTE]
> If calling low-level `read_raster()` or `write_raster()` directly, replace the legacy separate layout arguments with a `DataLayout` passed as `data_layout=`.

## 5. Point-target binary products

The binary point-target workflow remains close to the old API. `PointSetProduct` still accepts an `open_mode`, writes coordinates and RCS arrays, and supports subset and memory-mapped reads. The main migration work is updating imports, type arguments, and exception handling.

```python
from aresys_io.product import PointSetProduct

product = PointSetProduct(product_path, open_mode="w")
product.write_data(
    coords=coords,  # shape (N, 3)
    rcs=rcs,  # shape (N, 4)
    coords_data_type="FLOAT64",
    rcs_data_type="FLOAT_COMPLEX",
)
```

The data-type arguments are string literals (such as `"FLOAT64"` and `"FLOAT_COMPLEX"`), not legacy `ECellType` values. `NominalPointTarget` and `convert_array_to_point_target_structure()` are available from `aresys_io.product` (and the dedicated point-target modules). Specialized legacy exceptions may now be `ValueError` or `RuntimeError`.

The separate ArePyTools point-target XML functions `read_point_targets_file()` and `write_point_targets_file()` do **not** have a direct equivalent in the current `aresys_io` API. Do not treat `PointSetProduct` as a replacement for that XML workflow; plan a separate migration for it.

## 6. SAR-system files

Trajectory, timeline, swath-table, and satellite-table read/write functionality is available under `aresys_io.sarsystem`, and many function names are retained. Update imports and review keyword names and destination-path semantics before changing call sites.

| API | Migration note |
| --- | --- |
| `read_trajectory()`, `read_timeline_table()`, `read_swath_table()`, `read_sat_table()` | Names are retained; check keyword parameter names and return types. |
| `write_timeline_table_xml()` | The current `file` argument is the output file path; pass a path such as `folder / "TimeLineTable.xml"`. The legacy API took a directory and generated that filename. The current writer does not create missing parent directories. |
| `write_trajectory_xml()` | The current `filename` argument is the output XML path or a directory (which defaults to `Trajectory.xml`). The legacy API took `xml_dir_path` plus an optional `filename` basename; update keyword and positional calls accordingly. |
| `write_swath_table_xml()` | Still takes a destination directory. |
| `read_sat_table()` | Keyword names are now `sar_system_folder_name` and `acq_mode_id` (formerly `SARSystem_folder_name` and `acq_mode_ID`). |

Do not assume XML output is byte-for-byte identical just because a read/write function has the same name. Compare parsed content and validate outputs with the consuming application.

## 7. I/O functionality without a direct replacement

Most core I/O tasks have a replacement. Support for the separate point-target XML format was removed because the format is considered obsolete; there is no replacement for this workflow in `aresys_io`.

- **Point-target XML files:** The ArePyTools functions `arepytools.io.point_target_file.read_point_targets_file()` and `write_point_targets_file()` handled the separate point-target XML format. Support for this format was removed because it is considered obsolete. The Point Target **Binary** product remains supported, but it is a different format and does not replace the XML workflow.
- **Deprecated classes:** `arepytools.io.channel.Channel` and `arepytools.io.productfolder.ProductFolder` have no counterparts in `aresys_io`.

This list is about missing direct APIs, not every old import path. For example, generic XML parsing/serialization, binary debug reading, raster I/O, metadata XML I/O, and SAR-system file I/O are available in `aresys_io` under reorganized or changed APIs, as described above.

## 8. Geometry, timing, and math

Most of ArePyTools' geometry, timing, and math functionality has been migrated to the separate `perseo-core` package. When state vectors are held in a metadata object, replace `arepytools.io.create_orbit(state_vectors)` with `metadata.trajectory()`. It returns a PERSEO Core `CubicSplineTrajectory`, rather than the legacy `Orbit`, so update downstream code to the new trajectory API.

This is the general pattern for metadata-backed computations: the metadata elements remain the serialized product representation, while convenience methods build computational objects from them. For example, `metadata.attitude()` returns a PERSEO Core `Attitude`, and `metadata.doppler_centroid_poly()` returns a piecewise polynomial that can be evaluated:

```python
trajectory = metadata.trajectory()
attitude = metadata.attitude()
doppler_centroid = metadata.doppler_centroid_poly()
doppler_value = doppler_centroid.evaluate(
    azimuth_value=azimuth_time,
    range_values=range_time,
)
```

Here, `azimuth_time` is a `PreciseDateTime` and `range_time` is a range coordinate in the units used by the metadata. These methods on `MetaData` use its first metadata channel; use the corresponding channel's methods when working with another channel.

The old `create_orbit_from_trajectory()` helper has no named counterpart in `aresys_io`; migrate that conversion and subsequent geometry operations using the PERSEO Core migration guide.

## 9. Suggested migration checklist

1. Inventory all `arepytools` imports, including geometry, math, timing, and point-target XML usage.
2. Migrate geometry, timing, and math imports using the PERSEO Core migration guide; migrate I/O imports using this guide. Do not apply a blanket package-name substitution.
3. Update Product Folder methods and property access.
4. Migrate metadata construction, channel selection, field names, and enum/string values.
5. Review SAR-system writer path conventions and renamed keyword arguments.
6. Check exception handling, validation behavior, and dependency/runtime constraints.
7. Run the application tests against representative existing products and compare parsed metadata and raster values.

## Further reading

- [Installation](install.md)
- [Product Folder quickstart](documentation/product_folder/quickstart.md)
- [Point Target quickstart](documentation/point_target/quickstart.md)
- [SAR System documentation](documentation/sarsystem/index.md)
