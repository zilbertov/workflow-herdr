"""Atomic state writes without predictable temporary symlinks."""
import os
import tempfile
from pathlib import Path

def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix=".herdr-state-",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write(text)
        os.replace(name,path)
    finally:
        Path(name).unlink(missing_ok=True)
