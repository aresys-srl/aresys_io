# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Parsing.

Numpy scalar types (float32, float64, int32, int64) are supported in both
parsing and serialization.  When serializing, values assigned to XML ``int``
fields are always written as plain integers (e.g. ``7``, never ``7.0``);
assigning a float with a fractional part to an ``int`` field raises
``ValueError``.  Values assigned to XML ``float`` fields are written using
their natural float representation.
"""

from typing import Any, TypeVar

import numpy as np
import xsdata.exceptions
from xsdata.formats.converter import Converter, converter
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

__all__ = ["parse", "serialize"]


def _float_to_int_lossless(value: float) -> int:
    """Convert a float to int, raising ValueError if there is any loss of precision."""
    int_value = int(value)
    if int_value != value:
        msg = f"Cannot losslessly convert {value!r} to int: fractional part would be lost"
        raise ValueError(msg)
    return int_value


# DEV NOTE: two separate mechanisms are used to support numpy types during serialization.
# _NumpyConverter (below) handles *type registration*: xsdata's converter dispatch is
# value-type-based, so it never sees numpy scalars unless they are explicitly registered.
# However, at converter level the declared XML field type is not available, so the
# converter cannot distinguish "np.float64 in a float field" from "np.float64 in an int
# field".  That distinction is handled by _NormalizedXmlSerializer.encode_primitive
# (below), which runs before converter dispatch and has access to var.types.  The two
# mechanisms cannot be merged: _NumpyConverter cannot see the field type;
# encode_primitive cannot register new value types.
class _NormalizedXmlSerializer(XmlSerializer):
    """XmlSerializer that coerces float values assigned to int-typed fields."""

    @classmethod
    def encode_primitive(cls, value: Any, var: Any) -> Any:  # ruff: ignore[any-type]
        if int in var.types and isinstance(value, (float, np.floating)):
            value = _float_to_int_lossless(float(value))
        return super().encode_primitive(value, var)


_CONTEXT = XmlContext()
_PARSER_CONFIGURATION = ParserConfig(fail_on_converter_warnings=True)
_PARSER = XmlParser(context=_CONTEXT, config=_PARSER_CONFIGURATION)
_SERIALIZER_CONFIGURATION = SerializerConfig(indent="  ", encoding="utf-8")
_SERIALIZER = _NormalizedXmlSerializer(context=_CONTEXT, config=_SERIALIZER_CONFIGURATION)

ModelT = TypeVar("ModelT")


class _NumpyConverter(Converter):
    """Converter that normalizes numpy scalar values through a native XML type."""

    def __init__(self, numpy_type: type, xml_type: type) -> None:
        self._numpy_type = numpy_type
        self._xml_type = xml_type
        self._xml_converter = converter.type_converter(xml_type)

    def deserialize(self, value: Any, **kwargs) -> Any:  # ruff: ignore[missing-type-kwargs, any-type]
        parsed_value = self._xml_converter.deserialize(value, **kwargs)
        return self._numpy_type(parsed_value)

    def serialize(self, value: Any, **kwargs) -> str:  # ruff: ignore[missing-type-kwargs, any-type]
        return self._xml_converter.serialize(self._xml_type(value), **kwargs)


converter.register_converter(np.float32, _NumpyConverter(np.float32, float))
converter.register_converter(np.float64, _NumpyConverter(np.float64, float))
converter.register_converter(np.int32, _NumpyConverter(np.int32, int))
converter.register_converter(np.int64, _NumpyConverter(np.int64, int))


def parse(xml_string: str, model: type[ModelT]) -> ModelT:
    """Parse a string according to an XSD model.

    Parameters
    ----------
    xml_string : str
        input xml string to parse
    model : Type
        xsd model type

    Returns
    -------
    ModelT
        The content as a structure of type model

    Raises
    ------
    RuntimeError
        in case the xml_string is incompatible with the XSD model
    """
    try:
        model_obj = _PARSER.from_string(xml_string, model)
    except xsdata.exceptions.ParserError as exc:
        msg = "Parsing error"
        raise RuntimeError(msg) from exc
    except TypeError as exc:
        msg = "Parsing error"
        raise RuntimeError(msg) from exc

    return model_obj


def serialize(model: Any, **kwargs) -> str:  # ruff: ignore[missing-type-kwargs, any-type]
    """Serialize an XSD object to a string.

    Parameters
    ----------
    model :
        Object to serialize

    kwargs are forwarded to serializer render method

    Returns
    -------
    str
        XML string
    """
    return _SERIALIZER.render(model, **kwargs)
