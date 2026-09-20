__author__ = 'xtieume'

from datetime import date, datetime

from pydantic import BaseModel

from dtos import Result

DEFAULT_PUBLISHED_AT = '18:35'

PRIZE_GROUPS: dict[str, list[str]] = {
    'first': ['prize1'],
    'second': ['prize2_1', 'prize2_2'],
    'third': ['prize3_1', 'prize3_2', 'prize3_3', 'prize3_4', 'prize3_5', 'prize3_6'],
    'fourth': ['prize4_1', 'prize4_2', 'prize4_3', 'prize4_4'],
    'fifth': ['prize5_1', 'prize5_2', 'prize5_3', 'prize5_4', 'prize5_5', 'prize5_6'],
    'sixth': ['prize6_1', 'prize6_2', 'prize6_3'],
    'seventh': ['prize7_1', 'prize7_2', 'prize7_3', 'prize7_4'],
}

GROUP_WIDTH = {'first': 5, 'second': 5, 'third': 5, 'fourth': 4, 'fifth': 4, 'sixth': 3, 'seventh': 2}


class RecentDraw(BaseModel):
    date: str
    special: str
    first: list[str]
    second: list[str]
    third: list[str]
    fourth: list[str]
    fifth: list[str]
    sixth: list[str]
    seventh: list[str]
    publishedAt: str


class RecentFile(BaseModel):
    generatedAt: str
    draws: list[RecentDraw]


def to_recent_draw(result: Result, published_at: str) -> RecentDraw:
    groups = {
        name: [str(getattr(result, attr)).zfill(GROUP_WIDTH[name]) for attr in attrs]
        for name, attrs in PRIZE_GROUPS.items()
    }
    return RecentDraw(
        date=result.date.strftime('%Y-%m-%d'),
        special=str(result.special).zfill(5),
        publishedAt=published_at,
        **groups,
    )


def build_recent(
    data: dict[date, Result],
    publish_times: dict[date, str],
    now: datetime,
    keep: int = 60,
) -> RecentFile:
    dates = sorted(data.keys(), reverse=True)[:keep]
    draws = [to_recent_draw(data[d], publish_times.get(d, DEFAULT_PUBLISHED_AT)) for d in dates]
    return RecentFile(generatedAt=now.isoformat(timespec='seconds'), draws=draws)
