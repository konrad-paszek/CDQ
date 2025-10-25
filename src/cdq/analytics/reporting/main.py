from .request import ReportRequest, request
from .response import HandledResponse, ResultContext


class ReportingClient:
    def handle_standard_report(self, request):
        handler = request.info.handler.cls()
        return handler.handle(request)

    def submit(self, request: ReportRequest):
        return self.handle_standard_report(request)


def client():
    return ReportingClient()
