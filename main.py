import os
import httpx
from datetime import datetime, timedelta

YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
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
# this is ran the following day at 3am or something
if day['Date'] != YESTERDAY:
    msg += ":red_square: Uli didn't journal today! Ask him why! Yell at him! @everyone"
else:
    date = day["Date"]
    # TODO: Get habits data from airtable, don't rely on EVERYTHING cruch
    if 'Daily' not in day or 'EVERYTHING' not in day['Daily']:
        msg += f":yellow_square: ({date}) Uli didn't complete all his habits, oh well. at least he journaled."
    else:
        msg += f":green_square: ({date}) Uli got up early, meditated, and did all his other habits today! Yay!"
    msg += f"\n\n{day['Journal']}"


print(msg)
resp = httpx.post(f'{WEBHOOK_URL}', data={'content': msg})
resp.raise_for_status()
print(resp.text)
