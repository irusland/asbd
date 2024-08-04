import asyncio
import re
from textwrap import dedent
from typing import Iterator, NamedTuple, Sequence

import asyncpg
from dotenv import load_dotenv
from jinja2 import Template

from api.data.clients.db.settings import (
    BaseDBDataClientSettings,
    DB1DataClientSettings,
    DB2DataClientSettings,
    DB3DataClientSettings,
)
from paths import CURRENT_DIR

CREATE_USERS_SQL_JINJA = CURRENT_DIR / 'db' / 'create_users.sql.jinja'

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


async def fill_tables(prompt: bool = True):
    matches = re.finditer(PATTERN, REQUIREMENTS)

    sources = get_sources(matches)

    with open(CREATE_USERS_SQL_JINJA, 'r') as f:
        template = Template(f.read())

    settings = (DB1DataClientSettings(), DB2DataClientSettings(), DB3DataClientSettings())
    rendered_sqls = render_create_sqls(sources, template)

    await execute_sqls(rendered_sqls, settings, prompt)


async def execute_sqls(rendered_sqls: list[str], settings: Sequence[BaseDBDataClientSettings], prompt: bool=True) -> None:
    for sql, setting in zip(rendered_sqls, settings, strict=True):
        print(sql)
        if prompt:
            input(f'Press Enter to execute sql statement into db: "{setting.url}"')
        conn = await asyncpg.connect(setting.url)
        await conn.execute(sql)
        await conn.close()


def render_create_sqls(sources: list[Source], template: str) -> list[str]:
    rendered_sqls = []
    for source in sources:
        data = {
            "source_number": source.source_number,
            "values": [
                (i, f'Test {i}') for start, stop in source.ranges for i in
                range(start, stop + 1)
            ]
        }
        rendered_sql = template.render(data)
        rendered_sqls.append(rendered_sql)
    return rendered_sqls


def get_sources(matches: Iterator[re.Match[str]]) -> list[Source]:
    sources = []
    for match in matches:
        source_number = int(match.group('source_number'))
        ranges = [
            (int(match.group(f'start{r}')), int(match.group(f'end{r}'))) for r in
            range(1, MAX_RANGES + 1)
        ]
        sources.append(Source(source_number=source_number, ranges=ranges))
    return sources


if __name__ == '__main__':
    load_dotenv()
    asyncio.get_event_loop().run_until_complete(fill_tables())
