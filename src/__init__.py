import pathlib, tempfile
import os
os.environ["XDG_CACHE_HOME"] = str(pathlib.Path(tempfile.gettempdir()) / "hf_cache")
