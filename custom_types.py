"""
Shared type aliases for DocMind AI.

These aliases improve readability and provide a single location
for commonly used identifier types.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

# ============================================================================
# Identifier Types
# ============================================================================

DocumentId = Annotated[
    str,
    Field(
        min_length=1,
        description="Unique document identifier.",
    ),
]

ChunkId = Annotated[
    str,
    Field(
        min_length=1,
        description="Unique chunk identifier.",
    ),
]

SHA256Hash = Annotated[
    str,
    Field(
        min_length=64,
        max_length=64,
        description="SHA256 hash represented as a 64-character hexadecimal string.",
    ),
]

# ============================================================================
# File Types
# ============================================================================

FilePath = Annotated[
    str,
    Field(
        min_length=1,
        description="Absolute or relative file path.",
    ),
]

FileName = Annotated[
    str,
    Field(
        min_length=1,
        description="Original file name.",
    ),
]

StoredFileName = Annotated[
    str,
    Field(
        min_length=1,
        description="File name used for storage.",
    ),
]