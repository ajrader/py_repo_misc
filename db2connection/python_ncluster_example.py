#!/opt/discoverytools/anaconda/bin/python2.7

import getpass
import jaydebeapi

JDBC_PATH='/usr/aster/noarch-ncluster-jdbc-driver.jar'

USER = getpass.getuser()
PASSWORD = getpass.getpass()
DATASOURCE = 'jdbc:ncluster://ap74qn12.opr.statefarm.org:2406/ncprddb'

# Open a connection
conn = jaydebeapi.connect(
  'com.asterdata.ncluster.Driver',
  [DATASOURCE, USER, PASSWORD],
  JDBC_PATH)


#### !!!! WARNING - my nCluster access is not working, so these queries are invaled
#### To properly test things, you need to insert a valid query

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



