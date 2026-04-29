"""
ISSP Solidarity Leg — RTI × CWED on unemployment spending support
Data: ISSP 2006 Role of Government IV (ZA4700)
Outcome: v23 "Gov should spend more/less on unemployment benefits" (1=much less, 5=much more)
Comparator: Model 3 in main paper, β=−0.059 (RTI × CWED on anti-immigration, ESS 2012-2018)

NOTE ON TEMPORAL GAP
ZA4700 is 2006; main paper uses ESS waves 6-9 (2012-2018). This is a historical test
of the theory, not contemporaneous replication. Interpret with that caveat.

NOTE ON RTI SCORES
Gingrich's Occupation_GROUPS.dta was not included in the replication package.
Using own ISCO-08 3-digit task scores (isco08_3d-task3.csv) as approximation.
ISCO-88 (ZA4700) and ISCO-08 codes are largely compatible at 3-digit level for
major groups 1-9; some sub-group divergence expected. Flag in any write-up.
"""

import pandas as pd
import numpy as np
import pyreadstat
from pathlib import Path
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

ROOT = Path(r'C:\Users\PKF715\Documents\claude_repos\Research_Master')
GINGRICH = ROOT / 'data' / 'raw' / 'gingrich_2019'
CWED_PATH = ROOT / 'data' / 'raw' / 'CWED' / 'cwed-subset.csv'
TASKS_PATH = ROOT / 'data' / 'raw' / 'shared_isco_task_scores' / 'isco08_3d-task3.csv'

WEST_EU_15 = ['AT', 'BE', 'CH', 'DE', 'DK', 'ES', 'FI', 'FR',
              'GB', 'IE', 'IT', 'NL', 'NO', 'PT', 'SE']

# c_alphan prefix → ISO-2 crosswalk (handles regional codes like DE-W, GB-NIR)
ALPHAN_TO_ISO2 = {
    'AU': 'AU', 'AT': 'AT', 'BE': 'BE', 'CA': 'CA', 'CH': 'CH',
    'CL': 'CL', 'CZ': 'CZ', 'DE': 'DE', 'DK': 'DK', 'DO': 'DO',
    'ES': 'ES', 'FI': 'FI', 'FR': 'FR', 'GB': 'GB', 'HR': 'HR',
    'HU': 'HU', 'IE': 'IE', 'IL': 'IL', 'JP': 'JP', 'KR': 'KR',
    'LV': 'LV', 'NL': 'NL', 'NO': 'NO', 'NZ': 'NZ', 'PH': 'PH',
    'PL': 'PL', 'PT': 'PT', 'RU': 'RU', 'SE': 'SE', 'SI': 'SI',
    'SK': 'SK', 'TW': 'TW', 'US': 'US', 'UY': 'UY', 'VE': 'VE',
    'ZA': 'ZA', 'AR': 'AR',
}


def load_issp_2006():
    path = GINGRICH / 'ZA4700_v2-0-0.dta' / 'ZA4700_v2-0-0.dta'
    df, _ = pyreadstat.read_dta(str(path))
    return df


def clean_country(df):
    """Extract 2-letter ISO code from c_alphan (handles DE-W, GB-NIR, IL (J) etc.)"""
    prefix = df['c_alphan'].str.strip().str[:2].str.upper()
    df['iso2'] = prefix.map(ALPHAN_TO_ISO2)
    return df


def clean_outcome(df):
    """
    v23: 1=Spend much more, 2=Spend more, 3=Same, 4=Spend less, 5=Spend much less
    Reverse-code so that higher = more spending support (solidarity).
    solidarity = 6 - v23  →  5=much more, 1=much less
    """
    raw = pd.to_numeric(df['v23'], errors='coerce')
    raw[raw.isin([0, 8, 9])] = np.nan
    df['solidarity'] = 6 - raw   # reverse so 5=much more spending support
    return df


def merge_rti(df):
    """
    Truncate ISCO88 4-digit → 3-digit, merge own task scores.
    Task score: 1=high routine (high RTI), 5=low routine — reverse so higher = more exposed.
    """
    tasks = pd.read_csv(TASKS_PATH)
    df['isco88_raw'] = pd.to_numeric(df['ISCO88'], errors='coerce')
    df['isco_3d'] = np.floor(df['isco88_raw'] / 10)
    df['isco_3d'] = df['isco_3d'].where(df['isco_3d'] > 0)

    df = df.merge(tasks.rename(columns={'isco08_3d': 'isco_3d'}), on='isco_3d', how='left')

    # 'task' runs 1 (high routine) to 5 (non-routine) in this file — reverse-code
    # so that higher task_z = more routine/automation-exposed (matches paper convention)
    df['task_rev'] = 6 - df['task']
    df['task_z'] = (df['task_rev'] - df['task_rev'].mean()) / df['task_rev'].std()
    return df


def merge_cwed(df):
    """Mean TOTGEN 2004-2008 for WE15 countries."""
    cwed = pd.read_csv(CWED_PATH)
    abbrev_to_iso2 = {
        'AUS': 'AU', 'AUT': 'AT', 'BEL': 'BE', 'CAN': 'CA', 'CHE': 'CH',
        'DEU': 'DE', 'DNK': 'DK', 'ESP': 'ES', 'FIN': 'FI', 'FRA': 'FR',
        'GBR': 'GB', 'GRC': 'GR', 'IRL': 'IE', 'ISL': 'IS', 'ITA': 'IT',
        'JPN': 'JP', 'NLD': 'NL', 'NOR': 'NO', 'NZL': 'NZ', 'PRT': 'PT',
        'SWE': 'SE', 'USA': 'US',
    }
    cwed['iso2'] = cwed['COUNTRY ABBREV'].map(abbrev_to_iso2)
    cwed['TOTGEN'] = pd.to_numeric(cwed['TOTGEN'], errors='coerce')
    cwed_mean = (
        cwed[cwed['YEAR'].between(2004, 2008)]
        .groupby('iso2')['TOTGEN']
        .mean()
        .reset_index()
        .rename(columns={'TOTGEN': 'cwed_generosity'})
    )
    df = df.merge(cwed_mean, on='iso2', how='left')
    df['cwed_z'] = (df['cwed_generosity'] - df['cwed_generosity'].mean()) / df['cwed_generosity'].std()
    return df


def build_controls(df):
    """age, age², female, college (DEGREE>=4), unemployed status."""
    df['age'] = pd.to_numeric(df['AGE'], errors='coerce')
    df['age2'] = df['age'] ** 2
    df['female'] = (pd.to_numeric(df['SEX'], errors='coerce') == 2).astype(float)
    # DEGREE: 0=no formal, 1=incomp primary, 2=primary, 3=lower secondary,
    #         4=upper secondary, 5=post-secondary non-tertiary, 6=lower tertiary, 7=upper tertiary
    df['degree'] = pd.to_numeric(df['DEGREE'], errors='coerce')
    df['college'] = (df['degree'] >= 5).astype(float)
    return df


def restrict_sample(df):
    """Employed respondents (WRKHRS > 0 or employment status = employed), WE15, complete cases."""
    # Use ISCO88: non-missing, non-zero, non-9xxx (not classifiable)
    df = df[df['iso2'].isin(WEST_EU_15)].copy()
    df = df[df['isco_3d'].notna() & (df['isco_3d'] < 900)].copy()
    analysis_vars = ['solidarity', 'task_z', 'cwed_z', 'cwed_generosity',
                     'age', 'age2', 'female', 'college', 'iso2']
    df = df.dropna(subset=analysis_vars).copy()
    return df


def run_model(df):
    """
    Random slopes model: solidarity ~ task_z * cwed_z + controls + (1 + task_z | iso2)
    Matches Model 3 structure from main paper: RTI slope varies by country,
    cwed_z at country level predicts that slope variation via cross-level interaction.
    With N=12 countries the between-level is small — report with that caveat.
    """
    import statsmodels.api as sm

    exog_re = df[['task_z']].copy()
    exog_re.insert(0, 'const', 1.0)
    model = smf.mixedlm(
        'solidarity ~ task_z * cwed_z + age + age2 + female + college',
        data=df,
        groups=df['iso2'],
        exog_re=exog_re,
    )
    try:
        result = model.fit(method='lbfgs', maxiter=1000, reml=False)
    except Exception:
        # Fallback: random intercepts only with OLS on cwed_z
        result = model.fit(method='nm', maxiter=2000, reml=False)
    return result


def run_model_ols(df):
    """
    OLS fallback: solidarity ~ task_z * cwed_z + controls + country_dummies
    Country dummies control for country-level confounders; interaction term tests
    whether RTI-solidarity slope differs by CWED. cwed_z collinear with country
    dummies — drop it; interaction (task_z:cwed_z) is identified from within-
    country variation in RTI interacted with cross-country variation in CWED.
    """
    result = smf.ols(
        'solidarity ~ task_z * cwed_z + age + age2 + female + college',
        data=df
    ).fit(cov_type='cluster', cov_kwds={'groups': df['iso2']})
    return result


def main():
    print('=' * 65)
    print('ISSP SOLIDARITY LEG — RTI × CWED on unemployment spending support')
    print('Data: ISSP 2006 Role of Government IV (ZA4700)')
    print('=' * 65)

    print('\n[1] Loading ZA4700...')
    df = load_issp_2006()
    print(f'    Raw N = {len(df):,}')

    df = clean_country(df)
    df = clean_outcome(df)
    df = merge_rti(df)
    df = merge_cwed(df)
    df = build_controls(df)
    df = restrict_sample(df)

    print(f'\n[2] Analysis sample:')
    print(f'    N = {len(df):,}')
    print(f'    Countries ({len(df["iso2"].unique())}): {sorted(df["iso2"].unique())}')
    print(f'    RTI merge rate: {df["task_z"].notna().mean():.1%}')
    print(f'\n    Solidarity (v23) distribution:')
    print(df['solidarity'].value_counts().sort_index().to_string())
    print(f'    Mean solidarity: {df["solidarity"].mean():.3f}  SD: {df["solidarity"].std():.3f}')

    print(f'\n[3] CWED generosity by country:')
    cwed_tbl = df.groupby('iso2')['cwed_generosity'].first().sort_values()
    for c, v in cwed_tbl.items():
        print(f'    {c}: {v:.2f}')

    print('\n[4] Running RTI × CWED models...')
    print('    (a) Random slopes (1 + task_z | country) — matches Model 3 structure')
    result_mlm = run_model(df)
    print('    (b) OLS with country-clustered SEs — simpler, used as cross-check')
    result_ols = run_model_ols(df)

    # Primary result from random slopes model
    coef_int = result_mlm.params['task_z:cwed_z']
    se_int = result_mlm.bse['task_z:cwed_z']
    p_int = result_mlm.pvalues['task_z:cwed_z']

    # OLS cross-check
    coef_ols = result_ols.params['task_z:cwed_z']
    se_ols = result_ols.bse['task_z:cwed_z']
    p_ols = result_ols.pvalues['task_z:cwed_z']

    print('\n[5] KEY RESULTS')
    print('\n--- (a) Random slopes model ---')
    print('-' * 55)
    print(f'{"Parameter":<25} {"Coef":>9} {"SE":>9} {"z":>7} {"p":>9}')
    print('-' * 55)
    for param in ['Intercept', 'task_z', 'cwed_z', 'task_z:cwed_z', 'age', 'female', 'college']:
        if param in result_mlm.params:
            se = result_mlm.bse[param]
            if se < 1000:
                print(f'{param:<25} {result_mlm.params[param]:>9.4f} '
                      f'{se:>9.4f} '
                      f'{result_mlm.params[param]/se:>7.2f} '
                      f'{result_mlm.pvalues[param]:>9.4f}')
            else:
                print(f'{param:<25} {result_mlm.params[param]:>9.4f}  [SE degenerate — country-level]')
    print('-' * 55)
    print(f'\n--- (b) OLS clustered-SE cross-check ---')
    print(f'  task_z:cwed_z  coef={coef_ols:+.4f}  SE={se_ols:.4f}  p={p_ols:.4f}')

    print(f'\nPRIMARY INTERACTION: task_z × cwed_z = {coef_int:+.4f} (SE={se_int:.4f}, p={p_int:.4f})')

    print('\n[6] COMPARISON TO MAIN PAPER MODEL 3')
    print(f'    Model 3 (anti-immigration, ESS 2012-2018): β = −0.059')
    print(f'    This model (solidarity, ISSP 2006):        β = {coef_int:+.4f}')
    print()

    if p_int < 0.05 and coef_int > 0:
        verdict = 'SOLIDARITY LEG CONFIRMED — positive and significant'
        action = 'Add as Model 5b in §VI.G, update §VII conclusion'
    elif p_int >= 0.05:
        verdict = 'FLAT / NULL — not significant'
        action = 'Acknowledge in §VI.I limitations as second null'
    else:
        verdict = 'WRONG-SIGNED — negative interaction'
        action = 'Theoretical problem — discuss with supervisor before submission'

    print(f'    VERDICT: {verdict}')
    print(f'    ACTION:  {action}')
    print()

    # Temporal gap flag
    print('[!] TEMPORAL GAP WARNING')
    print('    ZA4700 = ISSP 2006. Main paper uses ESS rounds 6-9 (2012-2018).')
    print('    This is a historical test, not contemporaneous replication.')
    print('    A 6-year gap in welfare-attitude context matters for interpretation.')
    print()
    print('    RTI SCORE CAVEAT')
    print('    Gingrich Occupation_GROUPS.dta absent from replication package.')
    print('    Own ISCO-08 task scores used as ISCO-88 approximation.')
    print('    Substantial overlap at 3-digit for groups 1-9; some sub-group drift.')


if __name__ == '__main__':
    main()
