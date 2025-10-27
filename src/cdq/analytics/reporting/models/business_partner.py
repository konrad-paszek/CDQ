from cdq.dto import Schema


class BusinessPartnerSchema(Schema):
    def typemap_define(self):
        return {"business_partner_id": str, "name": str, "country": str, "vat_number": str}

    def project(self):
        return {
            self.fields.get('business_partner_id').name: {"$toString": "$_id"},
            self.fields.get('name').name: "$companyName",
            self.fields.get('country').name: "$address.country",
            self.fields.get('vat_number').name: "$identifier.vatNumber",
        }
