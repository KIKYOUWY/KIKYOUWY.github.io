"""Build a portable academic homepage with Python's standard library."""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
p = json.loads((ROOT / 'data/profile.json').read_text(encoding='utf-8'))
ordering = json.loads((ROOT / 'data/publication-order.json').read_text(encoding='utf-8'))

def normalize_author(name):
    return re.sub(r'[\s.]+', '', name).casefold()

self_aliases = {normalize_author(name) for name in ordering['first_author_aliases']}

def is_first_author(paper):
    first_author = re.split(r'[,，]', paper['authors'], maxsplit=1)[0]
    return normalize_author(first_author) in self_aliases

def publication_sort_key(paper):
    category_rank = ordering['category_order'].index(paper['category'])
    # These are editable presentation tiers, not live impact-factor measurements.
    venue_rank = 0
    if paper['category'] == 'journal':
        venue_rank = next((i for i, tier in enumerate(ordering['journal_venue_tiers'])
                           if any(paper['venue'].startswith(venue) for venue in tier)),
                          len(ordering['journal_venue_tiers']))
    return category_rank, venue_rank, not is_first_author(paper), -int(paper['year'] or 0)

p['papers'] = sorted(p['papers'], key=publication_sort_key)
e = lambda s: html.escape(str(s), quote=True)
def bi(en, zh):
    return f'<span class="en">{en}</span><span class="zh">{zh}</span>'

news_config = json.loads((ROOT / 'data/news.json').read_text(encoding='utf-8'))
paper_ids = {paper['id'] for paper in p['papers']}
assert set(news_config['publications']) <= paper_ids, 'Unknown paper in News'
corresponding_ids = set(news_config['corresponding_author_ids'])
assert corresponding_ids <= paper_ids, 'Unknown corresponding-author paper'
news_events = []
for paper in p['papers']:
    if paper['id'] not in news_config['publications']:
        continue
    event = news_config['publications'][paper['id']]
    stamp = event['date']
    assert re.fullmatch(r'\d{4}(?:-\d{2})?(?:-\d{2})?', stamp), 'Invalid News date'
    parts = [int(part) for part in stamp.split('-')]
    date(*(parts + [1] * (3 - len(parts))))  # Validate without inventing display precision.
    role = 'corresponding' if paper['id'] in corresponding_ids else 'first' if is_first_author(paper) else 'coauthor'
    news_events.append((paper, event, role))

news_subjects = {'first': ('One first-authored paper', '一篇第一作者论文'), 'coauthor': ('One co-authored paper', '一篇合著论文'), 'corresponding': ('One paper (corresponding author)', '一篇通讯作者论文')}
news_rows = []
for announcement in news_config.get('announcements', []):
    stamp = announcement['date']
    date.fromisoformat(stamp)
    message = bi(e(announcement['en']), e(announcement['zh']))
    if announcement.get('venue'):
        venue_text = e(announcement['venue'])
        message = message.replace(venue_text, f'<strong>{venue_text}</strong>')
    if announcement.get('url'):
        message = f'<a href="{e(announcement["url"])}" target="_blank" rel="noopener noreferrer">{message}</a>'
    row = f'<li data-news-id="{e(announcement["id"])}" data-news-role="{e(announcement["role"])}"><time datetime="{e(stamp)}">{e(stamp.replace("-", "."))}</time><div>{message}</div></li>'
    news_rows.append((stamp, row))
for paper, event, role in news_events:
    url = 'https://doi.org/' + paper['doi'] if paper.get('doi') else paper['scholar']
    subject_en, subject_zh = news_subjects[role]
    def news_link(label):
        return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer" title="{e(paper["title"])}">{e(label)}</a>'
    venue_name = {'ISPRS Journal of Photogrammetry and Remote Sensing': 'ISPRS J PRS', 'IEEE Signal Processing Letters': 'IEEE SPL'}.get(event['venue'], event['venue'])
    venue = f'<strong>{e(venue_name)}</strong>'
    if paper['category'] == 'preprint':
        message = bi(f'📄 {news_link(subject_en)} is available as a preprint on {venue}.', f'📄 {news_link(subject_zh)}预印本发布于 {venue}。')
    else:
        message = bi(f'📄 {news_link(subject_en)} was published in {venue}.', f'📄 {news_link(subject_zh)}发表于 {venue}。')
    news_rows.append((event['date'], f'<li data-paper-id="{e(paper["id"])}" data-news-role="{role}"><time datetime="{e(event["date"])}">{e(event["date"].replace("-", "."))}</time><div>{message}</div></li>'))
# Announcements and publications share one timeline, limited to the latest five.
news = ['<ul class="news-list">'] + [row for _, row in sorted(news_rows, key=lambda item: item[0], reverse=True)[:5]] + ['</ul>']

cards = []
last_category = None
category_names = {'journal': ('Journal Papers', '期刊论文'), 'conference': ('Conference Papers', '会议论文'), 'preprint': ('Preprints', '预印本')}
for paper in p['papers']:
    if paper['category'] != last_category:
        last_category = paper['category']
        cards.append(f'<h3 class="publication-group" data-group="{last_category}">{bi(*category_names[last_category])}</h3>')
    authors = e(paper['authors'])
    authors = re.sub(r'(?<!\w)(Yu Wan|Y Wan|Y WAN|W Yu|万宇)(?!\w)', r'<strong>\1</strong>', authors)
    url = 'https://doi.org/' + paper['doi'] if paper.get('doi') else paper['scholar']
    venue = paper['venue']
    badge = ('ISPRS J PRS' if venue.startswith('ISPRS Journal') else
             'IEEE TGRS' if venue.startswith('IEEE Transactions on Geoscience and Remote Sensing') else
             'IEEE JSTARS' if 'Selected Topics' in venue else
             'IEEE SPL' if 'Signal Processing Letters' in venue else
             'IGARSS' if 'IGARSS' in venue else
             'ISPRS Annals' if 'ISPRS Annals' in venue else
             'Journal of Remote Sensing' if venue.startswith('Journal of Remote Sensing') else
             'Optics and Precision Engineering' if venue.startswith('Optics and Precision') else
             'Preprint' if paper['category'] == 'preprint' else paper.get('short', ''))
    figure = ''
    if paper.get('image'):
        full_image = paper.get('image_full', paper['image'])
        figure = f'''<a class="paper-image" data-figure="{e(paper['id'])}" href="assets/{e(full_image)}" target="_blank" rel="noopener noreferrer" aria-label="View figure: {e(paper['title'])}"><span class="venue-badge">{e(badge)}</span><img loading="lazy" decoding="async" src="assets/{e(paper['image'])}" alt="{e(paper.get('image_caption', paper['title']))}"><span class="figure-hint">{bi('View full-size figure ↗', '点击查看论文大图 ↗')}</span></a>'''
    links = f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">Paper ↗</a>'
    if paper.get('code'):
        links += f'<a href="{e(paper["code"])}" target="_blank" rel="noopener noreferrer">Code ↗</a>'
    links += f'<button class="cite" data-id="{e(paper["id"])}">BibTeX <span aria-hidden="true">❞</span></button>'
    cards.append(f'''<article class="paper {'with-image' if figure else ''}" data-selected="{str(paper['selected']).lower()}" data-year="{e(paper['year'])}" data-category="{paper['category']}">
      {figure}<div class="paper-body"><div class="paper-meta"><span>{e(paper.get('short', paper['category'].title()))}</span><span>{e(paper['year'])} / {e(paper['category'].upper())}</span></div>
      <h3><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(paper['title'])}</a></h3><p class="authors">{authors}</p><p class="venue">{e(paper['venue'])}</p><div class="paper-links">{links}</div></div></article>''')

template = (ROOT / 'template.html').read_text(encoding='utf-8')
replacements = {
    '{{NEWS}}': '\n'.join(news),
    '{{PAPERS}}': '\n'.join(cards),
    '{{EMAIL}}': e(p['email']),
    '{{SCHOLAR}}': e(p['scholar']),
    '{{DATA}}': json.dumps(p, ensure_ascii=False).replace('<', '\\u003c'),
    '{{CITATIONS}}': e(p['metrics']['citations']),
    '{{H_INDEX}}': e(p['metrics']['h_index']),
    '{{I10_INDEX}}': e(p['metrics']['i10_index']),
    '{{UPDATED}}': e(p['updated']),
}
for key, value in replacements.items():
    template = template.replace(key, value)
(ROOT / 'index.html').write_text(template, encoding='utf-8')
print(f'Built index.html with {len(p["papers"])} publications.')
