import os
from rich import print
import httpx
from datetime import datetime

TODAY = datetime.now().strftime('%Y-%m-%d')
AIRTABLE_URL="https://api.airtable.com/v0/appq1TYckaWsk1tgt"
AIRTABLE_API_KEY=os.environ['AIRTABLE_API_KEY']
WEBHOOK_URL=os.environ['WEBHOOK_URL']

resp = httpx.get(f'{AIRTABLE_URL}/Daily', params={
    'maxRecords': 1,
    'view': 'Grid view',
    'sort[0][field]': 'Date',
    'sort[0][direction]': 'desc',
}, headers={'Authorization': f'Bearer {AIRTABLE_API_KEY}'})
resp.raise_for_status()
day = resp.json()["records"][0]["fields"]

msg = ''
if day['Date'] != TODAY:
    msg += ":red_square: Uli didn't journal today! Ask him why! Yell at him! @everyone"
else:
    # TODO: Get habits data from airtable, don't rely on EVERYTHING cruch
    if 'EVERYTHING' not in day['Daily']:
        msg += ":red_square: Uli didn't do everything today! Ask him why! Yell at him! @everyone"
    else:
        msg += ":green_square: Uli got up early, meditated an hour, and did all his other habits today! Yay!"
        # TODO: Summary + journal link instead(?)
        msg += f"\nJournal: {day['Journal']}"

msg = ":green_square: Uli got up early, meditated an hour, and did all his other habits today! Yay!"
msg += f"\nJournal entry: {day['Journal']}"

resp = httpx.post(f'{WEBHOOK_URL}', data={'content': msg})
resp.raise_for_status()
print(resp.text)
