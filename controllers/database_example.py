response.menu = [['Reg db2', False, URL('reg_db2')]]

def reg_db2():
	form = SQLFORM(db2.gerald).process()

	if form.accepted:
		response.flash = 'New Record Inserted'

	records = SQLTABLE(db2().select(db2.gerald.ALL), headers = 'fieldname:capitalize')

	return dict(form=form, records=records)
