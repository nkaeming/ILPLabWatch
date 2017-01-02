from UI.AbstractView import AbstractView


class logDownload(AbstractView):
    """View zum herunterladen von logDownloads"""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)
