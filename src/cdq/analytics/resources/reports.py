import importlib
from dataclasses import dataclass
from typing import Type

from cdq.dto import ResourceInfo


def _getclass(classpath: str) -> Type:
    parts = classpath.split(".")
    mod, clsname = importlib.import_module(".".join(parts[:-1])), parts[-1]
    return getattr(mod, clsname)


class ClassProxy:
    def __init__(self, classpath):
        self.classpath = classpath

    @property
    def cls(self):
        return _getclass(self.classpath)


@dataclass
class ReportInfo(ResourceInfo):
    schema: ClassProxy
    source: ClassProxy
    handler: ClassProxy
    report: ClassProxy


business_partner_report = ReportInfo(
    id="business_partner_report",
    schema=ClassProxy("cdq.analytics.reporting.models.BusinessPartnerSchema"),
    source=ClassProxy("cdq.data_processing.BusinessPartners"),
    handler=ClassProxy("cdq.analytics.reporting.handlers.DefaultHandler"),
    report=ClassProxy("cdq.analytics.reporting.BusinessPartnerReport"),
)
