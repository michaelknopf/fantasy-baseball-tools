from pytest import mark, param

from sabr.closer_chart import parse_closer_chart, parse_closer_id, CloserChartTeam, CloserChartPitcher


@mark.espn_integration
def test_get_closer_soup():
    parse_closer_chart.get_closer_soup()

def test_parse_closer_soup(closer_chart_soup):
    closers = parse_closer_chart.parse_closer_soup(closer_chart_soup)
    assert len(closers) == 30

def test_parse_team_node(team_node_soup):
    actual = parse_closer_chart.parse_team_soup(team_node_soup)
    expected = CloserChartTeam(
        name='ARIZONA DIAMONDBACKS',
        link='/mlb/team/_/name/ari/arizona-diamondbacks',
        pitchers=[
            CloserChartPitcher(name='Kevin Ginkel',
                               link='https://www.espn.com/mlb/player/_/id/41432/kevin-ginkel',
                               role='Closer',
                               ownership_percentage='13.7',
                               is_tired=False),
            CloserChartPitcher(name='Scott McGough',
                               link='https://www.espn.com/mlb/player/_/id/34834/scott-mcgough',
                               role='Primary setup',
                               ownership_percentage='0.2',
                               is_tired=False),
            CloserChartPitcher(name='Miguel Castro',
                               link='https://www.espn.com/mlb/player/_/id/33820/miguel-castro',
                               role='Secondary setup',
                               ownership_percentage='0.2',
                               is_tired=True),
            CloserChartPitcher(name='Paul Sewald',
                               link='https://www.espn.com/mlb/player/_/id/35009/paul-sewald',
                               role='Injured',
                               ownership_percentage='68.6',
                               is_tired=False)
        ]
    )
    assert actual == expected

@mark.parametrize(
    "url,expected",
    [
        param(
            "http://espn.go.com/mlb/player/_/id/33833/jorge-lopez", 33833, id="http"
        ),
        param(
            "https://www.espn.com/mlb/player/_/id/41432/kevin-ginkel", 41432, id="https"
        ),
        param(
            "wefwefwe", None, id="no match"
        ),
    ],
)
def test_parse_closer_id(url, expected):
    actual = parse_closer_id(url)
    assert actual == expected
