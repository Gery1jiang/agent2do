
import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr


def safe_execute(code, timeout=30):
    """
    在受限环境中执行 Python 代码
    返回：{"stdout": str, "stderr": str, "error": str | None}
    """
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # 受限全局变量：只允许安全的内置函数
    safe_globals = {
        "__name__": "__sandbox__",
        "__builtins__": {
            "__build_class__": __build_class__,
            "print": print, "len": len, "range": range,
            "enumerate": enumerate, "zip": zip, "map": map,
            "filter": filter, "sorted": sorted, "sum": sum,
            "min": min, "max": max, "abs": abs, "round": round,
            "int": int, "float": float, "str": str, "bool": bool,
            "list": list, "dict": dict, "set": set, "tuple": tuple,
            "isinstance": isinstance, "type": type,
        }
    }

    error = None
    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, safe_globals)
    except Exception:
        error = traceback.format_exc()

    return {
        "stdout": stdout_capture.getvalue(),
        "stderr": stderr_capture.getvalue(),
        "error": error,
    }

