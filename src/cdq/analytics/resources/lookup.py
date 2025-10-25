from .reports import business_partner_report


class ResourceLookup:

    @classmethod
    def getinfo(cls, report_id: str):
        # TODO: maintaining a list of searchable reports could get tedious
        for item in [business_partner_report]:
            if item.id == report_id:
                return item
        raise ValueError(f"unable to find {report_id}")
