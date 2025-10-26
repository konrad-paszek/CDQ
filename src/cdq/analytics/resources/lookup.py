from .reports import business_partner_report

class ResourceLookup:

    _reports = {
        business_partner_report.id: business_partner_report,
    }

    @classmethod
    def getinfo(cls, report_id: str):
        try:
            return cls._reports[report_id]
        except KeyError:
            raise ValueError(f"unable to find {report_id}")