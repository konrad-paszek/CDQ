import cdq.analytics.reporting as reporting


def test_request_is_handled():
    client = reporting.client()
    req = reporting.request(
        report_id="business_partner_report", storage_id="storage_one"
    )
    res = client.submit(req)
    assert res.to_dict()["status"] == "FINISHED"
