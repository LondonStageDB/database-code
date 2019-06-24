'''This program was written by Todd Hugie and Derek Miller on Mar-Jun, 2018
  This program will take the semi formatted output file from Todd Hugie's program that created the LondonFinal.txt file,
  which formated and cleaned up the data getting it ready for input into a relational
  database.  At the time I documented this the program that creates the LondonFinal.txt file is called
  LondonFormatEverythingMay112019.py

  This program (LondonLoadDatabaseMayOthersZ.py will create txt files that then will be put directly into the tables of
  the database. Tried using the write and CSV files but the , and " throughout the data caused major
  problems.  The print statement worked much better.  I use a function called pandas to help properly populate Season data into
  the events table.  The Season data is something that wasn't created in the original 1970s data.  It is something extra we
  worked on with the grant we received in 2018.

'''
import csv, re, datetime, string, pandas
import pandas as season

#writes out results to csv files in a subfolder

#In the first set of writes we create the Event CVS table.
        #This also sets volume.  Duplicate theatre codes were created in the London database.  These
        #  duplicate theatre codes had different theatres depending on year.  Mattie Burkert identified
        #  by year which theatre codes go with which theatre names.  The program assigns an event counter
        #  and Mattie matched up the event counter ranges a new field called volume.  In the database the
        #  theatre table contains the theatre code, volume, and theatre name.

def writer():         #afer processing the data the output is piped and written ready for database import
    with open('events.txt','w') as f:
        volcount = 1
        yr1 = "0"
        previousyr2 = "0"
        prevvolume = "0"


        for e in events:    #This is how we define the volume. We found the last event of each volume. Important to find the correct theatre name
            if (e[1] != "17000925" and volcount == 1) or (e[1] == "17000800" and e[2] == "bf"):
                volume = 1
            elif e[1] == "17000925":
                volcount = 2

            if (e[1] != "17290911" and volcount == 2) or (e[1] == "17290915" and e[2] == "sf"):
                volume = 2;
            elif e[1] == "17290911":
                volcount =3

            if (e[1] != "17470909" and volcount == 3) or (e[1] == "17470828" and e[2] == "smmf"):
                volume = 3;
            elif e[1] == "17470909":
                volcount =4

            if (e[1] != "17760921" and volcount == 4) or (e[1] == "17760923" and e[2] == "hay"):
                volume = 4;
            elif e[1] == "17760921":
                volcount = 5

            if (e[1] != "17760921" and volcount == 4) or (e[1] == "17760923" and e[2] == "hay" and volcount != 6):
                volume = 4;
            elif e[1] == "17760921" and e[2] == "dl":
                volcount = 6

            if volcount == 6:
                volume = 5;


#These next few lines are to figure out proper season boundaries.
            idhold = seasonyr[(e[1] == seasonyr['year2']) & (e[2] == seasonyr['Theatre2'])]
            if not idhold.empty:
                holdyr2=idhold.iloc[0:1, 3]
                previousyr2=holdyr2.iloc[0]


            idhold = seasonyr[(e[1] == seasonyr['year1']) & (e[2] == seasonyr['Theatre1'])]
            if not idhold.empty:
                holdyr1=idhold.iloc[0:1, 1]  #pull out yr1 from the pandas
                yr1=holdyr1.iloc[0]
                holdtheat1=idhold.iloc[0:1, 2]
                theat1=holdtheat1.iloc[0]

                if yr1 == e[1] and theat1 == e[2]:
                    holdvol=idhold.iloc[0:1, 5]
                    prevvolume = holdvol.iloc[0]
                    pass
            else:
                idhold = seasonyr[(e[1] >= seasonyr['year1']) & (e[1] <= seasonyr['year2'])]
                holdseason=idhold.iloc[0:1, 0]  #pull out season from the pandas
                seasn=holdseason.iloc[0]
                holdvol=idhold.iloc[0:1,5]
                volume=holdvol.iloc[0]

            holdseason=idhold.iloc[0:1, 0]  #pull out season from the pandas
            seasn=holdseason.iloc[0]
            holdyr1=idhold.iloc[0:1, 1]  #pull out yr1 from the pandas
            yr1=holdyr1.iloc[0]

            holdtheat1=idhold.iloc[0:1, 2]
            theat1=holdtheat1.iloc[0]

            holdyr2=idhold.iloc[0:1, 3]
            yr2=holdyr2.iloc[0]

            holdtheat2=idhold.iloc[0:1, 4]
            theat2=holdtheat2.iloc[0]

            holdvol=idhold.iloc[0:1,5]
            volume=holdvol.iloc[0]


            if e[0] in comments:
                print (e[0],"|",e[1],"|",e[2],"|",prevvolume,"|",seasn,"|",e[3],"|",comments[e[0]],"|",xrecord[e[0]].rstrip(),"|",zrecord[e[0]], sep="", end="", file=f)
            else:
                 print (e[0],"|",e[1],"|",e[2],"|",prevvolume,"|",seasn,"|",e[3],"|","","|",xrecord[e[0]].rstrip(),"|",zrecord[e[0]], sep="", end="", file=f)


    with open('performances.txt','w') as f:
        for p in performances:
            print (p[0],"|",p[1],"|",p[2],"|",p[3],"|",p[4],"|",p[7],"|",p[5],"|",p[6], sep="", file=f)


#    with open('works.txt','w') as f:
#        f.write('w_performanceID,title,author,season\n')
#        for w in works:
#            f.write('{},"{}","{}","{}"\n'.format(w[0],"title","author","season"))
#            print (w[0],"|","title","|","author","|","season", sep="", file=f)

    with open('cast.txt','w') as f:
        for r in roles:
            if r[2][-1:] == "|":
                print (r[0],"|",r[1],"|",r[2][:-1], sep="", file=f)
            else:
                print (r[0],"|",r[1],"|",r[2], sep="", file=f)

    with open('asdate.txt','w') as f:
        for d in asSee:
            print (d[0],"|",d[1],"|",d[2],"|",d[3],"|",d[4], sep="", file=f)


# gets an event, defined as a date and theater combination, along with a unique ID number
def getEvent(e):
    regex_date_theater = re.search(r'\*\w(\d{4}) (\d{1,2}) (\d{1,2}) ([a-zA-Z\'@/&\-]*)',e)
   # date = datetime.date(int(regex_date_theater.group(1)),int(regex_date_theater.group(2)),int(regex_date_theater.group(3)))
    date = (regex_date_theater.group(1))+(regex_date_theater.group(2))+(regex_date_theater.group(3))
    theatre = regex_date_theater.group(4)

    regex_hathi = re.search(r'\bhathi\b',e)

    if regex_hathi:
        hathi = "hathi"
    else:
        hathi = ""

    return (date,theatre,hathi)

# gets *p (mainpiece) and mainpiece comments
def getPContent(e):
    regex_content = re.search(r'\*\w\d{4} \d{1,2} \d{1,2} [a-zA-Z\'@/&\-.]* (.*?)(\.|!|\?)( |)(.*)',e)
    work = regex_content.group(1)



    if regex_content.group(4)[-7:] == "|hathi|":
       cast = regex_content.group(4)[:-6]            #strip Hathi out of *p records
    else:
       cast = regex_content.group(4)

    if regex_content.group(4)[-1:] != "|":             #A few records didn't end with a |.  Need it for import to DB
        cast = regex_content.group(4) + "|"

#         Take out ^ carrot character from the cast if it exists
    work = work.replace('^','')
    cast = cast.replace('^','')
    work = string.capwords(work)  #Take off all caps if the work is all caps

    return (work,cast)



# gets *a (afterpiece) and afterpiece comments
def getAContent(e):
    try:
#        regex_content = re.search(r'\*\w\d{4} \d{1,2} \d{1,2} (.*?)(\.|!|\?)( |)(.*)',e)
        regex_content = re.search(r'\*\w\d{4} \d{1,2} \d{1,2} [a-zA-Z\'@/&\-.]* (.*?)(\.|!|\?)( |)(.*)',e)
        work = regex_content.group(1)



        if regex_content.group(4)[-7:] == "|hathi|":
            cast = regex_content.group(4)[:-6]            #strip Hathi out of records
        else:
            cast = regex_content.group(4)

        if regex_content.group(4)[-1:] != "|":             #A few records didn't end with a |.  Need it for import to DB
            cast = regex_content.group(4) + "|"

#         Take out ^ carrot character from the cast if it exists
        work = work.replace('^','')
        cast = cast.replace('^','')
#        work = string.capwords(work)  #Take off all caps if the work is all caps

        return (work,cast)
    except:
        return re.search(r'\*\w\d{4} \d{1,2} \d{1,2} (.*)',e),None


# gets content for all other entry types
def getContent(e):
    regex_content = re.search(r'\*(\w)\d{4} \d{1,2} \d{1,2} [a-zA-Z\'@/&\-.]* (.*)',e)
    entry_type = regex_content.group(1)
    content = regex_content.group(2)
    return entry_type,content

# gets the asdates separated properly
def getAsSee(e):
    regex_as_date = re.findall(r'\^(\w\w\d{8}\^)',e)
    asdatindex = []
    i=0

    for asda in regex_as_date:
        asdatindex = regex_as_date
        if asdatindex[i][0:2] == "As" or asdatindex[i][0:2] == "as":
            dateType = "As"
            asSeeDate = asdatindex[i][2:10]
            return (dateType,asSeeDate)
        i=+1


# gets a rough cast list, if possible
def getRoles(performanceID,cast):
    i = 0
    c = 0
    firsttime = "1"
    castlistcomment = ""
    commentgood = ""
    isPage = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"] #Looking for a page reference
    performers = ""
    howmany = len(cast)
    character=""
    restOfComment=""
    commentP=""


    for i in range(howmany):

        if cast[i] == "-" and not cast[i-1] in isPage and not cast[i + 1] in isPage and i > 1:  #example 1|5  don't process as a cast list.
 #           Loop backwards through commentP

            c = i
            commentgood = cast[0:c]

            while True:
                c = c-1

#                if (cast[c] == ")") and (cast[c] == "-"):     #Ignore comments within a cast.
                if cast[c] == ")":
                    while True:
                        c=c-1
                        if cast[c] == "(" or c < 0:     #ADDED THIS c < 0 on 8/20/2018.  For some reason c went < 0 causing a crash.
                            break

                if re.search('[^a-zA-Z0-9<>/@_\s\']', commentgood[c-1]) or c == 1:  #look for a special character. It is start of cast.
                    commentgood = cast[0:c-1]

                    character = cast[c:i]    #character
                    if firsttime == "1":
                        commentP = cast[0:-1]
                        firsttime = "2"
                        if "hathi" in cast:
                            character = cast[c-1:i]  #Put in here if Hathi nested If statement
#                        else:
#                            character = cast[c:i]

#                    character = cast[c:i]    #character

#   NOTE: TO MYSELF  Took out the next two but added the next five sentences to fix a bug  6/11/2019
#                    if "but " in character:      #Take out but in character list.
#                        character = character[4:]    #so take the first 4 character out.

                    if "but " in character:      #Take out but in character list.
                        if character [:6] == ", but ":
                            character = character[5:]#so take the first 5 characters out.
                        elif character[11:19] == "but with":
                            character = character[20:] #take out the first 15 characters.
                        elif character[11:14] == "but":
                            character = character[14:]
                        else:
                            character = character[4:]

                    if "(" in character:             #Take out comments that are embedded in parentheses within the cast list.
                        s=character.index("(")
                        character = character[:s]

                    castlistcomment = castlistcomment + cast[c-1:i] #Added 4/9/2019
#                    castlistcomment = castlistcomment + cast[c:i]   #out 4/9/2019

                    c=i
                    while (cast[i] != ";" and (cast[i] != "[") and (cast[i] != "]")):
                        i +=1
                        performers = cast[i]
                        if i+1 == len(cast):
                            break
                    performers = cast[c+1:i]


#                    castlistcomment = castlistcomment + cast[c:i] + ";"#out on 4/9/2019
                    castlistcomment = castlistcomment + cast[c:i]   #added on 4/9/2019

                    restOfCommenti = i

                    character = character.strip()    #strip out leading spaces
                    performers = performers.strip() #strip out leading spaces

                    if "(" in performers:             #Take out comments that are embedded in parentheses
                        s=performers.index("(")
                        performers = performers[:s]

                    if ".hathi" in performers:        #Take out .hathi from performers if it exists
                        s=performers.index(".hathi")
                        performers = performers[:s]

#                    if character[0] == ",":  #if first character is a , take it out
#                        character = character[1:]

                    if performers != "_" and performers != "_%" and performers != "_.":
                        roles.append ((performanceID,character,performers))

                    break

                if i+1 == len(cast):
                    break

            i += 1

    if firsttime == "2":
        restOfComment = cast[restOfCommenti+1:i+1]
        commentP = commentP + restOfComment


    commentgood = cast

    if commentP == "":
        commentP = commentgood

    if commentP == "|":           #There is no data in commentP so take out | character.
        commentP = ""

    if len(commentP) > 0:
        if commentP[-1] == "|":       #Take out | at end of commentP
            commentP = commentP[0:-1]


    if castlistcomment != "":
        castlistcomment = castlistcomment[0:-1] + "."

    if len(castlistcomment) > 0:
        if castlistcomment[0] == ",":
            castlistcomment = castlistcomment[1:]

    if "hathi" in castlistcomment:
        castlistcomment = castlistcomment.replace(".hathi", "")

    if ".hathi" in commentP:
        commentP = commentP.replace(".hathi", "")


    return (character,performers,commentP,castlistcomment)


#Start main part of the program here.

#Create a Pandas List.  This defines seasons and volume years.  We decided
#     to put this long list inside the program for preservation reasons.
#     We thought it would be better preserved than having this list as it's own
#     file or spreadsheet.   This might not be best practice but it is best for
#     preservation.  The first column is the volume, the last is the season.
#     Both the season and volume will be moved into the database.  The rest of the
#     data helps us determine what gets put into the volume and season for those records
#     based on the date and theatre code of the event.
#   Here are the column headings,
#       ['Volume','Begin Year','Begin Theatre','End Year',' End Theatre','Season']

LondonList =[["1","16591029","city","16600913","sf","1659-1660"],
["1","16600913","none","16610905","sf","1660-1661"],
["1","16610906","vere","16620823","thames","1661-1662"],
["1","16620900","none","16630904","bf","1662-1663"],
["1","16631000","lif","16640907","bf","1663-1664"],
["1","16640910","lif","16650807","bf","1664-1665"],
["1","16660319","bridges","16661010","moorfields","1665-1666"],
["1","16661011","atcourt","16670906","bf","1666-1667"],
["1","16670909","none","16680907","bf","1667-1668"],
["1","16680900","none","16690800","bridges","1668-1669"],
["1","16690900","none","16700800","bridges","1669-1670"],
["1","16700900","lif","16710800","bridges","1670-1671"],
["1","16710900","lif","16720831","dg","1671-1672"],
["1","16720900","dg","16730912","none","1672-1673"],
["1","16730904","wf","16740800","dg","1673-1674"],
["1","16740900","dg","16750903","bf","1674-1675"],
["1","16750924","dg","16760803","dg","1675-1676"],
["1","16760900","dg","16770831","bf","1676-1677"],
["1","16770900","dg","16780620","mth","1677-1678"],
["1","16780900","dg","16790903","bf","1678-1679"],
["1","16790900","dg","16800900","sf","1679-1680"],
["1","16800900","dg","16810909","bf","1680-1681"],
["1","16810900","dg","16820912","sf","1681-1682"],
["1","16821009","dlordg","16830831","dlordg","1682-1683"],
["1","16830900","dlordg","16840906","bforsf","1683-1684"],
["1","16840900","dl","16850826","bf","1684-1685"],
["1","16850900","dlordg","16860800","bf","1685-1686"],
["1","16860900","dlordg","16870724","none","1686-1687"],
["1","16870900","dlordg","16880800","bf","1687-1688"],
["1","16880900","dlordg","16890826","bf","1688-1689"],
["1","16890900","dlordg","16900908","none","1689-1690"],
["1","16900900","none","16910813","none","1690-1691"],
["1","16910900","bg","16920913","sf","1691-1692"],
["1","16921000","none","16930907","sf","1692-1693"],
["1","16931000","dlordg","16940905","bf","1693-1694"],
["1","16940912","dlordg","16950900","sf","1694-1695"],
["1","16950900","lif","16960905","sf","1695-1696"],
["1","16960900","dl","16970824","bf","1696-1697"],
["1","16970900","dl","16980917","sf","1697-1698"],
["1","16981010","dldg","16990830","bf","1698-1699"],
["1","16990900","stjames","17000831","bf","1699-1700"],
["2","17000925","lif","17010825","ha","1700-1701"],
["2","17010908","riw","17020831","bf","1701-1702"],
["2","17020918","dl","17030823","bf","1702-1703"],
["2","17030921","lif","17040823","dl","1703-1704"],
["2","17040911","dl","17050827","bf","1704-1705"],
["2","17050912","lif","17060827","bf","1705-1706"],
["2","17061015","queen's","17070830","bf","1706-1707"],
["2","17071011","queen's","17080804","dl","1707-1708"],
["2","17080826","dl","17090825","sh","1708-1709"],
["2","17090903","ha","17100930","gr","1709-1710"],
["2","17101004","queen's","17110920","gr","1710-1711"],
["2","17110922","dl","17120826","dl","1711-1712"],
["2","17120920","dl","17130627","haw","1712-1713"],
["2","17130922","dl","17140831","sf","1713-1714"],
["2","17140921","dl","17150915","sf","1714-1715"],
["2","17150927","lif","17160925","sf","1715-1716"],
["2","17160929","dl","17170925","sf","1716-1717"],
["2","17170928","dl","17180906","sf","1717-1718"],
["2","17180920","dl","17190905","b-l","1718-1719"],
["2","17190912","dl","17200905","sf","1719-1720"],
["2","17200910","dl","17210908","sf","1720-1721"],
["2","17210909","dl","17220924","sf","1721-1722"],
["2","17220908","dl","17230925","sou","1722-1723"],
["2","17230914","dl","17240907","sf","1723-1724"],
["2","17240912","dl","17250908","sf","1724-1725"],
["2","17250904","dl","17260908","sf","1725-1726"],
["2","17260903","dl","17270823","bf","1726-1727"],
["2","17270907","dl","17280906","sf","1727-1728"],
["2","17280907","dl","17290915","sf","1728-1729"],
["3","17290911","dl","17300914","sf","1729-1730"],
["3","17300912","dl","17310908","sf","1730-1731"],
["3","17310917","lif","17320911","sf","1731-1732"],
["3","17320904","hay","17330910","sf","1732-1733"],
["3","17330910","gf","17340907","sf","1733-1734"],
["3","17340907","dl","17350905","lif","1734-1735"],
["3","17350901","dl","17360907","none","1735-1736"],
["3","17360826","dl","17370907","sf","1736-1737"],
["3","17370830","dl","17380905","sf","1737-1738"],
["3","17380907","dl","17390908","sf","1738-1739"],
["3","17390901","dl","17400909","sf","1739-1740"],
["3","17400906","dl","17410822","nwc","1740-1741"],
["3","17410905","dl","17420826","bf","1741-1742"],
["3","17420908","sf","17430823","bf","1742-1743"],
["3","17430908","sf","17440711","nwc","1743-1744"],
["3","17440828","hay","17450903","js","1744-1745"],
["3","17450919","dl","17460825","bf","1745-1746"],
["3","17460908","sf","17470828","smmf","1746-1747"],
["4","17470909","sf","17480824","bf","1747-1748"],
["4","17480905","hay","17490912","sf","1748-1749"],
["4","17490915","sf","17500820","nwsm","1749-1750"],
["4","17500907","sf","17510807","nwls","1750-1751"],
["4","17510905","nwls","17520811","tcjs","1751-1752"],
["4","17520916","dl","17530906","bf","1752-1753"],
["4","17530908","dl","17540906","bf","1753-1754"],
["4","17540910","hay","17550911","hay","1754-1755"],
["4","17550913","dl","17560906","bf","1755-1756"],
["4","17560918","dl","17570831","hay","1756-1757"],
["4","17570902","hay","17580919","marly","1757-1758"],
["4","17580902","bf","17590913","marly","1758-1759"],
["4","17590917","hay","17600911","hay","1759-1760"],
["4","17600903","bf","17610829","hay","1760-1761"],
["4","17610831","bf","17620917","hay","1761-1762"],
["4","17620918","dl","17630902","hay","1762-1763"],
["4","17630903","dl","17640914","hay","1763-1764"],
["4","17640915","dl","17650913","hay","1764-1765"],
["4","17650914","dl","17660919","king's","1765-1766"],
["4","17660920","dl","17670921","hay","1766-1767"],
["4","17670912","dl","17680917","king's","1767-1768"],
["4","17680917","dl","17690919","hay","1768-1769"],
["4","17690905","king's","17700921","marly","1769-1770"],
["4","17700922","dl","17710920","hay","1770-1771"],
["4","17710921","dl","17720918","hay","1771-1772"],
["4","17720919","dl","17730920","hay","1772-1773"],
["4","17730918","dl","17740916","hay","1773-1774"],
["4","17740917","dl","17750920","hay","1774-1775"],
["4","17750920","cg","17760923","hay","1775-1776"],
["5","17760921","dl","17770919","hay","1776-1777"],
["5","17770920","dl","17780916","hay","1777-1778"],
["5","17780917","dl","17790917","hay","1778-1779"],
["5","17790918","dl","17800915","hay","1779-1780"],
["5","17800916","dl","17810915","hay","1780-1781"],
["5","17810915","dl","17820920","hay","1781-1782"],
["5","17820917","dl","17830915","hay","1782-1783"],
["5","17830916","dl","17840915","hay","1783-1784"],
["5","17840916","dl","17850916","hay","1784-1785"],
["5","17850917","dl","17860915","hay","1785-1786"],
["5","17860916","dl","17870915","hay","1786-1787"],
["5","17870917","cg","17880915","hay","1787-1788"],
["5","17880913","dl","17890915","hay","1788-1789"],
["5","17890912","dl","17900915","hay","1789-1790"],
["5","17900916","dl","17910916","hay","1790-1791"],
["5","17910912","cg","17920915","hay","1791-1792"],
["5","17920915","dl","17930914","hay","1792-1793"],
["5","17930916","cg","17940917","hay","1793-1794"],
["5","17940915","cg","17950915","hay","1794-1795"],
["5","17950915","cg","17960917","hay","1795-1796"],
["5","17960919","cg","17970918","hay","1796-1797"],
["5","17970918","cg","17980917","hay","1797-1798"],
["5","17980915","dl","17990916","hay","1798-1799"],
["5","17990916","cg","18000916","hay","1799-1800"]]

seasonyr = season.DataFrame(LondonList, columns = ['Volume','year1','Theatre1','year2','Theatre2','Season'])

asSeeId = 0
volume = 0
event_counter = -1
volcount = 1
events = []

asSee = []

performance_counter = -1
performances = []

#works = []

roles = []
howlong = 0

commentgood = ""
comments = {}
zrecord = {}
xrecord = {}
commentP = ""
dateType = ""
asSeeDate = ""
#isPage = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]  Looking for a page reference

with open('LondonFinal.txt','r') as infile: #this file created from the LondonFormatEverythingMay112019.py program.
    for entry in infile:
        # get event, which is, essentially, n lines beginning with a *p line, it gets a unique ID and a theater and date
        # theater should eventually be related to a theaters table via a foreign key


        if re.search(r'^\*p',entry):
            event_counter += 1
            hathi = ""
            event = getEvent(entry)
            events.append((event_counter,event[0],event[1],event[2]))
            event_order = -1

        if re.search(r'^\*z',entry):
            zrecord[event_counter] = entry[2:]

        if re.search(r'^\*x',entry):
            xrecord[event_counter] = entry[2:]

        # separate out the type of entry [p,a,m,s,etc.] and the rest of the line's content
        if entry[:2] != "*z":
            if entry[:2] != "*x":
                entry_type, content = getContent(entry)

        # for all non-comment entries, create a new performance
        # performances have a performanceID, eventID (foreign key), order in the event, type of entry (p,m,s,etc.), and content

        if entry_type != 'c' and entry[:2] != "*z" and entry[:2] != "*x":
            performance_counter += 1
            event_order += 1

#            if entry_type == 'p' or entry_type == 'a': # for *p (mainpieces) or *a (afterpieces), parse out the work and the rest of the line's content
            if entry_type == 'p' and entry[:2] != "*z" and entry[:2] != "*x":
                work, cast = getPContent(entry)
                                    #See if there are As or See dates
                regex_as_date = re.findall(r'\^(\w\w\d{8}\^)',entry)
                try:
                    dateType = ""
                    asSeeDate = ""
                    if regex_as_date == re.findall(r'\^(\w\w\d{8}\^)',entry): # dateType,getSeeDate = getAsSee(entry)

                        dateType,asSeeDate = getAsSee(entry)
                        asSee.append((performance_counter,event[1],entry_type,dateType,asSeeDate))

                except:
                    pass
            else:
                work,cast = getAContent(entry)
                regex_as_date = re.findall(r'\^(\w\w\d{8}\^)',entry)
                if entry_type != 'p':
                    try:           #See if there are As or See dates
                        dateType = ""
                        asSeeDate = ""
                        if regex_as_date == re.findall(r'\^(\w\w\d{8}\^)',entry):
                                      #       dateType,getSeeDate = getAsSee(entry)
                            dateType,asSeeDate = getAsSee(entry)
                            asSee.append((performance_counter,event[1],entry_type,dateType,asSeeDate))

                    except:
                        pass

            character, performers, commentP, castlistcomment = getRoles(performance_counter,cast)


#                Take out the ^ carrot character. It is no longer needed and was cluttering the output  September 2018
            castlistcomment = castlistcomment.replace('^','')
            content = content.replace('^','')
            commentP = commentP.replace('^','')


            howlong = len(entry)
            if ("Comment." in entry and howlong < 55):  #added Sept 2018 - if there is only the word Comment in an *p then don't create performance record
                 pass
            else:
                 if content[-6:] == "hathi.":
#                     print ("Content 7", performance_counter,event_counter,entry_type,work,castlistcomment)
                     performances.append((performance_counter,event_counter,event_order,entry_type,work,castlistcomment,content[:-7],commentP))  # Take off last pipe character
                 else:
                     performances.append((performance_counter,event_counter,event_order,entry_type,work,castlistcomment,content[:-1],commentP))  # Take off |hathi|


#            else: # for all other performances, no further processing in this draft
#                commentP = ""
#                if content[-7:] == "hathi.":
#                    performances.append((performance_counter,event_counter,event_order,entry_type,"",castlistcomment,content[:-7],commentP)) #Take off last pipe character
#                else:
#                    performances.append((performance_counter,event_counter,event_order,entry_type,"",castlistcomment,content[:-1],commentP)) #Take off |hathi|

        elif entry_type == 'c': #for *c (comments), add the content directly to the entry itself)
            if "hathi." in content:
                content = content.replace("hathi.", "")

            if content[-7:] == "hathi.":
                comments[event_counter] = content[:-7]  #If hathi record strip out since it was included as it's own field above
            else:
                comments[event_counter] = content[:-1]  #Take out ending pipe to load into database.
writer()
