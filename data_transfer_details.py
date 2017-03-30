#!/usr/bin/python
import os
import csv
#Server Data transfer output file manupulation and combine in CSV format
#Data read from data_east.txt and data_west.txt
#Output file name Data_in_out_date.csv
# Bash command to collect data transfer output with vnstat and ssh loging from other servers
#for i in `cat /etc/hosts | grep vpc-prod-vertex | awk '{print $2}'` ;
#
#do
#
#ssh $i "hostname && vnstat -d | grep / | grep -v 'daily'|tail -2 |sed -n '1p'"
#
#done
#
#
elements1 = []
elements2 = []
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
region = 'None'
def data_sort(data, region):
    data = data.split(' ')
    if region == 'West':
        date = data[5].replace("/", "-")
     #   print data
        rx = data[8]
        rx_unit = data[9]
        rx = str(rx)+ str(rx_unit)
        tx = data[12]
        tx_unit = data[13]
        tx = str(tx)+ str(tx_unit)
        tot = data[18]
        tot_unit = data[19]
        tot = str(tot) + str(tot_unit)
    #    print date, rx, tx, tot
        return date, rx, tx, tot
    else:
        date = data[6].replace("/", "-")
        rx = data[10]
        rx_unit = data[11]
        rx = str(rx) + str(rx_unit)
        tx = data[14]
        tx_unit = data[15]
        tx = str(tx) + str(tx_unit)
        tot = data[18]
        tot_unit = data[19]
        tot = str(tot) + str(tot_unit)
        #   print date, rx, tx, tot
        return date, rx, tx, tot

def data_append(date, rx, tx, tot):  # function for data apend in list
    list2.append(date)
    list3.append(rx)
    list4.append(tx)
    list5.append(tot)

#DATA read for east
f = open('data_east.txt', 'r')
for row in f:
    elements1.append(row)
f.close()
print elements1
for row in elements1:

    if row[0:-1] == 'vpc-prod-vertex-trackers-api01':
        pass
    elif row[0:8] == 'vpc-prod':
        host = row[0:-1]
#        print host
        list1.append(host)
    else:
        date, rx, tx, tot = data_sort(row, region)
        data_append(date, rx, tx, tot)

#Data read for west
region = 'West'
w = open('data_west.txt', 'r')
for row in w:
    elements2.append(row)
w.close()

#print elements
for row in elements2:
    if row[0:8] == 'vpc-prod':
        host = row[0:-1]
#        print host
        list1.append(host)
    else:
        date, rx, tx, tot = data_sort(row, region)
        data_append(date, rx, tx, tot)

print elements2
end = len(list2)
print end, list2[0]

fName = 'Data_in_out_'+list2[0]+'.csv'
# create CSV file
try:
    print "Old file removed"
    os.remove(fName)  # Remove old file to clear file
except Exception as e:
    print 'Warning:', e
#Write CSV

f = open(fName, 'wb+')
fieldnames = ['DATE', 'Server Name', 'Data IN', 'Data OUT',	'Total']
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()

for i in range(end):
    print list1[i], list2[i], list3[i], list4[i], list5[i]
    #print list1[i]
    writer.writerow({'DATE': list2[i], 'Server Name': list1[i], 'Data IN': list3[i], 'Data OUT': list4[i], 'Total':list5[i]})
f.close()




