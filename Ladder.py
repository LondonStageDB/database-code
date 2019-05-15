#Ladder.py Python Program Created by Todd Hugie, July 2018
#This program updates the database AFTER the data has been loaded into the database.
#    The program goes through the ladder system and populates entries into the database cast table
#     properly creating the cast list, the performers and roles.  This program is only run
#     once when a new dataload is loaded into the database.


 #jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000  - Using Jupyter notebook for testing.
    #Make sure to start mysql first by going into MAMP and starting the server
    #I use MAMP and jupyter as the development platform for the London data.

import pymysql

cxn = pymysql.connect(host='localhost', port=3306, user='todhug', passwd='running', db='LondonStage')
cur = cxn.cursor()


#Query the AsSeeDate table
todd = 0
cur.execute("SELECT PerformanceId, TheatreCode, Ptype, AsSeeDate FROM AsSeeDate")
as_see_table = cur.fetchall()

for asSeeRow in as_see_table:
    perfIdAsSee=asSeeRow[0]
    theatreCode=asSeeRow[1]
    ptype=asSeeRow[2]
    asseedate=asSeeRow[3]

    cur.execute("SELECT EventId, EventDate, TheatreCode, Volume FROM Events where EventDate = %s and TheatreCode = %s", (asseedate, theatreCode))
    event_table = cur.fetchall()
    for eventrow in event_table:
        eventid = eventrow[0]
        eventdate = eventrow[1]
        eventtheatre = eventrow[2]
        eventvol = eventrow[3]

        cur.execute("SELECT PerformanceId FROM Performances Where PType = %s and EventID = %s", (ptype, eventid))
        performance_table = cur.fetchall()
        for performrow in performance_table:
            performceID = performrow[0]

            cur.execute("SELECT * FROM Cast Where performanceID = %s", (performceID))
            RolesOld = cur.fetchall()

            for roleRow1 in RolesOld:
                perfidOld=roleRow1[0]
                roleOld=roleRow1[1]
                performerOld=roleRow1[2]

            cur.execute("SELECT * FROM Cast Where performanceID = %s", (perfIdAsSee))
            RolesNew = cur.fetchall()


            for roleRow2 in RolesOld:
                isThere = "no"
                print (roleRow2[1], roleRow2[2])
                perfidOld = roleRow2[1]
                roleOld=roleRow2[2]
                performerOld=roleRow2[3]

                for roleRow3 in RolesNew:
                    perfidNew = roleRow3[1]
                    roleNew=roleRow3[2]
                    performerNew=roleRow3[3]

                    if roleOld == roleNew:
                        isThere = "yes"

                if isThere == "no":
                    if ("Prologue" not in roleOld) and ("prologue" not in roleOld) and ("Epilogue" not in roleOld) and ("epilogue" not in roleOld):
#                        print ("inserting ", perfIdAsSee, roleOld, performerOld)
                        sql = "insert into Cast (PerformanceId, Role, Performer) VALUES (%s, %s, %s)"
                        cur.execute(sql, (perfIdAsSee, roleOld, performerOld))
                        cxn.commit()




