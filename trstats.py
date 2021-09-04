

#General Imports

import os
import statistics
import json
import argparse
import time
import shutil

parser = argparse.ArgumentParser(description='Run traceroute multiple times towards a given target host')

parser.add_argument('-n', action='store', dest='NUM_RUNS', type=int, required=False, default=1, help='Number of times traceroute will run')
parser.add_argument('-d', action='store', dest='RUN_DELAY', type=int, required=False, default=0, help='Number of seconds to wait between two consecutive runs')
parser.add_argument('-m', action='store', dest='MAX_HOPS', type=int, required=False, default=30, help='Max hops that will be checked before traceroute terminates')
parser.add_argument('-o', action='store', dest='OUTPUT', type=str, required=False, default='json', help='Path and name of output JSON files containing the stats. Enter as XXX.json')
parser.add_argument('-g', action='store', dest='GRAPH', type=str, required=False, default='charts', help='Path and name of output PDF files containing stats graph. Enter as XXX.pdf')
parser.add_argument('-t', action='store', dest='TARGET', type=str, required=False, default='google.com', help='A target domain name or IP address (required if --test is absent)')
parser.add_argument('--test', action='store', dest='TEST_DIR', type=str, required=False, default='nun', help=("""Directory containing num_runs text files, each of which contains the output of a traceroute run.
If present, this will override all other options and traceroute will not be invoked. 
Stats will be computed over the traceroute output stored in the text files.
"""))

args = parser.parse_args()

def trtstats(NUM_RUNS, RUN_DELAY, MAX_HOPS, OUTPUT, GRAPH, TARGET, TEST_DIR ):


    #Creating traceroute text file

    json_list = []
    json_list_all = []

    num_times_run = NUM_RUNS

    if os.path.exists('charts'):
        shutil.rmtree('charts')
    if os.path.exists('json'):
        shutil.rmtree('json')
    if os.path.exists("trt_output"):
        shutil.rmtree('trt_output')    

    if TEST_DIR == 'nun':


        print('')
        print ("Running traceroute " + str(num_times_run) + " times...")

        txt_file_dir = r'trt_output'

        for x in range(0, num_times_run):

            #Adding in delay in between runs in seconds

            time.sleep(RUN_DELAY)

            
            print('')
            print('Run ' + str(x + 1) + '...')

            if not os.path.exists("trt_output"):
                os.mkdir("trt_output")

            website = TARGET
            cmd = 'traceroute -m ' + str(MAX_HOPS) + ' ' + website + ' > trt_output/trt' + str(x + 1) + '.txt'
            os.system(cmd)

            print('Run ' + str(x + 1) + ' finished!')

    else: 

        print('')
        print ("Reading traceroute txt data from " + TEST_DIR + " directory...")
        
        txt_file_dir =  TEST_DIR

    for filename in os.listdir(txt_file_dir):

        with open(os.path.join(txt_file_dir, filename), 'r') as file:
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


        # #Removing extra entries json_list

        # for row in range(0, len(json_list) + 1):
        #     try:
        #         if json_list[row].get('hop') == json_list[row + 1].get('hop'):
        #             json_list.remove(json_list[row])
        #     except:
        #         pass

        # for row in range(0, len(json_list) + 1):
        #     try:
        #         if json_list[row].get('hop') == json_list[row + 1].get('hop'):
        #             json_list.remove(json_list[row])
        #     except:
        #         pass

        
        # #Removing extra entries json_list_all

        # for row in range(0, len(json_list_all) + 1):
        #     try:
        #         if json_list_all[row].get('hop') == json_list_all[row + 1].get('hop'):
        #             json_list_all.remove(json_list_all[row])
        #     except:
        #         pass

        # for row in range(0, len(json_list_all) + 1):
        #     try:
        #         if json_list_all[row].get('hop') == json_list_all[row + 1].get('hop'):
        #             json_list_all.remove(json_list_all[row])
        #     except:
        #         pass


    print('')
    print('Exporting json data...')

    #Allowing user to specify where json files should be output

    if OUTPUT == 'json':

        if not os.path.exists("json"):
            os.mkdir("json")

        dest1 = OUTPUT + '/trt_data_avg.json'
        dest2 = OUTPUT + '/trt_data_all.json'
    else:
        dest2 = OUTPUT
        stripped = OUTPUT.rstrip('.json')
        dest1 = stripped + '_avg.json'
    
    #Exporting data in json_list file

    with open(dest1, 'w') as f:
        json.dump(json_list, f)

    #Exporting data in json_list_all file

    with open(dest2, 'w') as f:
        json.dump(json_list_all, f)

    print('Export successful!')

    #Imports for plotting data as boxplot

    import pandas as pd
    import plotly
    pd.options.plotting.backend = "plotly"

    print('')
    print('Generating boxplots...')

    #Creating boxplot for the average values for each number of hops each time traceroute was run

    raw_data = pd.read_json(dest1)

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

    fig1 = df_all.plot.box()

    fig1.update_layout(
        font_family="Courier New",
        font_color="blue",
        title="Boxplot of Avg Latency Values for Each Traceroute Run"
    )
    fig1.update_yaxes(title="latency (s)")
    fig1.update_xaxes(title="")


    #Creating boxplot for all latency data points for each hop

    raw_data = pd.read_json(dest2)

    df_all_lats = pd.DataFrame()

    hops_list = []


    for row in range(0, len(raw_data)):
        
        hops_list.append(raw_data.loc[row]['hop'])
        
    hops_list = list(set(hops_list))

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

    #Allowing user to specify where json files should be output

    if GRAPH == 'charts':

        if not os.path.exists("charts"):
            os.mkdir("charts")

        dest_1 = GRAPH + '/bxplt_avg.pdf'
        dest_2 = GRAPH + '/bxplt_all.pdf'
    else:
        dest_2 = GRAPH
        stripped = GRAPH.rstrip('.pdf')
        dest_1 = stripped + '_avg.pdf'
        
    fig1.write_image(dest_1, format="pdf")
    fig2.write_image(dest_2, format="pdf")


    print('Boxplots generated successfully!')
    print('')


if __name__ == '__main__':
    trtstats(args.NUM_RUNS, args.RUN_DELAY, args.MAX_HOPS, args.OUTPUT, args.GRAPH, args.TARGET, args.TEST_DIR)

