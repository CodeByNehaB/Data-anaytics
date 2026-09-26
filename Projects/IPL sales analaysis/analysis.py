import pandas as pd
from collections import defaultdict

df = pd.read_csv("data/processed/IPL_Dataset_Cleaned.csv", low_memory=False)

TEAM_REBRAND_NAME = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
}

def compute_team_win_percentage(df):
    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        teams=('batting_team_clean', lambda x: sorted(set(x))),
        won_by=('match_won_by_clean', 'first'),
    ).reset_index()

    decided = match_level[match_level['won_by'] != 'Unknown']

    played, wins = defaultdict(int), defaultdict(int)
    for _, row in decided.iterrows():
        for t in row['teams']:
            played[t] += 1
        wins[row['won_by']] += 1

    team_stats = pd.DataFrame({
        'team': list(played.keys()),
        'matches_played': [played[t] for t in played],
        'wins': [wins.get(t, 0) for t in played],
    })
    team_stats['win_pct'] = (team_stats['wins'] / team_stats['matches_played'] * 100).round(1)
    return team_stats.sort_values('win_pct', ascending=False).reset_index(drop=True)



def compute_team_win_percentage_by_season(df):
    """
    Business Question 2: season-by-season win percentage per team.
    Returns a team x season pivot table. A blank (NaN) cell means that
    team did not play that season - not a 0% loss record.
    """

    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level= df.groupby('match_id').agg(
        season= ('season_clean', 'first'),
        teams=('batting_team_clean', lambda x: sorted(set(x))),
        won_by=('match_won_by_clean', 'first')
    ).reset_index()

    decided = match_level[match_level['won_by'] != 'Unknown']


    played, wins = defaultdict(int), defaultdict(int)
    for _, row in decided.iterrows():
        for t in row['teams']:
            played[(t, row['season'])] += 1
        wins[(row['won_by'], row['season'])] +=1


    rows = [{'team': t, 'season':s, 'win_pct': round(wins.get((t,s),0)/p*100, 1)}
               for (t, s), p in played.items()]

    return pd.DataFrame(rows).pivot(index='team', columns='season', values='win_pct')

def compute_head_to_head(df):
    """
    Business Question 3: head-to-head win percentage between every pair
    of teams that have played each other at least once.
    Returns a team x team pivot: row_team's win % against column_team.
    Diagonal and never-played pairs are NaN.
    """

    df = df.copy()
    df['match_won_by_clean'] =df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level= df.groupby('match_id').agg(
        teams = ('batting_team_clean', lambda x:sorted(set(x))),
        won_by=('match_won_by_clean', 'first')
    ).reset_index()

    decided = match_level[(match_level['won_by'] !='Unknown') & (match_level['teams'].apply(len)==2)]


    h2h_wins = defaultdict(int)
    for _, row in decided.iterrows():
        a,b = row['teams']
        loser = b if row['won_by'] == a else a
        h2h_wins[(row['won_by'], loser)] +=1

    teams = sorted(set(df['batting_team_clean'].unique()))
    rows = []
    for a in teams:
        for b in teams:
            if a == b:
                continue
            wins_a, wins_b = h2h_wins.get((a, b), 0), h2h_wins.get((b, a), 0)
            total = wins_a + wins_b
            if total > 0:
                rows.append({'team': a, 'opponent': b, 'win_pct': round(wins_a / total * 100, 1)})

    return pd.DataFrame(rows).pivot(index='team', columns='opponent', values='win_pct')
def compute_top_run_scorers(df, top_n=15):
    """
    Business Question 4: all-time top run-scorers.
    Sums 'runs_batter' (runs on that specific ball) - NOT 'batter_runs',
    which is a cumulative running total within the innings and would
    wildly overcount if summed directly.
    """
    runs = df.groupby('batter')['runs_batter'].sum()
    matches = df.groupby('batter')['match_id'].nunique()
    innings = df.groupby('batter').apply(lambda x: x[['match_id', 'innings']].drop_duplicates().shape[0])

    top_scorers = pd.DataFrame({
        'total_runs': runs,
        'matches': matches,
        'innings': innings,
    }).sort_values('total_runs', ascending=False).head(top_n)
    top_scorers['avg_runs_per_innings'] = (top_scorers['total_runs'] / top_scorers['innings']).round(1)
    return top_scorers
import pandas as pd
def compute_top_wicket_takers(df, top_n=15):
    """
    Business Question 5: all-time top wicket-takers.
    Sums 'bowler_wicket' (per-ball flag) - NOT 'team_wicket', which is
    the batting team's cumulative wicket count and isn't bowler-specific
    at all.
    """
    wickets = df.groupby('bowler')['bowler_wicket'].sum()
    matches=df.groupby('bowler')['match_id'].nunique()
    balls_bowled = df[df['valid_ball']==1].groupby('bowler').size()


    top_bowlers = pd.DataFrame({
        'total_wickets':wickets,
        'matches':matches,
        'balls_bowled':balls_bowled,

    }).sort_values('total_wickets', ascending=False).head(top_n)
    top_bowlers['wickets_per_match'] =(top_bowlers['total_wickets']/top_bowlers['matches']).round(2)
    return top_bowlers





import pandas as pd

def compute_top_strike_rates(df, min_balls=1500, top_n=15):
    """
    Business Question 6: best batting strike rate, minimum 1500 balls faced
    so a small hot streak doesn't outrank a real season of scoring.
    balls_faced correctly excludes wides and includes no-balls - verified
    against valid_ball and cross-checked against batter_balls.
    """
    runs = df.groupby('batter')['runs_batter'].sum()
    balls = df.groupby('batter')['balls_faced'].sum()
    matches = df.groupby('batter')['match_id'].nunique()

    sr_df = pd.DataFrame({'total_runs': runs, 'balls_faced': balls, 'matches': matches})
    sr_df = sr_df[sr_df['balls_faced'] >= min_balls].copy()
    sr_df['strike_rate'] = (sr_df['total_runs'] / sr_df['balls_faced'] * 100).round(1)
    return sr_df.sort_values('strike_rate', ascending=False).head(top_n)

def compute_top_economy_bowlers(df, min_balls=1200, top_n=15):
    """
    Business Question 7: best economy rate, minimum 200 overs (1200 legal
    balls) bowled. runs_bowler correctly excludes byes/leg-byes on legal
    deliveries - verified: runs_bowler == runs_batter on every legal ball
    in the dataset - while still including wide/no-ball penalties.
    """
    legal = df[df['valid_ball'] == 1]
    balls_bowled = legal.groupby('bowler').size()
    runs_conceded = df.groupby('bowler')['runs_bowler'].sum()

    eco_df = pd.DataFrame({'runs_conceded': runs_conceded, 'balls_bowled': balls_bowled}).dropna()
    eco_df = eco_df[eco_df['balls_bowled'] >= min_balls].copy()
    eco_df['overs_bowled'] = (eco_df['balls_bowled'] / 6).round(1)
    eco_df['economy'] = (eco_df['runs_conceded'] / (eco_df['balls_bowled'] / 6)).round(2)
    return eco_df.sort_values('economy').head(top_n)

def compute_batting_consistency(df, min_innings_per_season=5, min_seasons=6, min_career_avg=20, top_n=10):
    """
    Business Question 8: most consistent run-scorers, season to season.
    Consistency = coefficient of variation (std / mean) of each player's
    average runs-per-innings across qualifying seasons. Lower CV = more
    consistent.
    """
    innings_level = df.groupby(['batter', 'season_clean', 'match_id', 'innings'])['runs_batter'].sum().reset_index()
    season_level = innings_level.groupby(['batter', 'season_clean']).agg(
        innings_played=('runs_batter', 'count'),
        avg_runs=('runs_batter', 'mean')
    ).reset_index()

    real_seasons = season_level[season_level['innings_played'] >= min_innings_per_season]
    seasons_per_player = real_seasons.groupby('batter').size()
    qualified_players = seasons_per_player[seasons_per_player >= min_seasons].index

    consistency = real_seasons[real_seasons['batter'].isin(qualified_players)].groupby('batter')['avg_runs'].agg(['mean', 'std', 'count'])
    consistency['cv'] = (consistency['std'] / consistency['mean']).round(3)
    consistency = consistency.rename(columns={'mean': 'career_avg_runs', 'count': 'qualifying_seasons'})

    return consistency[consistency['career_avg_runs'] >= min_career_avg].sort_values('cv').head(top_n)

def compute_toss_match_correlation(df):
    """
    Business Question 9: does winning the toss correlate with winning the
    match, and has toss strategy shifted over the 19 seasons?
    """
    df = df.copy()
    df['toss_winner_clean'] = df['toss_winner'].replace(TEAM_REBRAND_NAME)
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'),
        toss_winner=('toss_winner_clean', 'first'),
        toss_decision=('toss_decision', 'first'),
        won_by=('match_won_by_clean', 'first'),
    ).reset_index()

    decided = match_level[match_level['won_by'] != 'Unknown'].copy()
    decided['toss_winner_won_match'] = decided['toss_winner'] == decided['won_by']

    overall_pct = round(decided['toss_winner_won_match'].mean() * 100, 1)
    by_decision = decided.groupby('toss_decision')['toss_winner_won_match'].mean().mul(100).round(1)

    by_season = decided.groupby('season').agg(
        toss_win_match_pct=('toss_winner_won_match', lambda x: round(x.mean() * 100, 1)),
        field_first_pct=('toss_decision', lambda x: round((x == 'field').mean() * 100, 1)),
    )
    return overall_pct, by_decision, by_season

def compute_chase_vs_defend(df):
    """
    Business Question 10: is chasing more successful than defending,
    overall and by season?
    """
    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    first_innings_team = df[df['innings'] == 1].groupby('match_id')['batting_team_clean'].first()
    second_innings_team = df[df['innings'] == 2].groupby('match_id')['batting_team_clean'].first()

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'),
        won_by=('match_won_by_clean', 'first'),
    ).reset_index()
    match_level['team_bat_2nd'] = match_level['match_id'].map(second_innings_team)

    decided = match_level.dropna(subset=['team_bat_2nd'])
    decided = decided[decided['won_by'] != 'Unknown'].copy()
    decided['chasing_team_won'] = decided['team_bat_2nd'] == decided['won_by']

    overall_pct = round(decided['chasing_team_won'].mean() * 100, 1)
    by_season = decided.groupby('season')['chasing_team_won'].mean().mul(100).round(1)
    return overall_pct, by_season

def compute_venue_scoring(df, min_matches=20):
    """
    Business Question 11: average first-innings score by venue.
    Uses the final (max) team_runs of innings 1 as that match's
    first-innings total.
    """
    first_innings = df[df['innings'] == 1].groupby('match_id').agg(
        venue=('venue_clean', 'first'),
        final_score=('team_runs', 'max')
    ).reset_index()

    venue_scores = first_innings.groupby('venue')['final_score'].agg(['mean', 'count']).round(1)
    venue_scores = venue_scores[venue_scores['count'] >= min_matches].sort_values('mean', ascending=False)
    return venue_scores.rename(columns={'mean': 'avg_first_innings_score', 'count': 'matches'})

def compute_biggest_margins(df, top_n=10):
    """
    Business Question 12: biggest winning margins, by runs and by wickets
    (wickets uses balls-remaining as a tiebreaker for the 10-wicket ties).
    """
    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    second_innings_balls = df[df['innings'] == 2].groupby('match_id')['team_balls'].max()

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'), won_by=('match_won_by_clean', 'first'),
        win_margin=('win_margin', 'first'), win_type=('win_type', 'first'),
    ).reset_index()
    match_level['balls_remaining'] = 120 - match_level['match_id'].map(second_innings_balls)

    biggest_runs = match_level[match_level['win_type'] == 'runs'].sort_values('win_margin', ascending=False).head(top_n)
    biggest_wickets = match_level[(match_level['win_type'] == 'wickets') & (match_level['win_margin'] == 10)].sort_values('balls_remaining', ascending=False).head(top_n)
    closest = match_level.dropna(subset=['win_margin']).sort_values('win_margin').head(top_n)

    return biggest_runs, biggest_wickets, closest

def compute_close_matches(df, runs_cutoff=10, wickets_cutoff=1):
    """
    Business Question 13: closest matches, and which teams/venues appear
    most often among them (as a % of their total matches, not raw count).
    """
    match_level = df.groupby('match_id').agg(
        venue=('venue_clean', 'first'), win_margin=('win_margin', 'first'), win_type=('win_type', 'first'),
        teams=('batting_team_clean', lambda x: sorted(set(x))),
    ).reset_index()

    close = match_level[((match_level['win_type'] == 'runs') & (match_level['win_margin'] <= runs_cutoff)) |
                         ((match_level['win_type'] == 'wickets') & (match_level['win_margin'] <= wickets_cutoff))]

    team_close = pd.Series([t for teams in close['teams'] for t in teams]).value_counts()
    team_total = pd.Series([t for teams in match_level.dropna(subset=['win_margin'])['teams'] for t in teams]).value_counts()
    team_stats = pd.DataFrame({'close_matches': team_close, 'total_matches': team_total})
    team_stats['pct_close'] = (team_stats['close_matches'] / team_stats['total_matches'] * 100).round(1)

    venue_close = close['venue'].value_counts()
    return team_stats.sort_values('pct_close', ascending=False), venue_close

def compute_scoring_trend(df):
    """
    Business Question 14: average first-innings score by season, plus a
    correlation test to check whether the trend is statistically real.
    """
    from scipy import stats

    first_innings = df[df['innings'] == 1].groupby('match_id').agg(
        season=('season_clean', 'first'),
        final_score=('team_runs', 'max')
    ).reset_index()

    by_season = first_innings.groupby('season')['final_score'].mean().round(1)
    corr, pval = stats.pearsonr(first_innings['season'], first_innings['final_score'])
    return by_season, corr, pval

def compute_powerplay_vs_death(df):
    """
    Business Question 15: powerplay (overs 1-6) vs death-overs (16-20)
    scoring, overall and by season.
    """
    def phase_run_rate(phase_df):
        legal_balls = (phase_df['valid_ball'] == 1).sum()
        return round(phase_df['runs_total'].sum() / (legal_balls / 6), 2)

    pp, death = df[df['over'] <= 5], df[df['over'] >= 15]
    overall = {'powerplay_rr': phase_run_rate(pp), 'death_rr': phase_run_rate(death)}

    rows = []
    for s in sorted(df['season_clean'].unique()):
        s_pp = df[(df['over'] <= 5) & (df['season_clean'] == s)]
        s_death = df[(df['over'] >= 15) & (df['season_clean'] == s)]
        rows.append({'season': s, 'powerplay_rr': phase_run_rate(s_pp), 'death_rr': phase_run_rate(s_death)})
    by_season = pd.DataFrame(rows).set_index('season')

    return overall, by_season

def compute_batting_average_and_boundaries(df, min_dismissals=30, top_n=15):
    """
    Phase 7 EDA: batting average (runs per dismissal - NOT runs per innings,
    which Question 8 already covered) and boundary counts.
    """
    runs = df.groupby('batter')['runs_batter'].sum()
    dismissals = df.groupby('batter')['striker_out'].sum()
    fours = df[df['runs_batter'] == 4].groupby('batter').size()
    sixes = df[df['runs_batter'] == 6].groupby('batter').size()

    stats_df = pd.DataFrame({'runs': runs, 'dismissals': dismissals, 'fours': fours, 'sixes': sixes}).fillna(0)
    stats_df = stats_df[stats_df['dismissals'] >= min_dismissals].copy()
    stats_df['batting_average'] = (stats_df['runs'] / stats_df['dismissals']).round(1)
    stats_df['boundary_runs'] = stats_df['fours'] * 4 + stats_df['sixes'] * 6
    stats_df['boundary_pct_of_runs'] = (stats_df['boundary_runs'] / stats_df['runs'] * 100).round(1)

    return stats_df.sort_values('batting_average', ascending=False).head(top_n)

def compute_team_scoring_profile(df):
    """
    Phase 7 EDA: team-level average runs scored/conceded and wickets
    lost/taken per innings (not win % - Question 1 already covers that).
    Restricted to regular innings (1-2); Super Overs excluded since a
    1-over mini-innings would badly skew a per-innings average.
    """
    regular = df[df['innings'] <= 2]
    innings_final = regular.groupby(['match_id', 'innings']).agg(
        batting_team=('batting_team_clean', 'first'),
        bowling_team=('bowling_team_clean', 'first'),
        final_runs=('team_runs', 'max'),
        final_wkts=('team_wicket', 'max'),
    ).reset_index()

    batting_side = innings_final.groupby('batting_team').agg(
        avg_runs_scored=('final_runs', 'mean'), avg_wkts_lost=('final_wkts', 'mean')
    ).round(1)
    bowling_side = innings_final.groupby('bowling_team').agg(
        avg_runs_conceded=('final_runs', 'mean'), avg_wkts_taken=('final_wkts', 'mean')
    ).round(1)

    team_profile = batting_side.join(bowling_side)
    team_profile['run_diff'] = (team_profile['avg_runs_scored'] - team_profile['avg_runs_conceded']).round(1)
    return team_profile.sort_values('run_diff', ascending=False)

def compute_score_records(df, top_n=5):
    """Phase 7 EDA: highest and lowest single-innings scores (completed matches only)."""
    decided_matches = df[df['win_outcome'].notna()]['match_id'].unique()
    regular = df[(df['innings'] <= 2) & (df['match_id'].isin(decided_matches))]

    innings_final = regular.groupby(['match_id', 'innings']).agg(
        team=('batting_team_clean', 'first'), season=('season_clean', 'first'), score=('team_runs', 'max')
    ).reset_index()

    highest = innings_final.sort_values('score', ascending=False).head(top_n)[['team', 'season', 'score']]
    lowest = innings_final.sort_values('score').head(top_n)[['team', 'season', 'score']]
    return highest, lowest


def compute_season_overview(df):
    """Phase 7 EDA: matches played and average wickets per match, by season."""
    matches_by_season = df.groupby('season_clean')['match_id'].nunique()
    wkts_by_season = df[df['innings'] <= 2].groupby(['season_clean', 'match_id', 'innings'])['team_wicket'].max().groupby('season_clean').mean().round(2)
    return pd.DataFrame({'matches': matches_by_season, 'avg_wickets_per_innings': wkts_by_season})

def compute_team_momentum(df):
    """
    Phase 8: does winning the previous match predict winning the next one?
    Returns (baseline_pct, after_win_pct, after_loss_pct, chi2, p_value).
    """
    from scipy.stats import chi2_contingency

    match_level = df.groupby('match_id').agg(
        date=('date', 'first'), won_by=('match_won_by_clean', 'first'),
        teams=('batting_team_clean', lambda x: sorted(set(x))),
    ).reset_index()
    match_level['date'] = pd.to_datetime(match_level['date'], format='%d-%m-%Y')
    decided = match_level[(match_level['won_by'] != 'Unknown') & (match_level['teams'].apply(len) == 2)].sort_values('date')

    rows = [{'team': t, 'date': row['date'], 'won': t == row['won_by']}
            for _, row in decided.iterrows() for t in row['teams']]
    team_form = pd.DataFrame(rows).sort_values(['team', 'date'])
    team_form['prev_result'] = team_form.groupby('team')['won'].shift(1)

    baseline = round(team_form['won'].mean() * 100, 1)
    after_win = round(team_form[team_form['prev_result'] == True]['won'].mean() * 100, 1)
    after_loss = round(team_form[team_form['prev_result'] == False]['won'].mean() * 100, 1)

    valid = team_form.dropna(subset=['prev_result'])
    chi2, p, dof, exp = chi2_contingency(pd.crosstab(valid['prev_result'], valid['won']))
    return baseline, after_win, after_loss, round(chi2, 3), round(p, 4)

def compute_team_momentum(df):
    """
    Phase 8: does winning the previous match predict winning the next one?
    Returns (baseline_pct, after_win_pct, after_loss_pct, chi2, p_value).
    """
    from scipy.stats import chi2_contingency

    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        date=('date', 'first'), won_by=('match_won_by_clean', 'first'),
        teams=('batting_team_clean', lambda x: sorted(set(x))),
    ).reset_index()
    match_level['date'] = pd.to_datetime(match_level['date'], format='%d-%m-%Y')
    decided = match_level[(match_level['won_by'] != 'Unknown') & (match_level['teams'].apply(len) == 2)].sort_values('date')

    rows = [{'team': t, 'date': row['date'], 'won': t == row['won_by']}
            for _, row in decided.iterrows() for t in row['teams']]
    team_form = pd.DataFrame(rows).sort_values(['team', 'date'])
    team_form['prev_result'] = team_form.groupby('team')['won'].shift(1)

    baseline = round(team_form['won'].mean() * 100, 1)
    after_win = round(team_form[team_form['prev_result'] == True]['won'].mean() * 100, 1)
    after_loss = round(team_form[team_form['prev_result'] == False]['won'].mean() * 100, 1)

    valid = team_form.dropna(subset=['prev_result'])
    chi2, p, dof, exp = chi2_contingency(pd.crosstab(valid['prev_result'], valid['won']))
    return baseline, after_win, after_loss, round(chi2, 3), round(p, 4)

def compute_toss_chase_significance(df):
    """
    Phase 8: formal significance tests for toss impact and chase advantage.
    """
    from scipy.stats import binomtest, chi2_contingency

    df = df.copy()
    df['toss_winner_clean'] = df['toss_winner'].replace(TEAM_REBRAND_NAME)
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        toss_winner=('toss_winner_clean', 'first'), toss_decision=('toss_decision', 'first'),
        won_by=('match_won_by_clean', 'first'),
    ).reset_index()
    decided = match_level[match_level['won_by'] != 'Unknown'].copy()
    decided['toss_winner_won'] = decided['toss_winner'] == decided['won_by']

    n_toss_wins, n_total = decided['toss_winner_won'].sum(), len(decided)
    test1_p = binomtest(n_toss_wins, n_total, 0.5).pvalue

    chi2, test2_p, _, _ = chi2_contingency(pd.crosstab(decided['toss_decision'], decided['toss_winner_won']))

    second_innings_team = df[df['innings'] == 2].groupby('match_id')['batting_team_clean'].first()
    match_level['team_bat_2nd'] = match_level['match_id'].map(second_innings_team)
    decided3 = match_level.dropna(subset=['team_bat_2nd'])
    decided3 = decided3[decided3['won_by'] != 'Unknown'].copy()
    decided3['chase_won'] = decided3['team_bat_2nd'] == decided3['won_by']
    test3_p = binomtest(decided3['chase_won'].sum(), len(decided3), 0.5).pvalue

    return {
        'toss_winner_win_pct': round(n_toss_wins / n_total * 100, 1), 'test1_p': round(test1_p, 4),
        'decision_chi2': round(chi2, 3), 'test2_p': round(test2_p, 6),
        'chase_win_pct': round(decided3['chase_won'].mean() * 100, 1), 'test3_p': round(test3_p, 4),
    }

def compute_team_momentum(df):
    """
    Phase 8: does winning the previous match predict winning the next one?
    Returns (baseline_pct, after_win_pct, after_loss_pct, chi2, p_value).
    """
    from scipy.stats import chi2_contingency

    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        date=('date', 'first'), won_by=('match_won_by_clean', 'first'),
        teams=('batting_team_clean', lambda x: sorted(set(x))),
    ).reset_index()
    match_level['date'] = pd.to_datetime(match_level['date'], format='%Y-%m-%d')
    decided = match_level[(match_level['won_by'] != 'Unknown') & (match_level['teams'].apply(len) == 2)].sort_values('date')

    rows = [{'team': t, 'date': row['date'], 'won': t == row['won_by']}
            for _, row in decided.iterrows() for t in row['teams']]
    team_form = pd.DataFrame(rows).sort_values(['team', 'date'])
    team_form['prev_result'] = team_form.groupby('team')['won'].shift(1)

    baseline = round(team_form['won'].mean() * 100, 1)
    after_win = round(team_form[team_form['prev_result'] == True]['won'].mean() * 100, 1)
    after_loss = round(team_form[team_form['prev_result'] == False]['won'].mean() * 100, 1)

    valid = team_form.dropna(subset=['prev_result'])
    chi2, p, dof, exp = chi2_contingency(pd.crosstab(valid['prev_result'], valid['won']))
    return baseline, after_win, after_loss, round(chi2, 3), round(p, 4)

def compute_venue_toss_advantage(df, min_per_decision=10):
    """
    Phase 8: does the field-first advantage hold at every venue, or do
    some venues actually favor batting first?
    """
    df = df.copy()
    df['toss_winner_clean'] = df['toss_winner'].replace(TEAM_REBRAND_NAME)
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        venue=('venue_clean', 'first'), toss_winner=('toss_winner_clean', 'first'),
        toss_decision=('toss_decision', 'first'), won_by=('match_won_by_clean', 'first'),
    ).reset_index()
    decided = match_level[match_level['won_by'] != 'Unknown'].copy()
    decided['toss_winner_won'] = decided['toss_winner'] == decided['won_by']

    venue_field = decided[decided['toss_decision'] == 'field'].groupby('venue')['toss_winner_won'].agg(['mean', 'count'])
    venue_bat = decided[decided['toss_decision'] == 'bat'].groupby('venue')['toss_winner_won'].agg(['mean', 'count'])
    venue_field.columns, venue_bat.columns = ['field_win_pct', 'field_n'], ['bat_win_pct', 'bat_n']
    combined = venue_field.join(venue_bat, how='outer')
    combined['field_win_pct'] = (combined['field_win_pct'] * 100).round(1)
    combined['bat_win_pct'] = (combined['bat_win_pct'] * 100).round(1)

    qualified = combined[(combined['field_n'] >= min_per_decision) & (combined['bat_n'] >= min_per_decision)].copy()
    qualified['field_advantage'] = qualified['field_win_pct'] - qualified['bat_win_pct']
    return qualified.sort_values('field_advantage')

def compute_powerplay_death_ttest(df):
    """
    Phase 9, Test 3: paired t-test - is death-overs run rate genuinely
    higher than powerplay run rate, innings by innings?
    """
    from scipy.stats import ttest_rel

    def phase_rr(sub):
        legal = (sub['valid_ball'] == 1).sum()
        return sub['runs_total'].sum() / (legal / 6) if legal > 0 else None

    pp_by_innings = df[df['over'] <= 5].groupby(['match_id', 'innings']).apply(phase_rr)
    death_by_innings = df[df['over'] >= 15].groupby(['match_id', 'innings']).apply(phase_rr)

    paired = pd.DataFrame({'pp_rr': pp_by_innings, 'death_rr': death_by_innings}).dropna()
    t_stat, p_val = ttest_rel(paired['death_rr'], paired['pp_rr'])
    mean_diff = round((paired['death_rr'] - paired['pp_rr']).mean(), 2)
    return round(t_stat, 3), p_val, mean_diff, len(paired)

import importlib
import analysis
importlib.reload(analysis)
from analysis import compute_powerplay_death_ttest

t_stat, p_val, mean_diff, n = compute_powerplay_death_ttest(df)
print(f"t={t_stat}, p={p_val}, mean diff={mean_diff} runs/over, n={n} innings")

def compute_powerplay_death_ttest(df):
    """
    Phase 9, Test 3: paired t-test - is death-overs run rate genuinely
    higher than powerplay run rate, innings by innings?
    """
    from scipy.stats import ttest_rel

    def phase_rr(sub):
        legal = (sub['valid_ball'] == 1).sum()
        return sub['runs_total'].sum() / (legal / 6) if legal > 0 else None

    pp_by_innings = df[df['over'] <= 5].groupby(['match_id', 'innings']).apply(phase_rr)
    death_by_innings = df[df['over'] >= 15].groupby(['match_id', 'innings']).apply(phase_rr)

    paired = pd.DataFrame({'pp_rr': pp_by_innings, 'death_rr': death_by_innings}).dropna()
    t_stat, p_val = ttest_rel(paired['death_rr'], paired['pp_rr'])
    mean_diff = round((paired['death_rr'] - paired['pp_rr']).mean(), 2)
    return round(t_stat, 3), p_val, mean_diff, len(paired)

import importlib
import analysis
importlib.reload(analysis)
from analysis import compute_powerplay_death_ttest

t_stat, p_val, mean_diff, n = compute_powerplay_death_ttest(df)
print(f"t={t_stat}, p={p_val}, mean diff={mean_diff} runs/over, n={n} innings")

def compute_kpis(df):
    """Phase 10: headline KPI layer for the dashboard."""
    teams_raw = set(df['batting_team'].unique()) | set(df['bowling_team'].unique())
    players = set(df['batter'].unique()) | set(df['bowler'].unique()) | set(df['non_striker'].unique())
    decided_matches = df[df['win_outcome'].notna()]['match_id'].unique()
    regular = df[(df['innings'] <= 2) & (df['match_id'].isin(decided_matches))]
    innings_scores = regular.groupby(['match_id', 'innings'])['team_runs'].max()

    top_scorer = df.groupby('batter')['runs_batter'].sum().idxmax()
    top_scorer_runs = df.groupby('batter')['runs_batter'].sum().max()
    top_wkt_taker = df.groupby('bowler')['bowler_wicket'].sum().idxmax()
    top_wkt_taker_wkts = df.groupby('bowler')['bowler_wicket'].sum().max()

    return {
        'total_matches': df['match_id'].nunique(),
        'total_seasons': df['season_clean'].nunique(),
        'total_teams': 15,
        'total_players': len(players),
        'total_runs': int(df['runs_total'].sum()),
        'total_wickets': int(df['striker_out'].sum()),
        'average_score': round(innings_scores.mean(), 1),
        'highest_score': int(innings_scores.max()),
        'top_run_scorer': f"{top_scorer} ({top_scorer_runs})",
        'top_wicket_taker': f"{top_wkt_taker} ({top_wkt_taker_wkts})",
        'match_decisiveness_pct': round(len(decided_matches) / df['match_id'].nunique() * 100, 1),
    }


def compute_powerplay_death_ttest(df):
    """Phase 9, Test 3: paired t-test - death-overs vs powerplay run rate, innings by innings."""
    from scipy.stats import ttest_rel

    def phase_rr(sub):
        legal = (sub['valid_ball'] == 1).sum()
        return sub['runs_total'].sum() / (legal / 6) if legal > 0 else None

    pp_by_innings = df[df['over'] <= 5].groupby(['match_id', 'innings']).apply(phase_rr, include_groups=False)
    death_by_innings = df[df['over'] >= 15].groupby(['match_id', 'innings']).apply(phase_rr, include_groups=False)

    paired = pd.DataFrame({'pp_rr': pp_by_innings, 'death_rr': death_by_innings}).dropna()
    t_stat, p_val = ttest_rel(paired['death_rr'], paired['pp_rr'])
    mean_diff = round((paired['death_rr'] - paired['pp_rr']).mean(), 2)
    return round(t_stat, 3), p_val, mean_diff, len(paired)
def compute_top_run_scorers(df, top_n=15):
    """Business Question 4: all-time top run-scorers (sums runs_batter, not batter_runs)."""
    runs = df.groupby('batter')['runs_batter'].sum()
    matches = df.groupby('batter')['match_id'].nunique()
    innings = df.groupby('batter').apply(lambda x: x[['match_id', 'innings']].drop_duplicates().shape[0], include_groups=False)

    top_scorers = pd.DataFrame({
        'total_runs': runs,
        'matches': matches,
        'innings': innings,
    }).sort_values('total_runs', ascending=False).head(top_n)
    top_scorers['avg_runs_per_innings'] = (top_scorers['total_runs'] / top_scorers['innings']).round(1)
    return top_scorers
def compute_top_run_scorers(df, top_n=15):
    """
    Business Question 4: all-time top run-scorers.
    Sums 'runs_batter' (runs on that specific ball) - NOT 'batter_runs',
    which is a cumulative running total within the innings and would
    wildly overcount if summed directly.
    """
    runs = df.groupby('batter')['runs_batter'].sum()
    matches = df.groupby('batter')['match_id'].nunique()
    innings = df.groupby('batter').apply(lambda x: x[['match_id', 'innings']].drop_duplicates().shape[0])

    top_scorers = pd.DataFrame({
        'total_runs': runs,
        'matches': matches,
        'innings': innings,
    }).sort_values('total_runs', ascending=False).head(top_n)
    top_scorers['avg_runs_per_innings'] = (top_scorers['total_runs'] / top_scorers['innings']).round(1)
    return top_scorers

def compute_powerplay_death_ttest(df):
    """Phase 9, Test 3: paired t-test - death-overs vs powerplay run rate, innings by innings."""
    from scipy.stats import ttest_rel

    def phase_rr(sub):
        legal = (sub['valid_ball'] == 1).sum()
        return sub['runs_total'].sum() / (legal / 6) if legal > 0 else None

    pp_by_innings = df[df['over'] <= 5].groupby(['match_id', 'innings'], include_groups=False).apply(phase_rr)
    death_by_innings = df[df['over'] >= 15].groupby(['match_id', 'innings'], include_groups=False).apply(phase_rr)

    paired = pd.DataFrame({'pp_rr': pp_by_innings, 'death_rr': death_by_innings}).dropna()
    t_stat, p_val = ttest_rel(paired['death_rr'], paired['pp_rr'])
    mean_diff = round((paired['death_rr'] - paired['pp_rr']).mean(), 2)
    return round(t_stat, 3), p_val, mean_diff, len(paired)

def compute_powerplay_death_ttest(df):
    """Phase 9, Test 3: paired t-test - death-overs vs powerplay run rate, innings by innings."""
    from scipy.stats import ttest_rel

    def phase_rr(sub):
        legal = (sub['valid_ball'] == 1).sum()
        return sub['runs_total'].sum() / (legal / 6) if legal > 0 else None

    pp_by_innings = df[df['over'] <= 5].groupby(['match_id', 'innings']).apply(phase_rr, include_groups=False)
    death_by_innings = df[df['over'] >= 15].groupby(['match_id', 'innings']).apply(phase_rr, include_groups=False)

    paired = pd.DataFrame({'pp_rr': pp_by_innings, 'death_rr': death_by_innings}).dropna()
    t_stat, p_val = ttest_rel(paired['death_rr'], paired['pp_rr'])
    mean_diff = round((paired['death_rr'] - paired['pp_rr']).mean(), 2)
    return round(t_stat, 3), p_val, mean_diff, len(paired)

def compute_kpis(df):
    """Phase 10: headline KPI layer for the dashboard."""
    teams_raw = set(df['batting_team'].unique()) | set(df['bowling_team'].unique())
    players = set(df['batter'].unique()) | set(df['bowler'].unique()) | set(df['non_striker'].unique())
    decided_matches = df[df['win_outcome'].notna()]['match_id'].unique()
    regular = df[(df['innings'] <= 2) & (df['match_id'].isin(decided_matches))]
    innings_scores = regular.groupby(['match_id', 'innings'])['team_runs'].max()

    top_scorer = df.groupby('batter')['runs_batter'].sum().idxmax()
    top_scorer_runs = df.groupby('batter')['runs_batter'].sum().max()
    top_wkt_taker = df.groupby('bowler')['bowler_wicket'].sum().idxmax()
    top_wkt_taker_wkts = df.groupby('bowler')['bowler_wicket'].sum().max()

    return {
        'total_matches': df['match_id'].nunique(),
        'total_seasons': df['season_clean'].nunique(),
        'total_teams': 15,
        'total_players': len(players),
        'total_runs': int(df['runs_total'].sum()),
        'total_wickets': int(df['striker_out'].sum()),
        'average_score': round(innings_scores.mean(), 1),
        'highest_score': int(innings_scores.max()),
        'top_run_scorer': f"{top_scorer} ({top_scorer_runs})",
        'top_wicket_taker': f"{top_wkt_taker} ({top_wkt_taker_wkts})",
        'match_decisiveness_pct': round(len(decided_matches) / df['match_id'].nunique() * 100, 1),
    }


def compute_player_runs_by_season(df, players):
    """
    Dashboard: runs per season for a specific list of players (not a
    top-N ranking - this is for showing exactly who was selected).
    """
    filtered = df[df['batter'].isin(players)]
    return filtered.groupby(['batter', 'season_clean'])['runs_batter'].sum().reset_index()
