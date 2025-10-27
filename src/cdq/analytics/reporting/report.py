import os
from collections import defaultdict
from functools import wraps

import pandas as pd

from cdq.dto import FileInfo, Schema


class ReportMeta(type):
    def __new__(cls, name, bases, attrs):
        # Initialize a defaultdict to store hooks and their ordered methods
        attrs["_hook_registry"] = defaultdict(list)

        # Collect decorated methods from the class
        for name, method in attrs.items():
            if callable(method) and hasattr(method, "_hook_name"):
                # Register the method under its hook name
                attrs["_hook_registry"][method._hook_name].append(method)

        return super().__new__(cls, name, bases, attrs)


def execute(hook_name):
    """
    Decorator to mark methods for a specific hook and register them.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)

        # Mark the method with the hook name
        wrapper._hook_name = hook_name
        return wrapper

    return decorator


class Report(metaclass=ReportMeta):
    def __init__(self, data: pd.DataFrame, schema: Schema):
        self.schema = schema
        self.data = data
        self._processed = False

    def _ensure_processed(self):
        if not self._processed:
            self.process()
            self._processed = True

    def to_excel(self, filepath: os.PathLike):
        self._ensure_processed()
        self.data.to_excel(filepath, index=False)
        return FileInfo(path=filepath)

    def execute_hooks(self, hook_name):
        """
        Execute all methods registered for the given hook in order.
        """
        for method in self._hook_registry.get(hook_name, []):
            method(self)

    def process(self):
        """
        Run all processing hooks in the desired order.
        """
        self.execute_hooks("before_transform")
        self.execute_hooks("on_transform")
        self.execute_hooks("after_transform")

class BusinessPartnerReport(Report):
    pass
