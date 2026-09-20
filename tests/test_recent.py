from datetime import date, datetime
from zoneinfo import ZoneInfo

from dtos import Result
from recent import DEFAULT_PUBLISHED_AT, build_recent, record_publish_time, to_recent_draw


def sample_result(d: date) -> Result:
    return Result(
        date=d,
        special=31429, prize1=3514,
        prize2_1=53198, prize2_2=75906,
        prize3_1=8456, prize3_2=7879, prize3_3=58383, prize3_4=94172, prize3_5=96124, prize3_6=89852,
        prize4_1=277, prize4_2=3386, prize4_3=8578, prize4_4=9159,
        prize5_1=479, prize5_2=4683, prize5_3=6690, prize5_4=5614, prize5_5=4245, prize5_6=9355,
        prize6_1=875, prize6_2=772, prize6_3=57,
        prize7_1=73, prize7_2=55, prize7_3=76, prize7_4=64,
    )


def test_pad_zero_theo_bac_giai():
    draw = to_recent_draw(sample_result(date(2026, 9, 19)), '18:35')
    assert draw.special == '31429'
    assert draw.third[0] == '08456'      # prize3_1=8456 → pad 5
    assert draw.fourth[0] == '0277'      # prize4_1=277 → pad 4
    assert draw.fifth[0] == '0479'       # prize5_1=479 → pad 4
    assert draw.sixth[3 - 1] == '057'    # prize6_3=57 → pad 3
    assert draw.seventh[0] == '73'       # đủ 2, không thêm 0


def test_thu_tu_moi_nhat_truoc_va_gioi_han_keep():
    data = {date(2026, 9, 17): sample_result(date(2026, 9, 17)),
            date(2026, 9, 19): sample_result(date(2026, 9, 19)),
            date(2026, 9, 18): sample_result(date(2026, 9, 18))}
    recent = build_recent(data, {}, now=datetime(2026, 9, 19, 18, 35, tzinfo=ZoneInfo('Asia/Ho_Chi_Minh')), keep=2)
    assert [d.date for d in recent.draws] == ['2026-09-19', '2026-09-18']


def test_published_at_backfill():
    d = date(2026, 9, 19)
    draw = to_recent_draw(sample_result(d), DEFAULT_PUBLISHED_AT)
    assert draw.publishedAt == '18:35'
    draw2 = to_recent_draw(sample_result(d), '18:41')
    assert draw2.publishedAt == '18:41'


def test_generated_at_iso():
    recent = build_recent({}, {}, now=datetime(2026, 9, 19, 18, 35, 12, tzinfo=ZoneInfo('Asia/Ho_Chi_Minh')))
    assert recent.generatedAt == '2026-09-19T18:35:12+07:00'


def test_record_publish_time_khong_de_len_ban_ghi_cu():
    times = {date(2026, 9, 18): '18:35'}
    first = record_publish_time(
        times, date(2026, 9, 19), datetime(2026, 9, 19, 18, 36, tzinfo=ZoneInfo('Asia/Ho_Chi_Minh')))
    assert first == '18:36'
    again = record_publish_time(
        times, date(2026, 9, 19), datetime(2026, 9, 19, 19, 10, tzinfo=ZoneInfo('Asia/Ho_Chi_Minh')))
    assert again == '18:36'  # kỳ đã có giờ rồi thì giữ giờ ĐẦU TIÊN ghi nhận
    assert times == {date(2026, 9, 18): '18:35', date(2026, 9, 19): '18:36'}
