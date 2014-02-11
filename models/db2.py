db2 = DAL('sqlite://storage.sqlite',pool_size=1, check_reserved=['all'])

db2.define_table('gerald', Field('name'), format='%(name)s')
#db2.gerald.insert(name = "New test String")

