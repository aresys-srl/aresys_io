# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Product folder channel iteration utilities."""

from collections.abc import Callable, Iterator

from aresys_io.product.metadata.channel import MetaData
from aresys_io.product.metadata.elements import SwathPolarization
from aresys_io.product.metadata.io import read_metadata
from aresys_io.product.pf.product_folder import ProductFolder

__all__ = ["iter_channels", "iter_channels_generator"]


MetaDataFilter = Callable[[MetaData], bool]


class SwathIDFilter:
    """SwathID filtering class."""

    def __init__(
        self,
        polarization: SwathPolarization | list[SwathPolarization] | None = None,
        swath: str | None = None,
    ) -> None:
        """Filter metadata file searching for the selected polarization and/or swath.

        Parameters
        ----------
        polarization : SwathPolarization | list[SwathPolarization] | None, optional
            polarizations to be filtered, it can be a single value or a list of polarizations,
            by default None
        swath : str | None, optional
            swath name to be filtered, by default None.

        Raises
        ------
        RuntimeError
            if both filtering fields are not defined
        """
        if polarization is None and swath is None:
            msg = "No filtering fields have been defined"
            raise RuntimeError(msg)

        if not isinstance(polarization, list) and polarization is not None:
            polarization = [polarization]

        self.polarization = polarization
        self.swath = swath

    def __call__(self, metadata: MetaData) -> bool:
        """Filter out the input metadata file to match the polarization and/or swath name.

        Parameters
        ----------
        metadata : MetaData
            metadata object to be checked

        Returns
        -------
        bool
            boolean matching result
        """
        swath_info = metadata.swath_info
        if self.polarization is not None:
            pol_condition = swath_info.polarization in self.polarization
            if self.swath is not None:
                sw_condition = swath_info.swath == self.swath
                return pol_condition and sw_condition

            return pol_condition

        assert self.swath is not None
        return swath_info.swath == self.swath


def iter_channels_generator(
    product: ProductFolder,
    filter_func: MetaDataFilter | None = None,
) -> Iterator[tuple[int, MetaData]]:
    """Channel iteration generator that yields channel id and channel metadata.

    If a filter MetaDataFilter-like function is provided, the output yielded is restricted only
    to channels matching the filtering conditions.

    Parameters
    ----------
    product : ProductFolder
        product folder from which to get the channels
    filter_func : MetaDataFilter | None, optional
        filtering MetaDataFilter-like function, by default None

    Yields
    ------
    Iterator[Tuple[int, MetaData]]
        channel id,
        channel metadata object
    """
    for ch_index in product.channel_ids:
        metadata = read_metadata(product.channel_metadata_path(ch_index))

        if filter_func is None or filter_func(metadata):
            yield ch_index, metadata


def iter_channels(
    product: ProductFolder,
    polarization: SwathPolarization | list[SwathPolarization] | None = None,
    swath: str | None = None,
) -> Iterator[tuple[int, MetaData]]:
    """Channels iterator with optional SwathID filter pre-configured.

    Parameters
    ----------
    product : ProductFolder
        product folder from which to get the channels
    polarization : SwathPolarization | list[SwathPolarization] | None, optional
        polarizations to be filtered, it can be a single value or a list of polarizations,
        by default None
    swath : str | None, optional
        swath name to be filtered, by default None

    Yields
    ------
    Iterator[Tuple[int, MetaData]]
        channel id,
        channel metadata object
    """
    filtering = None
    if polarization is not None or swath is not None:
        filtering = SwathIDFilter(polarization=polarization, swath=swath)

    yield from iter_channels_generator(product=product, filter_func=filtering)
