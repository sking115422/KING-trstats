

#General Imports

import os
import statistics
import json

#Creating traceroute text file

json_list = []
json_list_all = []

num_times_run = 3

print('')
print ("Running traceroute " + str(num_times_run) + " times...")

for x in range(0, num_times_run):
    
    print('')
    print('Run ' + str(x + 1) + '...')

    website = 'google.com'
    cmd = 'traceroute ' + website + ' > trt.txt'
    cmd2 = 'traceroute ' + website

    os.system(cmd)

    #*******************************************************************************************

    #Parsing text file in .json format

    with open('trt.txt', 'r') as file:
        trt_text = file.read()

    trt_list = trt_text.splitlines()

    count = 0
    avg = None
    mx = None
    md = None
    mn = None
    hop = None
    hosts = None
    host_list = []
    lat_list = []

    for line in trt_list:

        count = count + 1

        each_list = line.split()

        while 'ms' in each_list:
            each_list.remove('ms')
        while '*' in each_list:
            each_list.remove('*')

    #     print(each_list)


        if len(each_list) == 6:

            hop = int(each_list[0])
            hosts = [each_list[1], each_list[2]]

            lat_list = [float(each_list[3]), float(each_list[4]), float(each_list[5])]

            avg = round(statistics.mean(lat_list), 3)
            mx = max(lat_list)
            md = round(statistics.median(lat_list), 3)
            mn = min(lat_list)


            json_dict ={'avg': avg,
                        'hop': hop,
                        'hosts': hosts,
                        'max': mx,
                        'med': md,
                        'min': mn}
            
            json_dict_all ={'hop': hop,
                            'lat': lat_list}

            json_list.append(json_dict)
            
            json_list_all.append(json_dict_all)


        elif len(each_list) == 5:

            hop = int(each_list[0])

            host_list = []
            host_list = [each_list[1], each_list[2]]

            lat_list = []
            lat_list = [float(each_list[3]), float(each_list[4])]

            avg = round(statistics.mean(lat_list), 3)
            mx = max(lat_list)
            md = round(statistics.median(lat_list), 3)
            mn = min(lat_list)

            json_dict = {'avg': avg,
                        'hop': hop,
                        'hosts': host_list,
                        'max': mx,
                        'med': md,
                        'min': mn}

            json_dict_all ={'hop': hop,
                            'lat': lat_list}

            json_list.append(json_dict)
            
            json_list_all.append(json_dict_all)


        elif len(each_list) == 4:

            if len(each_list[0]) < 3:

                hop = int(each_list[0])

                host_list = []
                host_list = [each_list[1], each_list[2]]

                lat_list = []
                lat_list = [float(each_list[3])]

                avg = round(statistics.mean(lat_list), 3)
                mx = max(lat_list)
                md = round(statistics.median(lat_list), 3)
                mn = min(lat_list)

                json_dict = {'avg': avg,
                            'hop': hop,
                            'hosts': host_list,
                            'max': mx,
                            'med': md,
                            'min': mn}
                
                json_dict_all ={'hop': hop,
                                'lat': lat_list}

                json_list.append(json_dict)
                
                json_list_all.append(json_dict_all)

            else:

                host_list.append(each_list[0])
                host_list.append(each_list[1])

                lat_list.append(float(each_list[2]))
                lat_list.append(float(each_list[3]))

                avg = round(statistics.mean(lat_list), 3)
                mx = max(lat_list)
                md = round(statistics.median(lat_list), 3)
                mn = min(lat_list)

                json_dict = {'avg': avg,
                            'hop': hop,
                            'hosts': host_list,
                            'max': mx,
                            'med': md,
                            'min': mn}
                
                json_dict_all ={'hop': hop,
                                'lat': lat_list}

                json_list.append(json_dict)
                
                json_list_all.append(json_dict_all)
                


        elif len(each_list) == 3:

                host_list.append(each_list[0])
                host_list.append(each_list[1])

                lat_list.append(float(each_list[2]))

                avg = round(statistics.mean(lat_list), 3)
                mx = max(lat_list)
                md = round(statistics.median(lat_list), 3)
                mn = min(lat_list)

                json_dict = {'avg': avg,
                            'hop': hop,
                            'hosts': host_list,
                            'max': mx,
                            'med': md,
                            'min': mn}
                
                json_dict_all ={'hop': hop,
                            'lat': lat_list}

                json_list.append(json_dict)
                
                json_list_all.append(json_dict_all)


        else:
            pass



    # print('')       
    # for one in json_list:
    #     print(one)

    #*******************************************************************************************

    #Removing extra entries json_list

    for row in range(0, len(json_list) + 1):
        try:
            if json_list[row].get('hop') == json_list[row + 1].get('hop'):
                json_list.remove(json_list[row])
        except:
            pass

    for row in range(0, len(json_list) + 1):
        try:
            if json_list[row].get('hop') == json_list[row + 1].get('hop'):
                json_list.remove(json_list[row])
        except:
            pass

#     print('')       
#     for one in json_list:
#         print(one)
        
    #*******************************************************************************************
    
    #Removing extra entries json_list_all

    for row in range(0, len(json_list_all) + 1):
        try:
            if json_list_all[row].get('hop') == json_list_all[row + 1].get('hop'):
                json_list_all.remove(json_list_all[row])
        except:
            pass

    for row in range(0, len(json_list_all) + 1):
        try:
            if json_list_all[row].get('hop') == json_list_all[row + 1].get('hop'):
                json_list_all.remove(json_list_all[row])
        except:
            pass
        
#     print('')       
#     for one in json_list_all:
#         print(one)

    print('Run ' + str(x + 1) + ' finished!')

print('')
print('Exporting json data...')

#Exporting data in json_list file

with open('trt_data.json', 'w') as f:
    json.dump(json_list, f)

#Exporting data in json_list_all file

with open('trt_data_all.json', 'w') as f:
    json.dump(json_list_all, f)

print('Export successful!')

#Imports for plotting data as boxplot

import pandas as pd
import plotly
pd.options.plotting.backend = "plotly"

# import seaborn as sns
# import matplotlib.pyplot as plt
# %matplotlib inline

print('')
print('Generating boxplots...')

#Creating boxplot for the average values for each number of hops each time traceroute was run

raw_data = pd.read_json('trt_data.json')

raw_data.head()

df = raw_data [['hop','avg']]

df_all = pd.DataFrame()

raw_data.head(100)

for hops in range(1, df.hop.max() + 1):
    df_by_hops = df[df.hop == hops][['avg']]
    if df_by_hops.empty != True:
        tmplist=[]
        for row in range(0, len(df_by_hops)):
            tmplist.append(df_by_hops.iloc[row]['avg'])
        
        if len(tmplist) != num_times_run:
            count = 0
            for each in tmplist:
                count = count + 1
            for times in range(0, num_times_run-count):
                tmplist.append(None)
            
        
        df_all[str(hops) + " hop(s)"] = tmplist
        
# print(df_all)

# print(tmplist)   

fig1 = df_all.plot.box()

fig1.update_layout(
    font_family="Courier New",
    font_color="blue",
    title="Boxplot of Avg Latency Values for Each Traceroute Run"
)
fig1.update_yaxes(title="latency (s)")
fig1.update_xaxes(title="")

if not os.path.exists("charts"):
    os.mkdir("charts")
    
fig1.write_image("charts/bxplt_avg.pdf", format="pdf")


#Creating boxplot for all latency data points for each hop

raw_data = pd.read_json('trt_data_all.json')

df_all_lats = pd.DataFrame()

hops_list = []

# print(raw_data)


for row in range(0, len(raw_data)):
    
    hops_list.append(raw_data.loc[row]['hop'])
    
hops_list = list(set(hops_list))

# print(hops_list)

for each in hops_list:


    hop_proc = raw_data[ raw_data['hop'] == each  ]

    hop_proc = hop_proc.reset_index()

    tmplist=[]
    latlist=[]

    for row in range(0, len(hop_proc)):

        hop = hop_proc.loc[row]['hop']

        tmplist = hop_proc.loc[row]['lat']
        
        for each in tmplist:
            latlist.append(each)
            
    if len(latlist) < num_times_run * 3:

        filler = 3 * num_times_run - len(latlist)

        for each in range(0, filler):
            latlist.append(None)        
            

    df_all_lats[str(hop) + " hop(s)"] = latlist
    
df_all_lats.head(100)
    
fig2 = df_all_lats.plot.box()

fig2.update_layout(
    font_family="Courier New",
    font_color="Black",
    title="Boxplot of All Latency Values for Each Traceroute Run"
)
fig2.update_yaxes(title="latency (s)")
fig2.update_xaxes(title="")

if not os.path.exists("charts"):
    os.mkdir("charts")
    
fig2.write_image("charts/bxplt_all.pdf", format="pdf")


print('Boxplots generated successfully to the charts folder!')




