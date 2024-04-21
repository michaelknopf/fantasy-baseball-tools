from typing import List

from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin

@dataclass_json
@dataclass
class CloserChartPitcher(DataClassJsonMixin):
    name: str
    id: int
    link: str
    role: str
    ownership_percentage: str
    is_tired: bool

@dataclass_json
@dataclass
class CloserChartTeam(DataClassJsonMixin):
    name: str
    link: str
    pitchers: List[CloserChartPitcher]
