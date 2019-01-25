import hashlib

from django.template import Context, Template, loader
from django.db import connection
from django.core.cache import cache

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
        self._cursor = connection.cursor()
        self._cursor.execute(self.render())
        self._columns = []
        return self

    def close(self):
        self._cursor.close()
        self._cursor = None
        self._count = None
        self._columns = []
        return self

    def fetchall(self):
        return [
            dict(zip(self._columns, row))
            for row in self._cursor.fetchall()
        ]


class CachedRawModel(RawModel):
    cache_default_timeout = 24*60*60
    _cached_data = None

    def get_query_hash(self, query):
        org_id_str = str(self._filter_data.get('org_id', 0))
        hash = org_id_str + '_' + hashlib.md5(query.encode('utf-8')).hexdigest()
        return hash

    def save_to_cache(self, query_hash, data):
        org_id = self._filter_data.get('org_id', 0)
        cache.set(query_hash, data, self.cache_default_timeout, version=org_id)

    def fetch_from_cache(self, query_hash):
        org_id = self._filter_data.get('org_id', 0)
        data = cache.get(query_hash, None, version=org_id)
        return data

    def open(self):
        query = self.render()
        self._query_hash = self.get_query_hash(query)
        self._cached_data = self.fetch_from_cache(self._query_hash)

        if self._cached_data:
            self._columns = self._cached_data['columns']
        else:
            self._cursor = connection.cursor()
            self._cursor.execute(query)
            self._columns = [col[0] for col in self._cursor.description] if self._cursor.description else None
        return self

    def fetchall(self):
        if self._cached_data:
            print('Fetch from CACHE {}'.format(self._query_hash))
            return self._cached_data['rows']
        else:
            rows = super().fetchall()
            self.save_to_cache(self._query_hash, {'columns':self._columns, 'rows':rows})
            print('Fetch from DBMS {}'.format(self._query_hash))
            return rows

    def close(self):
        if self._cached_data:
            self._cached_data = []
        else:
            self._cursor.close()
        self._cursor = None
        self._count = None
        self._columns = []
        return self

    def count(self):
        if self._count:
            return self._count

        sql = self.count_query
        query_hash = self.get_query_hash(sql)
        count = self.fetch_from_cache(query_hash)

        if count != None:
            self._count = count
            print('Count from CACHE {}'.format(query_hash))
        else:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                row = cursor.fetchone()
            self._count = row[0]
            self.save_to_cache(query_hash,self._count)
            print('Count from DBMS {}'.format(query_hash))

        return self._count


