# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for aresys_io.core.parsing."""

from dataclasses import dataclass, field

import numpy as np
import pytest

from aresys_io.core.parsing import parse, serialize


@dataclass(kw_only=True)
class IntXmlModel:
    """Minimal XML model in xsdata-generated style."""

    class Meta:
        name = "IntXmlModel"

    value: int = field(metadata={"name": "Value", "type": "Element", "namespace": ""})
    label: str = field(metadata={"name": "Label", "type": "Element", "namespace": ""})


@dataclass(kw_only=True)
class FloatXmlModel:
    """Minimal XML model in xsdata-generated style with float content."""

    class Meta:
        name = "FloatXmlModel"

    value: float = field(metadata={"name": "Value", "type": "Element", "namespace": ""})
    label: str = field(metadata={"name": "Label", "type": "Element", "namespace": ""})


def test_parse_simple_xml_model() -> None:
    xml = "<IntXmlModel><Value>42</Value><Label>ok</Label></IntXmlModel>"

    parsed = parse(xml, IntXmlModel)

    assert parsed == IntXmlModel(value=42, label="ok")


def test_parse_simple_xml_model_from_float_raises() -> None:
    xml = "<IntXmlModel><Value>42.0</Value><Label>ok</Label></IntXmlModel>"

    with pytest.raises(RuntimeError, match="Parsing error"):
        parse(xml, IntXmlModel)


def test_parse_wrong_content_raises_runtime_error() -> None:
    xml = "<IntXmlModel><Value>not_an_int</Value><Label>ok</Label></IntXmlModel>"

    with pytest.raises(RuntimeError, match="Parsing error"):
        parse(xml, IntXmlModel)


def test_parse_wrong_tag_name_raises_runtime_error() -> None:
    xml = "<IntXmlModel><1Value>42</1Value><Label>ok</Label></IntXmlModel>"

    with pytest.raises(RuntimeError, match="Parsing error"):
        parse(xml, IntXmlModel)


def test_parse_missing_field_raises_error() -> None:
    xml = "<IntXmlModel><Value>42</Value></IntXmlModel>"

    with pytest.raises(RuntimeError, match="Parsing error"):
        parse(xml, IntXmlModel)


def test_parse_non_closed_tag_raises_runtime_error() -> None:
    xml = "<IntXmlModel><Value>42</Value><Unclosed></IntXmlModel>"

    with pytest.raises(RuntimeError, match="Parsing error"):
        parse(xml, IntXmlModel)


def test_parse_float_field_returns_python_float_not_numpy_float64() -> None:
    xml = "<FloatXmlModel><Value>7.0</Value><Label>ok</Label></FloatXmlModel>"

    parsed = parse(xml, FloatXmlModel)

    assert isinstance(parsed.value, float)
    assert not isinstance(parsed.value, np.float64)
    assert parsed.value == 7.0  # ruff: ignore[float-equality-comparison]


@pytest.mark.parametrize(
    ("numpy_type", "xml_value", "expected_value"),
    [
        pytest.param(np.float32, "7.0", np.float32(7.0), id="float32"),
        pytest.param(np.float64, "8.0", np.float64(8.0), id="float64"),
        pytest.param(np.int32, "9", np.int32(9), id="int32"),
        pytest.param(np.int64, "10", np.int64(10), id="int64"),
    ],
)
def test_parse_numpy_typed_field_returns_expected_numpy_scalar(
    numpy_type: type,
    xml_value: str,
    expected_value: np.generic,
) -> None:
    @dataclass(kw_only=True)
    class ModelWithNumpyValue:
        class Meta:
            name = "ModelWithNumpyValue"

        value: numpy_type = field(metadata={"name": "Value", "type": "Element", "namespace": ""})

    xml = f"<ModelWithNumpyValue><Value>{xml_value}</Value></ModelWithNumpyValue>"

    parsed = parse(xml, ModelWithNumpyValue)

    assert isinstance(parsed.value, numpy_type)
    assert parsed.value == expected_value


def test_serialize_simple_xml_model() -> None:
    model = IntXmlModel(value=7, label="hello")

    xml = serialize(model)

    assert "<IntXmlModel>" in xml
    assert "<Value>7</Value>" in xml
    assert "<Label>hello</Label>" in xml


@pytest.mark.parametrize(
    ("value", "expected_value"),
    [
        pytest.param(np.int32(7), "7", id="numpy-int32"),
        pytest.param(np.int64(8), "8", id="numpy-int64"),
        pytest.param(7.0, "7", id="python-float"),
        pytest.param(np.float32(7.0), "7", id="numpy-float32"),
        pytest.param(np.float64(7.0), "7", id="numpy-float64"),
    ],
)
def test_serialize_int_field_supports_python_and_numpy_scalars(
    value: float | np.generic,
    expected_value: str,
) -> None:
    model = IntXmlModel(value=value, label="hello")  # pyrefly: ignore[bad-argument-type]

    xml = serialize(model)

    assert "<IntXmlModel>" in xml
    assert f"<Value>{expected_value}</Value>" in xml
    assert "<Label>hello</Label>" in xml


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(7.1, id="python-float-fractional"),
        pytest.param(np.float32(7.1), id="numpy-float32-fractional"),
        pytest.param(np.float64(7.1), id="numpy-float64-fractional"),
    ],
)
def test_serialize_int_field_fractional_float_raises(value: float | np.generic) -> None:
    model = IntXmlModel(value=value, label="hello")  # pyrefly: ignore[bad-argument-type]

    with pytest.raises(ValueError, match="Cannot losslessly convert"):
        serialize(model)


def test_serialize_simple_xml_model_with_numpy_float32_string_field() -> None:
    model = IntXmlModel(value=7, label=np.float32(3.0))  # pyrefly: ignore[bad-argument-type]

    xml = serialize(model)

    assert "<IntXmlModel>" in xml
    assert "<Value>7</Value>" in xml
    assert "<Label>3.0</Label>" in xml


@pytest.mark.parametrize(
    ("value", "expected_value"),
    [
        pytest.param(np.float32(6.0), "6.0", id="numpy-float32"),
        pytest.param(np.float64(7.0), "7.0", id="numpy-float64"),
        pytest.param(np.int32(7), "7", id="numpy-int32"),
        pytest.param(np.int64(8), "8", id="numpy-int64"),
    ],
)
def test_serialize_float_field_supports_python_and_numpy_scalars(
    value: float | np.generic,
    expected_value: str,
) -> None:
    model = FloatXmlModel(value=value, label="hello")  # pyrefly: ignore[bad-argument-type]

    xml = serialize(model)

    assert "<FloatXmlModel>" in xml
    assert f"<Value>{expected_value}</Value>" in xml
    assert "<Label>hello</Label>" in xml
