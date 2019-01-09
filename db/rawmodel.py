from django.template import Context, Template, loader
from django.db import connection

class RawModel(object):
    _columns = []
    _order_data = []
    _filter_data = {}
    _offset = None
    _limit = None
    _cursor = None
    _count = None
    _template_type = 0
    _count_template_type = 0
    _count_query = None

    def __init__(self,query, count_query = None):
        try:
            self._query = loader.get_template(query)
        except:
            self._query = Template(query)
            self._template_type = 1

        if count_query:
            try:
                self._count_query = loader.get_template(count_query)
            except:
                self._count_query = Template(count_query)
                self._count_template_type = 1

        self._columns = []
        self._order_data = []
        self._filter_data = {}
        self._offset = None
        self._limit = None
        self._cursor = None
        self._count = None

    @property
    def columns(self):
        return self._columns

    @property
    def query(self):
        return self.render()

    def __getitem__(self, key):
        if isinstance(key, slice):
            self._offset = key.start
            self._limit = key.stop - key.start
            # self._step = key.step
        else:
            self._offset = None
            self._limit = None
        return self

    @property
    def count_query(self):
        if self._count_query:
            if self._count_template_type:
                sql = self._count_query.render(Context(self._filter_data))
            else:
                sql = self._count_query.render(self._filter_data)
        else:
            sql = "select COUNT_BIG(*) from ({}) subquery".format(self.render(forcount=True))
        return sql

    def count(self):
        if self._count == None:
            with connection.cursor() as cursor:
                sql = self.count_query
                cursor.execute(sql)
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
        self._order_data.clear()
        for o in args:
            if not o in self._order_data:
                self._order_data.append(o)
        return self

    def render(self, forcount = False):
        # add Ordering to filters
        # filter_and_order = self._filter_data
        # if (not forcount) and self._order_data:
        #     filter_and_order.update({'order_by': "order by {} \n".format(','.join([str(e) for e in self._order_data]))})

        # Ordering and Filtering
        if self._template_type:
            sql = self._query.render(Context(self._filter_data))
        else:
            sql = self._query.render(self._filter_data)

        # Ordering
        if (not forcount):
            sql = "{} order by {} \n".format(sql,','.join([str(e) for e in self._order_data])) if self._order_data else sql

        # Offset & Limit
        if (not forcount) and self._order_data:
            sql = "{} OFFSET {} ROWS \n".format(sql,self._offset) if (self._offset != None) else sql
            sql = "{} FETCH NEXT {} ROWS ONLY \n".format(sql, self._limit) if (self._limit !=None) else sql

        return sql

    def open(self):
        self._cursor = connection.cursor()
        self._cursor.execute(self.render())
        self._columns = [col[0] for col in self._cursor.description] if self._cursor.description else None
        return self

    def exec(self):
        self.open()
        connection.commit()
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
