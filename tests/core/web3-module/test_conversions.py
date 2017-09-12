# coding=utf-8

from __future__ import unicode_literals

import pytest
import sys

from web3 import Web3


@pytest.mark.parametrize(
    'val, expected',
    (
        (0x01, b'\x01'),
        (0xFF, b'\xff'),
        (0, b'\x00'),
        (256, b'\x01\x00'),
        (True, b'\x01'),
        (False, b'\x00'),
    )
)
def test_to_bytes_primitive(val, expected):
    assert Web3.toBytes(val) == expected


@pytest.mark.parametrize(
    'val, expected',
    (
        ('0x', b''),
        ('0x0', b'\x00'),
        ('0x1', b'\x01'),
        ('0', b'\x00'),
        ('1', b'\x01'),
        ('0xFF', b'\xff'),
        ('0x100', b'\x01\x00'),
        ('0x0000', b'\x00\x00'),
    )
)
def test_to_bytes_hexstr(val, expected):
    assert Web3.toBytes(hexstr=val) == expected


@pytest.mark.parametrize(
    'val, expected',
    (
        ('cowmö', b'cowm\xc3\xb6'),
        ('', b''),
    )
)
def test_to_bytes_text(val, expected):
    assert Web3.toBytes(text=val) == expected


@pytest.mark.parametrize(
    'val, expected',
    (
        (b'', ''),
        ('0x', ''),
        (b'cowm\xc3\xb6', 'cowmö'),
        ('0x636f776dc3b6', 'cowmö'),
        (0x636f776dc3b6, 'cowmö'),
    )
)
def test_to_text(val, expected):
    if sys.version_info.major < 3:
        with pytest.raises(NotImplementedError):
            Web3.toText(val)
    else:
        assert Web3.toText(val) == expected


@pytest.mark.parametrize(
    'val, expected',
    (
        (b'\x00', 0),
        (b'\x01', 1),
        (b'\x00\x01', 1),
        (b'\x01\x00', 256),
        ('255', 255),
        (True, 1),
        (False, 0),
        # Deprecated:
        ('0x0', 0),
        ('0x1', 1),
        ('0x01', 1),
        ('0x10', 16),
    )
)
def test_to_decimal(val, expected):
    if isinstance(val, bytes) and bytes == str:
        pytest.skip("Python 3 is required to pass in bytes")
    assert Web3.toDecimal(val) == expected


@pytest.mark.parametrize(
    'val, expected',
    (
        ('0x0', 0),
        ('0x1', 1),
        ('0x01', 1),
        ('0x10', 16),
        ('0', 0),
        ('1', 1),
        ('01', 1),
        ('10', 16),
    )
)
def test_to_decimal_hexstr(val, expected):
    assert Web3.toDecimal(hexstr=val) == expected
