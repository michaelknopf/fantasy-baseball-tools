from typing import Dict, List, Any, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Player(DataClassJsonMixin):
    draft_auction_value: int
    id: int
    keeper_value: int
    keeper_value_future: int
    lineup_locked: bool
    on_team_id: int
    player: 'PlayerProfile'
    ratings: Dict[int, 'Ratings']
    roster_locked: bool
    status: str
    trade_locked: bool
    waiver_process_date: int

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PlayerProfile(DataClassJsonMixin):
    active: bool
    default_position_id: int
    draft_ranks_by_rank_type: 'Dict[str, DraftRank]'
    droppable: bool
    eligible_slots: List[int]
    first_name: str
    full_name: str
    games_played_by_position: Optional[Dict[int, int]]
    id: int
    injured: bool
    injury_status: str
    jersey: str
    last_name: str
    last_news_date: Optional[int]
    ownership: 'Ownership'
    pro_team_id: int
    season_outlook: str
    starter_status_by_pro_game: Dict[int, str]
    stats: List['Stats']

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Stats(DataClassJsonMixin):
    applied_total: float
    external_id: str
    id: str
    pro_team_id: int
    scoring_period_id: int
    season_id: int
    stat_source_id: int
    stat_split_type_id: int
    stats: Dict[int, float]

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Ownership(DataClassJsonMixin):
    activity_level: Any
    auction_value_average: float
    auction_value_average_change: float
    average_draft_position: float
    average_draft_position_percent_change: float
    date: int
    league_type: int
    percent_change: float
    percent_owned: float
    percent_started: float

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DraftRank(DataClassJsonMixin):
    auction_value: int
    published: bool
    rank: int
    rank_source_id: int
    rank_type: str
    slot_id: int

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Ratings:
    positional_ranking: int
    total_ranking: int
    total_rating: float
