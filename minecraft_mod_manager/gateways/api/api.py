from datetime import datetime
from typing import List

from ...core.entities.mod import Mod
from ...core.entities.sites import Site, Sites
from ...core.entities.version_info import VersionInfo
from ..http import Http


class Api:
    def __init__(self, http: Http, site_name: Sites) -> None:
        self.http = http
        self.site_name = site_name

    def get_all_versions(self, mod: Mod) -> List[VersionInfo]:
        raise NotImplementedError()

    def search_mod(self, search: str) -> List[Site]:
        raise NotImplementedError()

    def get_mod_info(self, site_id: str) -> Mod:
        """Get mod info from the id.
        Throws ModNotFoundException if it's not found.
        """
        raise NotImplementedError()

    @staticmethod
    def _to_epoch_time(date_string: str) -> int:
        # Has milliseconds
        date = 0
        try:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

        return round(date.timestamp())
