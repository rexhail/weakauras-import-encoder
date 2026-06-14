"""
weakauras_encoder.py — encode/decode WeakAuras import strings ("!WA:2!") in Python.

Pipeline (matches WeakAuras + LibSerialize + LibDeflate):
    LibSerialize:Serialize  ->  raw DEFLATE (zlib)  ->  EncodeForPrint  ->  "!WA:2!" + data

LibSerialize (MIT, by Ross Nichols) is run directly through a real Lua interpreter
(via `lupa`), so serialization is byte-for-byte identical to the game. The DEFLATE
step uses Python's zlib (raw, no zlib header), which WeakAuras' LibDeflate decodes
natively. EncodeForPrint is a 6-bit packing over a fixed 64-char alphabet.

Requires:  pip install lupa
"""
import os, zlib, tempfile, urllib.request

try:
    from lupa import LuaRuntime
except ImportError:  # pragma: no cover
    raise SystemExit("This tool needs the 'lupa' package:  pip install lupa")

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()"
PREFIX = "!WA:2!"
_LS_URL = "https://raw.githubusercontent.com/rossnichols/LibSerialize/master/LibSerialize.lua"
_LS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LibSerialize.lua")


def _strip_header(src: str) -> str:
    i = src.find("--[[")
    return src[i:] if i > 0 else src


def _lua():
    """Return (LuaRuntime, LibSerialize). Downloads LibSerialize.lua on first use."""
    if not os.path.exists(_LS_PATH):
        data = urllib.request.urlopen(_LS_URL).read().decode("utf-8")
        with open(_LS_PATH, "w", encoding="utf-8") as f:
            f.write(_strip_header(data))
    lua = LuaRuntime(unpack_returned_tuples=True)
    LS = lua.execute(_strip_header(open(_LS_PATH, encoding="utf-8").read()))
    return lua, LS


# ---------- EncodeForPrint / DecodeForPrint (6-bit packing) ----------
def encode_for_print(data: bytes) -> str:
    out, i, n = [], 0, len(data)
    while i + 3 <= n:
        c = data[i] + data[i + 1] * 256 + data[i + 2] * 65536
        for _ in range(4):
            out.append(ALPHABET[c % 64]); c //= 64
        i += 3
    rem = n - i
    if rem:
        c = 0
        for k in range(rem):
            c += data[i + k] * (256 ** k)
        bits = rem * 8
        while bits > 0:
            out.append(ALPHABET[c % 64]); c //= 64; bits -= 6
    return "".join(out)


def decode_for_print(s: str) -> bytes:
    lut = {ch: i for i, ch in enumerate(ALPHABET)}
    v = [lut[ch] for ch in s]
    o, i, n = bytearray(), 0, len(v)
    while i + 4 <= n:
        c = v[i] + v[i + 1] * 64 + v[i + 2] * 64 ** 2 + v[i + 3] * 64 ** 3
        o.append(c & 255); c >>= 8
        o.append(c & 255); c >>= 8
        o.append(c & 255); i += 4
    rem = n - i
    if rem:
        c = 0
        for k in range(rem):
            c += v[i + k] * (64 ** k)
        for _ in range((rem * 6) // 8):
            o.append(c & 255); c >>= 8
    return bytes(o)


# ---------- high-level API ----------
def encode(serialized: bytes) -> str:
    """serialized LibSerialize bytes -> importable !WA:2! string"""
    raw_deflate = zlib.compress(serialized, 9)[2:-4]  # strip zlib header + adler32
    return PREFIX + encode_for_print(raw_deflate)


def decode(import_string: str) -> bytes:
    """importable !WA:2! string -> serialized LibSerialize bytes"""
    if not import_string.startswith(PREFIX):
        raise ValueError("not a !WA:2! string")
    return zlib.decompress(decode_for_print(import_string[len(PREFIX):]), -15)


def serialize(lua_chunk: str) -> bytes:
    """Run a Lua chunk that `return`s a table; serialize it via LibSerialize.
    `LS` (LibSerialize) is exposed as a global to the chunk."""
    lua, LS = _lua()
    g = lua.globals(); g.LS = LS
    g._wa_tbl = lua.execute(lua_chunk)
    fd, path = tempfile.mkstemp(suffix=".ser"); os.close(fd)
    g._wa_out = path
    lua.execute('local s = LS:Serialize(_wa_tbl); '
                'local f = io.open(_wa_out, "wb"); f:write(s); f:close()')
    data = open(path, "rb").read(); os.remove(path)
    return data


def deserialize(serialized: bytes):
    """serialized bytes -> (ok, lua_table) using the genuine LibSerialize."""
    lua, LS = _lua()
    return LS.Deserialize(LS, serialized)


def encode_table(lua_chunk: str) -> str:
    """convenience: Lua table chunk -> importable !WA:2! string"""
    return encode(serialize(lua_chunk))
