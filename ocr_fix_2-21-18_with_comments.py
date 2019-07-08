# Title: Python script to format OCR data in 1730s and 1780s to accord with other entries
# 
# Author: Derek Miller, Harvard University
# Contact: dmiller(at)fas.harvard.edu
# Date: February 21, 2018
#
# This script operates on two sets of data, which represent OCR and then human-corrected performance entries from stretches of the 1730s and 1780s. These stretches were missing from the original files recovered from Schneider's London Stage Database.
# 
# The script loops over the entries, each of which is presented only as an event, and not parsed into individual elements (e.g., singing, comment). It splits the entry up into sub-events, and rewrites the file so that each subevent gets its own entry line, to accord with the remainder of the data set, as already parsed from the recovered LSD files.

# Import modules
import re
import codecs

#1730s

# Load file to correct as a list of rows
rows = []
with open('OCR_data_1733-1736_mb_2.20.18_dm_format_corrections.txt','r') as f:
    for row in f:
        try:
            rows.append(row)
        except:
            print(row)

# Define subevent categories that may be present
categories = r'singing and dancing|dancing|comment|entertainments|entertainment|monologue|ballet|instrumental|opera|trick|music|singing'

# Open revised file which will hold the results
with open('OCR_data_1733-1736_dm_2.21.18.txt','w') as f:

    # loop through extent rows
    for r in rows:

        # parse rows into elements, consisting of (1) type of entry, (2) date and venue, (3) content 
        first_regex = re.search(r'\*(\w)(\d{4} \d{1,2} \d{1,2} .*?)( .*)', r)
        try:
            date = first_regex.group(2)
            content = first_regex.group(3)
        except:
            print(r)
            break

        #if row is a performance event, split event into subevent elements, saved as a dictionary with the key being the subevent name
        if first_regex.group(1) == 'p': 
            second_regex = re.split(r'({})\.'.format(categories), content, flags=re.I) #split contents into list, each beginning with any of the named categories
            elements = {}
            key = 'root'
            for s in second_regex: # create dictionary entries for subevents
                if re.match(r'({})'.format(categories), s, flags=re.I):
                    key = s.lower()
                else:
                    elements[key] = s.lstrip().rstrip()
            if re.search(r'Also ', elements['root']): # repeat process for any subevents after "Also" to deal with afterpieces
                third_regex = re.split(r'Also ', elements['root'])
                elements['root'] = third_regex[0].rstrip().lstrip()
                for i,e in enumerate(third_regex[1:]):
                    elements['afterpiece{}'.format(i)] = third_regex[i+1].rstrip().lstrip()
                if i > 2:
                    print(r)
        else:# otherwise, the type of entry is a comment
            elements = {}
            elements['comment'] = content.lstrip().rstrip()

        # convert elements dictionary back into encoded form and write out to the new file
        for k in ['root','afterpiece0','afterpiece1','afterpiece2','music','singing and dancing','dancing','entertainments','singing','comment',
                 'entertainment','monologue','ballet','instrumental','opera','trick']:
            if k in elements:
                if k == 'root':
                    code = 'p'
                elif k=='monologue':
                    code = 'u'
                else:
                    code = k[0]
                if len(elements[k]) < 1:
                    entry = '.'
                else:
                    entry = elements[k]
                if k == 'singing and dancing':
                    f.write('*s{} .\n'.format(date))
                    code = 'd'
                f.write('*{}{} {}\n'.format(code,date,entry))

#1780s (see above for code explanation; modifications only noted here)

rows = []
with open('OCR_data_1781-1786_mb_2.20.18_dm_format_corrections.txt','r') as f:
    for row in f:
        try:
            rows.append(row)
        except:
            print(row)

categories = r'singing and dancing|dancing|comment|entertainments|entertainment|monologue|ballet|instrumental|opera|trick|music|singing'

with open('OCR_data_1781-1786_dm_2.21.18.txt','w') as f:

    for r in rows:
        first_regex = re.search(r'\*(\w)(\d{4} \d{1,2} \d{1,2} .*?)( .*)', r)
        try:
            date = first_regex.group(2)
            date_only = re.search(r'(\d{4} \d{1,2} \d{1,2})',date).group(1) # date information without venue info
            content = first_regex.group(3)
        except:
            print(r)
            break


        if first_regex.group(1) == 'p':
            second_regex = re.split(r'({})\.'.format(categories), content, flags=re.I)

            elements = {}
            key = 'root'
            for s in second_regex:
                if re.match(r'({})'.format(categories), s, flags=re.I):
                    key = s.lower()
                else:
                    elements[key] = s.lstrip().rstrip()
            if re.search(r'Also ', elements['root']):
                third_regex = re.split(r'Also ', elements['root'])
                elements['root'] = third_regex[0].rstrip().lstrip()
                for i,e in enumerate(third_regex[1:]):
                    elements['afterpiece{}'.format(i)] = third_regex[i+1].rstrip().lstrip()
                if i > 2:
                    print(r)
        else:
            elements = {}
            elements['comment'] = content.lstrip().rstrip()
        for k in ['root','afterpiece0','afterpiece1','afterpiece2','music','singing and dancing','dancing','entertainments','singing','comment',
                 'entertainment','monologue','ballet','instrumental','opera','trick']:
            if k in elements:
                if k == 'root':
                    code = 'p'
                elif k=='monologue':
                    code = 'u'
                else:
                    code = k[0]
                if len(elements[k]) < 1:
                    entry = '.'
                else:
                    entry = elements[k]
                if k == 'singing and dancing':
                    f.write('*s{} .\n'.format(date))
                    code = 'd'
                if code == 'p': # output includes full date information, if event is performance event
                    f.write('*{}{} {}\n'.format(code,date,entry))
                else: # if event is not performance, than exclude venue name from date information
                    f.write('*{}{} {}\n'.format(code,date_only,entry))
