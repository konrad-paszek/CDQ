from dataclasses import dataclass

from cdq.dto import Schema


@dataclass
class BusinessPartnerSchema(Schema):
    def typemap_define(self):
        return {"business_partner_id": str, "name": str, "country": str}

    def project(self):
        return {
            self.fields.business_partner_id.name: {"$toString": "$_id"},
            self.fields.name.name: "$companyName",
            self.fields.country.name: "$address.country",
        }
