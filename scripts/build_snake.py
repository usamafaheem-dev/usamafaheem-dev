"""Animate a snake over the existing, dated public contribution snapshot."""
from pathlib import Path
from datetime import date, timedelta
from html import escape
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
snapshot = json.loads((ASSETS / 'github-data.json').read_text(encoding='utf-8'))
today = date.fromisoformat(snapshot['date'])
start = date(today.year, 1, 1)
first_sunday = start - timedelta(days=(start.weekday() + 1) % 7)
counts = snapshot['calendar_counts']
last_column = (today - first_sunday).days // 7
columns = (date(today.year, 12, 31) - first_sunday).days // 7 + 1
pitch, side, gx, gy = 20, 14, 60, 103
grid_walk = []
for col in range(last_column + 1):
    rows = range(7) if col % 2 == 0 else range(6, -1, -1)
    grid_walk.extend((col, row) for row in rows)
steps = [(-2, 0), (-1, 0)] + grid_walk + [(last_column + 2, grid_walk[-1][1])]
visit = {point: i for i, point in enumerate(steps)}
def center(point):
    return f'{gx + point[0]*pitch + side/2:.1f},{gy + point[1]*pitch + side/2:.1f}'

themes = {
    'light': ('#ffffff','#dce6d2','#17260e','#536849',['#eef3e7','#dceea8','#b8d872','#86ad38','#466b12']),
    'dark': ('#0d1117','#29342c','#eff7e7','#a1b199',['#19251b','#354b20','#668b2d','#98bf40','#c7f52b'])
}
for theme, (bg, line, text, muted, dots) in themes.items():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="285" viewBox="0 0 1180 285" role="img" aria-labelledby="title desc"><title id="title">Contribution snake, {today.year}</title><desc id="desc">A looping snake animation built from the public contribution snapshot dated {today}. The snake clears cells and the grid resets. Not live activity.</desc>',
        f'<rect x="1" y="1" width="1178" height="283" rx="24" fill="{bg}" stroke="{line}"/>',
        '<defs><clipPath id="grid"><rect x="24" y="91" width="1132" height="155" rx="12"/></clipPath></defs>',
        f'<g font-family="Arial,Helvetica,sans-serif"><text x="28" y="35" fill="{text}" font-size="13" font-weight="700" letter-spacing="2">CONTRIBUTION SNAKE / {today.year}</text>',
        f'<text x="28" y="58" fill="{muted}" font-size="12">{snapshot["contributions_in_graph"]} contributions shown · {snapshot["active_days"]} active days · snapshot {today}</text>',
        f'<text x="28" y="79" fill="{muted}" font-size="10">Snake animation of the dated public calendar. Cells reset after every loop.</text>']
    for month in range(1,13):
        month_date = date(today.year, month, 1)
        col = (month_date - first_sunday).days // 7
        parts.append(f'<text x="{gx + col*pitch}" y="96" fill="{muted}" font-size="9">{month_date:%b}</text>')
    for row, label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
        parts.append(f'<text x="25" y="{gy+row*pitch+10}" fill="{muted}" font-size="9">{label}</text>')
    for col in range(columns):
        for row in range(7):
            day = first_sunday + timedelta(days=col*7+row)
            valid = start <= day <= today
            count = counts.get(day.isoformat(),0) if valid else 0
            level = 0 if count == 0 else 1 if count < 3 else 2 if count < 6 else 3 if count < 10 else 4
            color = dots[level]
            opacity = '1' if valid else '.3'
            parts.append(f'<rect x="{gx+col*pitch}" y="{gy+row*pitch}" width="{side}" height="{side}" rx="3" fill="{color}" opacity="{opacity}"><title>{day}: {count} contributions</title>')
            if count and (col,row) in visit:
                t = .90*visit[(col,row)]/(len(steps)-1)
                before = max(.001,t-.001)
                parts.append(f'<animate attributeName="fill" values="{color};{color};{dots[0]};{dots[0]};{color}" keyTimes="0;{before:.5f};{t:.5f};0.96;1" dur="32s" repeatCount="indefinite" calcMode="discrete"/>')
            parts.append('</rect>')
    parts.append('<g clip-path="url(#grid)">')
    key_times = ';'.join(f'{.90*i/(len(steps)-1):.6f}' for i in range(len(steps))) + ';1'
    for segment in range(6,-1,-1):
        values = [center(steps[max(0,i-segment)]) for i in range(len(steps))]
        values.append(values[-1])
        fill = '#d5ff62' if segment == 0 else '#b0dd43'
        parts.append(f'<g><rect x="-7" y="-7" width="14" height="14" rx="4" fill="{fill}" stroke="#253c10" stroke-width="1"/>')
        if segment == 0:
            parts.append('<circle cx="3" cy="-2.5" r="1.1" fill="#17300b"/><circle cx="3" cy="2.5" r="1.1" fill="#17300b"/>')
        parts.append(f'<animateTransform attributeName="transform" type="translate" values="{";".join(values)}" keyTimes="{key_times}" dur="32s" repeatCount="indefinite" calcMode="linear"/></g>')
    parts.append('</g>')
    parts.append(f'<text x="28" y="267" fill="{muted}" font-size="10">Source: {escape(snapshot["graph_source"])}. Animation is decorative; contribution totals are unchanged.</text></g></svg>')
    svg = '\n'.join(parts)
    ET.fromstring(svg)
    (ASSETS / f'snake-{theme}.svg').write_text(svg,encoding='utf-8')
print(f'Built light/dark contribution snakes from {today} public snapshot.')
