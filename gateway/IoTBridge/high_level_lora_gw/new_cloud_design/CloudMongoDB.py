#-------------------------------------------------------------------------------
# Copyright 2016 Congduc Pham, University of Pau, France.
# 
# Congduc.Pham@univ-pau.fr
#
# This file is part of the low-cost LoRa gateway developped at University of Pau
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with the program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

import os
import json
import time
import datetime
import sys
import re

global add_document, remove_if_new_month, mongodb_set_max_months
from MongoDB import add_document, remove_if_new_month, mongodb_set_max_months

#see how we can get additional information for the internal usage of the script
#
#name of json file containing the cloud declarations
cloud_filename = "clouds.json"

#enabled cloud array
_enabled_clouds = []

#open json file to retrieve enabled clouds
f = open(os.path.expanduser(cloud_filename),"r")
string = f.read()
f.close()
	
#change it into a python array
json_array = json.loads(string)

#retrieving all cloud declarations
clouds = json_array["clouds"]

#here we check for our own script entry
#
for cloud in clouds:
	if "CloudMongoDB.py" in cloud["script"]:
		mongodb_set_max_months(cloud["max_months_to_store"])
		print "MongoDB with max months to store is %d" % cloud["max_months_to_store"]


# main
# -------------------

def main(ldata, pdata, rdata, tdata, gwid):

	now = datetime.datetime.utcnow()
	
	# this is common code to process packet information provided by the main gateway script (i.e. post_processing_gw.py)
	# these information are provided in case you need them	
	arr = map(int,pdata.split(','))
	dst=arr[0]
	ptype=arr[1]				
	src=arr[2]
	seq=arr[3]
	datalen=arr[4]
	SNR=arr[5]
	RSSI=arr[6]
	
	arr = map(int,rdata.split(','))
	bw=arr[0]
	cr=arr[1]
	sf=arr[2]

	# this part depends on the syntax used by the end-device
	# we use: thingspeak_channel#thingspeak_field#TC/22.4/HU/85... 
	#		  ##TC/22.4/HU/85... or TC/22.4/HU/85... or thingspeak_channel##TC/22.4/HU/85... or #thingspeak_field#TC/22.4/HU/85... to use some default value
				
	# get number of '#' separator
	nsharp = ldata.count('#')			
	#no separator
	if nsharp==0:
		#will use default channel and field
		data=['','']
		
		#contains ['', '', "s1", s1value, "s2", s2value, ...]
		data_array = data + re.split("/", ldata)		
	elif nsharp==1:
		#only 1 separator
		
		data_array = re.split("#|/", ldata)
		
		#if the first item has length > 1 then we assume that it is a channel write key
		if len(data_array[0])>1:
			#insert '' to indicate default field
			data_array.insert(1,'');		
		else:
			#insert '' to indicate default channel
			data_array.insert(0,'');		
	else:
		#contains [channel, field, "s1", s1value, "s2", s2value, ...]
		data_array = re.split("#|/", ldata)	
		
	#just in case we have an ending CR or 0
	data_array[len(data_array)-1] = data_array[len(data_array)-1].replace('\n', '')
	data_array[len(data_array)-1] = data_array[len(data_array)-1].replace('\0', '')	
	
	#test if there are characters at the end of each value, then delete these characters
	i = 3
	while i < len(data_array) :
		while not data_array[i][len(data_array[i])-1].isdigit() :
			data_array[i] = data_array[i][:-1]
		i += 2

	print("MongoDB: removing obsolete entries")
	
	#check if new month
	remove_if_new_month(now)

	print("MongoDB: saving the document in the collection...")
	
	#saving data in a JSON var
	str_json_data = "{"
	#start from the first nomenclature
	iteration = 2
	while iteration < len(data_array)-1 :
		#last iteration, do not add "," at the end
		if iteration == len(data_array)-2 :
			str_json_data += "\""+data_array[iteration]+"\" : "+data_array[iteration+1]
		else :
			str_json_data += "\""+data_array[iteration]+"\" : "+data_array[iteration+1]+", "
		iteration += 2
	str_json_data += "}"

	#creating document to add
	doc = {
		"type" : ptype,
		"gateway_eui" : gwid, 
		"node_eui" : src,
		"snr" : SNR, 
		"rssi" : RSSI, 
		"cr" : cr, 
		"datarate" : "SF"+str(sf)+"BW"+str(bw),
		"time" : now,
		"data" : json.dumps(json.loads(str_json_data))
	}

	#adding the document
	add_document(doc)

	print("MongoDB: saving done")	
	
if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])	