import importlib
from typing import Type
from pydantic import BaseModel, Field, PrivateAttr

class ClassProxy(BaseModel):
    classpath: str

    _class_instance: Type = PrivateAttr()

    @property
    def cls(self) -> Type:
        if not hasattr(self, "_class_instance") or self._class_instance is None:
            parts = self.classpath.split(".")
            mod, clsname = importlib.import_module(".".join(parts[:-1])), parts[-1]
            self._class_instance = getattr(mod, clsname)
        return self._class_instance

class ReportInfo(BaseModel):
    id: str
    schema: ClassProxy
    source: ClassProxy
    handler: ClassProxy
    report: ClassProxy

business_partner_report = ReportInfo(
    id="business_partner_report",
    schema=ClassProxy(classpath="cdq.analytics.reporting.models.BusinessPartnerSchema"),
    source=ClassProxy(classpath="cdq.data_processing.BusinessPartners"),
    handler=ClassProxy(classpath="cdq.analytics.reporting.handlers.DefaultHandler"),
    report=ClassProxy(classpath="cdq.analytics.reporting.BusinessPartnerReport"),
)
