#!/opt/discoverytools/anaconda/bin/python2.7

# This uses the PyDB2 package
import DB2

USER = 'kes1'
PASSWORD = ''
DATASOURCE = 'FDW2P'

# Open a connection
conn = DB2.connect(dsn=DATASOURCE, uid=USER, pwd=PASSWORD)

# Get a cursor, which allows buffered fetching of rows
curs = conn.cursor()
curs.execute('SELECT LOS_EST_DIM_ID FROM FDWAE.LOS_EST_VW FETCH FIRST 10 ROWS ONLY')

# curs.fetchall() will fetch all of the results
rows = curs.fetchall()
for rownum, r in enumerate(rows):
    print rownum,":",repr(r)

# Close cursors when you're done
curs.close()


# Cursors can be used to iterate through large requests
curs = conn.cursor()
# Note the lack of a limit on this query
curs.execute('SELECT LOS_EST_DIM_ID FROM FDWAE.LOS_EST_VW')
rows = curs.fetchmany(size=2)
for rownum, r in enumerate(rows):
    print rownum,":",repr(r)
curs.close()

# Connections must be closed also
conn.close()



