# Title: Python script to fix encoding problems in the London Stage Project raw data files.
# 
# Author: Derek Miller, Harvard University
# Contact: dmiller(at)fas.harvard.edu
# Date: February 19, 2017

# In the LSP raw data files, each entry begins \*p or \*c or \*a, etc. Those two characters (the asterisk to indicate the start of an entry, and the letter to indicate the category of data entered) should be followed by a date. Indeed, they are followed by a date in a number of the files. But in many of the files where the date should be we find instead two odd characters. Those characters are, in fact, dates, but *encoded* by a rather straightforward system which requires us to convert those two characters into dates by reading their hex values. The encoding system works as follows:
# 
# In the first file, 1659.NPK, the first entry with a known date (not just a known month) reads:
# 
# `*p<0x01><0x3D>city`
# 
# That date is October 29, 1659 (as printed in *The London Stage*).
# 
# The second hex character is the important one. Each month gets its own hex range of 00-1F, 20-3F, 40-5F, etc. In hex, of course, the range <0x00> to <0x1F> is equal to 0-31 in base 10. Thus each hex range encompasses all the possible days of a month. Any month-hex ending in zero (<0x20>, for example) is an unknown date within the month. The first few performances listed in 1659.NPK took place on unknown days in September (hex range <0x00> to <0x1F>). And the first dated performance was the next month, October (range <0x20> to <0x3F>) on the 29th (<0x3D> is 61, which becomes 29 in mod 32).
# 
# When you hit FF after eight months, you increase the *first* hex character by one (so, from <0x01> to <0x02>). Thus the date encoding system can be calculated quite easily once you know that <0x01><0x01> is September 1, 1659. Every other month's range for the remainder of the series is calcuable from there.
# 
# (Note: this script should be run in a directory that includes the subfolder LSP_data, which has all the .NPK files, and has a new subfolder LSP_data/converted_NPK_files, to which we'll write our unencoded files.)


#Create a dictionary of tuples of two hex characters into date values
#Call the first hex character the tally_hex (it keeps a tally of which month we're on, starting with September, 1659).
#Call the second hex character the date_hex, which tells us the day of the month in modulo 32

date_dictionary = {} #our dictionary
year = 1659 #our starting year
month = 8 #one less than our starting month, because month++ in our code

for t in range(1,256): # our starting tally value, remember, is <0x01>
    # the tally_hex increases by one after the date_hex goes from <0x00> to <0xFF>, or 0 to 256
    tally_hex = hex(t) 
    for d in range(0, 256): #calculate each date from 0 to 256 (or <0x00> to <0xFF>)
        date_hex = hex(d)
        day = d%32
        if day == 0: #increase the month each time we run through 32 days
            if month == 12: #increase the year if the current month is December
                month = 1
                year += 1
            else:
                month += 1
        date_dictionary[(tally_hex,date_hex)] = (year,month,day) #enter our value in the dictionary



#Test our known value: <0x01><0x3D> should be October 29, 1659
#Remember, <0x01> = 1 in base 10 and <0x3D> = 3*16 + 13 = 61
print(date_dictionary[(hex(1),hex(61))])


#Now we need to fix the files, which are currently in the folder LSP_data. 


import os, re, datetime
import binascii as ba

def converter(f,file_name): #function to convert dates
    
    fixed_entries = [] #this is where we'll put our entries with converted dates
    hexed_file = ba.hexlify(f) #convert file entirely to hex, since line break character may also be hex encodings
    entries = hexed_file.split('20202a') #split file into entries, which open with two spaces (<0x20>) and an asterisk (<0x2a>)
    entries[0] = entries[0][2:] #each file starts with a leading asterisk, which we remove
    
    for i,e in enumerate(entries):
        fixed_entry = '*' + ba.unhexlify(e[:2]) #fixed_entry will be our properly formatted entry, starting with the entry type code (p, c, a, etc.), we'll convert it back from hex, too, and add the leading asterisk
        tally_hex = e[2:4] #the tally_hex and date_hex characters are the second and third hex values in each entry
        date_hex = e[4:6]
        try:
            date = date_dictionary[(hex(int(tally_hex,16)),hex(int(date_hex,16)))] # use dictionary to get date value
        except: #catch any errors and print the file name and entry number for later human checking
            date = ['','','']
            print file_name, i+1
        fixed_entry += '{} {} {} '.format(date[0],date[1],date[2]) # add our date value to our entry
        fixed_entry += ba.unhexlify(e[6:])
        fixed_entries.append(fixed_entry)
    return fixed_entries

#We'll make a new subfolder, converted_NPK_files, and put the fixed files there.
try:
    os.mkdir('LSP_data/converted_NPK_files')
except:
    print('Folder already exists')
#Our encoded files end with .NPK, so those are the files we need to worry about.
#Read in each file and send it to our converter function
for f in os.listdir('LSP_data'):
    if f[-3:] == 'NPK':
        converted_entries = converter(open('LSP_data/{}'.format(f),'r').read(),f)
        with open('LSP_data/converted_NPK_files/{}'.format(f),'w') as q: #Wre out to new NPK files in our subfolder
            for entry in converted_entries:
                q.write(entry)
                q.write('\n') #place each entry on its own line
#The output of this function indicates line numbers that need checking in the converted_NPK_files folder,
#because some kind of date processing error appeared in that entry. Those corrections must be done manually.
