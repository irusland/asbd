import asyncio
import re
from textwrap import dedent
from typing import NamedTuple

import asyncpg
from jinja2 import Template

from api.data.clients.db.settings import (
    DB1DataClientSettings, DB2DataClientSettings,
    DB3DataClientSettings,
)
from dotenv import load_dotenv

CREATE_USERS_SQL_JINJA = 'create_users.sql.jinja'

REQUIREMENTS = dedent("""\
- 1st source: IDs 1-10, 31-40;
- 2nd source: IDs 11-20, 41-50; 
- 3rd source: IDs 21-30, 51-60;
""")
MAX_RANGES = 2

PATTERN = re.compile(r'(?P<source_number>\d+)(?:st|nd|rd|th) source: IDs (?P<start1>\d+)-(?P<end1>\d+), (?P<start2>\d+)-(?P<end2>\d+);')


class Source(NamedTuple):
    source_number: int
    ranges: list[tuple[int, int]]


async def main():
    matches = re.finditer(PATTERN, REQUIREMENTS)

    sources = []
    for match in matches:
        source_number = int(match.group('source_number'))
        ranges = [
            (int(match.group(f'start{r}')), int(match.group(f'end{r}'))) for r in range(1,MAX_RANGES+1)
        ]
        sources.append(Source(source_number=source_number, ranges=ranges))

    with open(CREATE_USERS_SQL_JINJA, 'r') as f:
        template = Template(f.read())

    settings = (DB1DataClientSettings(), DB2DataClientSettings(), DB3DataClientSettings())

    for source, setting in zip(sources, settings):
        data = {
            "source_number": source.source_number,
            "values": [
                (i, f'Test {i}') for start, stop in source.ranges for i in range(start, stop+1)
            ]
        }
        rendered_sql = template.render(
            data
        )
        print(rendered_sql)
        input(f'Press Enter to execute sql statement into db: "{setting.url}"')
        conn = await asyncpg.connect(setting.url)

        await conn.execute(rendered_sql)

        await conn.close()


if __name__ == '__main__':
    load_dotenv()
    asyncio.get_event_loop().run_until_complete(main())
