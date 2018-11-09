from django.template import Context, Template
from django.db import connection

class RawModel(object):
    _query = ''
    _columns = []
    _order_data = []
    _filter_data = {}
    _offset = None
    _limit = None
    _cursor = None
    _count = None

    def __init__(self,query):
        self._query = query

    @property
    def columns(self):
        return self._columns

    @property
    def query(self):
        return self.render()

    def __getitem__(self, key):
        if isinstance(key, slice):
            self._offset = key.start
            self._limit = key.stop
            # self._step = key.step
        else:
            self._offset = None
            self._limit = None
        return self

    def count(self):
        if self._count == None:
            count_query = "select COUNT_BIG(*) from ({}) subquery".format(self.render(forcount=True))
            with connection.cursor() as cursor:
                cursor.execute(count_query)
                row = cursor.fetchone()
            self._count = row[0]
        return self._count

    def filter(self,**kwargs):
        for key in kwargs:
            self._filter_data[key] = kwargs[key]
        self._count = None
        return self

    def addfilters(self,filters):
        self._filter_data.update(filters)
        self._count = None
        return self

    def order_by(self, *args):
        for o in args:
            self._order_data.append(o)
        return self

    def render(self, forcount = False):
        t = Template(self._query)

        # Filtering
        sql = t.render(Context(self._filter_data))

        # Ordering
        if (not forcount):
            sql = "{} order by {} ".format(sql,','.join([str(e) for e in self._order_data])) if self._order_data else sql

        # Offset & Limit
        if (not forcount) and self._order_data:
            sql = "{} OFFSET {} ROWS \n".format(sql,self._offset) if (self._offset != None) else sql
            sql = "{} FETCH NEXT {} ROWS ONLY \n".format(sql, self._limit) if (self._limit !=None) else sql

        return sql

    def open(self):
        self._cursor = connection.cursor()
        self._cursor.execute(self.render())
        self._columns = [col[0] for col in self._cursor.description]
        return self

    def close(self):
        self._cursor.close()
        self._cursor = None
        self._count = None
        self._columns = []
        return self

    def fetchall(self):
        "Return all rows from a cursor as a dict"
        return [
            dict(zip(self._columns, row))
            for row in self._cursor.fetchall()
        ]
