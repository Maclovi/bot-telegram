import itertools

from sqlalchemy import Engine, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable


class DbToolSQLalchemy:
    '''Depended: sqlalchemy'''

    @classmethod
    def preview_table(cls, environ: dict, db='sql', start=1, limit=10) -> None:
        '''
        to works correct need to name classes like - 'UserOrm, BuyOrm'
        '''
        dict_globals = environ.copy().items()
        filter_globals = filter(lambda x: x[0].endswith('Orm'), dict_globals)
        skip_begin = itertools.islice(filter_globals, start - 1, None)
        output_result = itertools.islice(skip_begin, None, limit)
        for elems in output_result:
            default = CreateTable(elems[1].__table__)
            db_dict = {
                'sql': default,
                'psql': default.compile(dialect=postgresql.dialect()),
            }
            if db.lower() != 'all':
                print(db, db_dict.get(db))
            else:
                for k, v in db_dict.items():
                    print(k, v)

    @classmethod
    def check_connect(cls, engine: Engine) -> None:
        with engine.begin() as conn:
            res = conn.execute(text("SELECT VERSION()"))
            print(res.scalar())
