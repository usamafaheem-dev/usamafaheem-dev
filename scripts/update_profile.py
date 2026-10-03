"""Build local GitHub profile visuals from public, dated GitHub data."""
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from html import escape
import argparse
import json
import os
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
USER = 'usamafaheem-dev'
parser = argparse.ArgumentParser()
parser.add_argument('--date', default=datetime.now(timezone(timedelta(hours=5))).date().isoformat())
args = parser.parse_args()
TODAY = date.fromisoformat(args.date)
YEAR = TODAY.year
THEMES = {
    'dark': dict(bg='#0C1118', card='#141D26', text='#F4F7FA', muted='#9AAEBE', line='#273744', accent='#C7F52B', grid=['#1A2630','#354A17','#638C1B','#97C926','#C7F52B']),
    'light': dict(bg='#FFFFFF', card='#F3F7EC', text='#1B2817', muted='#596C50', line='#D7E2CD', accent='#466E0C', grid=['#EAF0E1','#D2E6A3','#ADCE68','#789E31','#466E0C']),
}

def request(url):
    headers = {'User-Agent':'UsamaFaheem-Profile', 'Accept':'application/vnd.github+json'}
    token = os.environ.get('GITHUB_TOKEN')
    if token and url.startswith('https://api.github.com/'):
        headers['Authorization'] = 'Bearer ' + token
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as response:
        return json.load(response)

def api(path):
    return request('https://api.github.com/' + path)

def svg_start(width, height, theme, title, subtitle=''):
    c = THEMES[theme]
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle or title)}</desc>',
            f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="{c["bg"]}" stroke="{c["line"]}"/>',
            f'<g font-family="Segoe UI,Arial,sans-serif"><text x="28" y="36" fill="{c["accent"]}" font-size="11" font-weight="700" letter-spacing="2">{escape(title.upper())}</text>']

def text(x,y,value,theme,size=13,color='text',weight='400'):
    return f'<text x="{x}" y="{y}" fill="{THEMES[theme][color]}" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>'

def save(parts, filename):
    content = '\n'.join(parts + ['</g></svg>'])
    ET.fromstring(content)
    (ASSETS / filename).write_text(content,encoding='utf-8')

profile = api('users/' + USER)
repos = []
page = 1
while True:
    batch = api(f'users/{USER}/repos?per_page=100&page={page}&sort=updated')
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1

query = f'author:{USER}+author-date:{YEAR}-01-01..{TODAY.isoformat()}'
search = api('search/commits?q=' + query + '&per_page=100&sort=author-date&order=desc')
commits = search.get('items', [])
for page in range(2, min(10,(search['total_count']+99)//100)+1):
    commits.extend(api(f'search/commits?q={query}&per_page=100&page={page}&sort=author-date&order=desc').get('items',[]))
commit_counts = Counter(item['commit']['author']['date'][:10] for item in commits)

# This optional mirror scrapes GitHub's public contribution calendar. If unavailable,
# use the real indexed authored-commit dates, with a different explicit label.
try:
    contribution_data = request(f'https://github-contributions-api.jogruber.de/v4/{USER}?y={YEAR}')
    days = [d for d in contribution_data['contributions'] if d['date'] <= TODAY.isoformat()]
    counts = {d['date']:d['count'] for d in days}
    levels = {d['date']:d['level'] for d in days}
    graph_label = f'GitHub contributions / {YEAR}'
    graph_source = 'GitHub public calendar via github-contributions-api'
except Exception:
    counts = dict(commit_counts)
    levels = {d:min(4,n) for d,n in counts.items()}
    graph_label = f'Public indexed commit activity / {YEAR}'
    graph_source = 'GitHub public commit search; not the full contribution calendar'

languages = Counter(repo.get('language') for repo in repos if not repo.get('fork') and repo.get('language'))
stars = sum(repo.get('stargazers_count',0) for repo in repos)
forks = sum(repo.get('forks_count',0) for repo in repos)
contributions = sum(counts.values())
active_days = sum(1 for value in counts.values() if value)
daily = []
day = date(YEAR,1,1)
while day <= TODAY:
    daily.append((day, counts.get(day.isoformat(),0)))
    day += timedelta(days=1)
best = run = 0
for _, count in daily:
    run = run+1 if count else 0
    best = max(best,run)

snapshot = {'date':TODAY.isoformat(),'username':USER,'public_repos':profile['public_repos'],
            'followers':profile['followers'],'stars':stars,'forks':forks,
            'public_indexed_commits_year':search['total_count'], 'graph_label':graph_label,
            'graph_source':graph_source,'contributions_in_graph':contributions,
            'active_days':active_days,'best_streak_days':best,'languages_by_repository':dict(languages),
            'calendar_counts':counts,
            'recent_commits':[{'sha':i['sha'][:7],'message':i['commit']['message'].splitlines()[0],
                               'repository':i['repository']['name'],'url':i['html_url'],
                               'date':i['commit']['author']['date']} for i in commits[:5]]}
(ASSETS/'github-data.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')

for theme,c in THEMES.items():
    parts = svg_start(1180,210,theme,'GitHub at a glance', f'Public repositories, indexed commits in {YEAR}, stars and followers. Updated {TODAY}.')
    parts.append(text(28,60,f'@{USER}  /  Public data  /  Updated {TODAY}',theme,12,'muted'))
    metrics=[(profile['public_repos'],'Public repositories'),(search['total_count'],f'Indexed commits · {YEAR}'),(stars,'Repository stars'),(profile['followers'],'Followers')]
    for i,(number,label) in enumerate(metrics):
        x=28+i*288
        parts.append(f'<rect x="{x}" y="80" width="260" height="100" rx="13" fill="{c["card"]}"/>')
        parts += [text(x+19,126,f'{number:,}',theme,33,'text','700'),text(x+19,155,label,theme,12,'muted')]
    save(parts,f'stats-{theme}.svg')

    parts = svg_start(1180,270,theme,graph_label,'Real dated activity from ' + graph_source)
    parts.append(text(28,62,f'{contributions:,} contributions shown  ·  {active_days} active days  ·  best streak {best} days',theme,13))
    parts.append(text(28,83,'Jan 1 to '+TODAY.isoformat()+'  /  '+graph_source,theme,10,'muted'))
    start=date(YEAR,1,1)
    first=start-timedelta(days=(start.weekday()+1)%7)
    for week in range(53):
        for weekday in range(7):
            d=first+timedelta(days=week*7+weekday)
            if d.year!=YEAR or d>TODAY:
                continue
            x=58+week*20; y=116+weekday*15
            level=levels.get(d.isoformat(),0)
            parts.append(f'<rect x="{x}" y="{y}" width="16" height="11" rx="2" fill="{c["grid"][level]}"><title>{d}: {counts.get(d.isoformat(),0)} contributions</title></rect>')
    for i,month in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']):
        parts.append(text(58+i*90,107,month,theme,10,'muted'))
    for y,label in [(143,'Mon'),(173,'Wed'),(203,'Fri')]:
        parts.append(text(20,y,label,theme,9,'muted'))
    parts.append(text(28,246,'Commits and contributions use different counting rules.',theme,11,'muted'))
    for i,col in enumerate(c['grid']):
        parts.append(f'<rect x="{1000+i*21}" y="232" width="16" height="11" rx="2" fill="{col}"/>')
    save(parts,f'contributions-{theme}.svg')

    parts=svg_start(570,285,theme,'Languages across my repositories','Primary language of non-fork public repositories, not a line-of-code percentage.')
    parts.append(text(28,60,'Primary languages · non-fork public repositories',theme,11,'muted'))
    palette=['#C7F52B','#71D6D0','#8DA3FA','#EFAB6D','#C895DA']
    top=languages.most_common(5)
    maximum=max([n for _,n in top],default=1)
    for i,(language,n) in enumerate(top):
        y=95+i*34
        parts += [text(28,y,language,theme,12),text(491,y,str(n)+' repos',theme,11,'muted')]
        parts.append(f'<rect x="155" y="{y-10}" width="310" height="9" rx="4" fill="{c["card"]}"/><rect x="155" y="{y-10}" width="{max(4,n/maximum*310):.1f}" height="9" rx="4" fill="{palette[i]}"/>')
    parts.append(text(28,264,'Language mix reflects repositories, not skill rankings.',theme,10,'muted'))
    save(parts,f'languages-{theme}.svg')

    parts=svg_start(570,285,theme,'Activity snapshot','Year to date public activity, with GitHub source dates.')
    metrics=[(active_days,'Active days'),(best,'Best streak / days'),(contributions,'Contributions shown'),(forks,'Repository forks')]
    for i,(number,label) in enumerate(metrics):
        x=28+(i%2)*260; y=68+(i//2)*88
        parts.append(f'<rect x="{x}" y="{y}" width="238" height="76" rx="12" fill="{c["card"]}"/>')
        parts += [text(x+15,y+35,number,theme,27,'text','700'),text(x+15,y+58,label,theme,11,'muted')]
    parts.append(text(28,264,f'Year to date: {YEAR} · updated {TODAY}',theme,10,'muted'))
    save(parts,f'activity-{theme}.svg')

    parts=svg_start(1180,330,theme,'Recent public commits','Latest indexed authored commits, showing SHA, message, repository and date.')
    parts.append(text(28,61,'Latest authored commits indexed by GitHub · newest first',theme,12,'muted'))
    for i,item in enumerate(snapshot['recent_commits']):
        y=100+i*43
        if i:
            parts.append(f'<path d="M28 {y-28}H1152" stroke="{c["line"]}"/>')
        parts += [text(28,y,item['sha'],theme,12,'accent','700'),text(119,y,item['message'][:68],theme,13),
                  text(119,y+16,item['repository'][:52],theme,11,'muted'),text(1050,y,item['date'][:10],theme,11,'muted')]
    save(parts,f'commits-{theme}.svg')
print(json.dumps({k:snapshot[k] for k in ['date','public_repos','public_indexed_commits_year','graph_label','contributions_in_graph','active_days']},indent=2))
