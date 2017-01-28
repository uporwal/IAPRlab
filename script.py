#!/usr/bin/python
header1 = '{"index":{"_id":"'
header2 = '"}}'
str0 = '{ "name" : "'
str1 = '", "name_suggest" : { "input": "'
str2 = '", "weight" : '
str3 = ' } }'
target = open('aol.json', 'w')
target.truncate()

for line in open('aol.txt'):
	line = line.strip('\n')
	arr = line.split("\t")
	line1 = header1 + arr[0] + header2
	line2 = str0 + arr[1] + str1 + arr[1] + str2 + arr[2] + str3
	target.write(line1)
	target.write("\n")
	target.write(line2)
	target.write("\n")
target.close()
