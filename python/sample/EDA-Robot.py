#sudo python3 -m pip install bs4
#sudo python3 -m pip install requests
#sudo python3 -m pip install dns-batch-resolver

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import subprocess
import requests
import re
import os
import sys
import time
from time import sleep
import dns.resolver
from urllib3.util import connection
from pathlib import Path

ext_deb = '.deb'
dell_vpn_nameservers = ['10.14.1.1', '10.11.0.1']
system_create_connection = connection.create_connection

########################################################
### Function for parsing platform-sku.xml file       ###
########################################################
def parseXMLFile(filename):
    xml_sku_item_num = []
    xml_sku_info = ['platform']
    xml_platform_sku = []
    xml_sku_name = []
    xml_sku_ip_addr = []
    len_xml_sku_name = 0
    len_xml_sku_ip_addr = 0    
    count_xml_sku_item = 0

    print ("Parsing platform sku information...\n")

    tree = ET.parse(filename)  
    root = tree.getroot()

    platform_num = len(root[0])
    ###print ("Number of platforms: " + str(platform_num))

    # for each platform
    for item in range(platform_num):
        xml_sku_info.clear()
        count_xml_sku_item = 0
        item_num = len(root[0][item])

        ###print("Number of items: " + str(item_num))

        # for each item in each platform, search for "platform-name"
        for item1 in range(item_num):
            tag_pf_name = re.search ("platform-name", root[0][item][item1].tag)
            if tag_pf_name is not None:
                ###print (tag_pf_name)
                xml_sku_info.append(root[0][item][item1].text)
                count_xml_sku_item = count_xml_sku_item + 1                
                break

        # for each item in each platform, search for "url-prefix"
        for item2 in range(item_num):
            tag_url_prefix = re.search ("url-prefix", root[0][item][item2].tag)
            if tag_url_prefix is not None:
                ###print (tag_url_prefix)
                xml_sku_info.append(root[0][item][item2].text)
                count_xml_sku_item = count_xml_sku_item + 1
                break

        # for each item in each platform, search for "url-postfix"
        for item3 in range(item_num):
            tag_url_postfix = re.search ("url-postfix", root[0][item][item3].tag)
            if tag_url_postfix is not None:
                ###print (tag_url_postfix)
                xml_sku_info.append(root[0][item][item3].text)
                count_xml_sku_item = count_xml_sku_item + 1
                break

        if tag_pf_name is not None:
            if tag_url_prefix is not None:
                if tag_url_postfix is not None:
                    # "platform-name"
                    xml_platform_sku.append(xml_sku_info[0])
                    # "url-prefix"
                    xml_platform_sku.append(xml_sku_info[1])
                    # "url-postfix"
                    xml_platform_sku.append(xml_sku_info[2])  
                    ###print ("append: ", xml_platform_sku[0])
                    ###print ("append: ", xml_platform_sku[1])
                    ###print ("append: ", xml_platform_sku[2])
                    xml_sku_info.clear()
                    # for each <sku>
                    for item4 in range(item_num):
                        tag_sku = re.search ("sku", root[0][item][item4].tag)
                        if tag_sku is None:
                            tag_pf_name1 = re.search ("platform-name", root[0][item][item4].tag)
                            if tag_pf_name1 is not None:
                                continue
                            tag_url_prefix1 = re.search ("url-prefix", root[0][item][item4].tag)
                            if tag_url_prefix1 is not None:
                                continue
                            tag_url_postfix1 = re.search ("url-postfix", root[0][item][item4].tag)
                            if tag_url_postfix1 is not None:
                                continue
                            break
                        else:         
                            ###print ("sku_tag=", tag_sku)
                            sku_item_num  = len(root[0][item][item4])
                            #print ("sku_item_num: ", sku_item_num)
                            xml_sku_name.clear()
                            xml_sku_ip_addr.clear()
                            len_xml_sku_name = 0
                            len_xml_sku_ip_addr = 0
                            if sku_item_num != 2:
                                print ("Error: <sku-name> and <sku-ip-addr> not match in XML file!")
                                break                              
                            for item5 in range(sku_item_num):
                                tag_sku_name = re.search ("sku-name", root[0][item][item4][item5].tag)
                                if tag_sku_name is not None:
                                    count_xml_sku_item = count_xml_sku_item + 1
                                    #print SKU name
                                    print (root[0][item][item4][item5].text) 
                                    xml_sku_name.append(root[0][item][item4][item5].text)
                                    continue
                                else: 
                                    tag_sku_ip_addr = re.search ("sku-ip-addr", root[0][item][item4][item5].tag)
                                    if tag_sku_ip_addr is not None:
                                        count_xml_sku_item = count_xml_sku_item + 1
                                        # print IP Address
                                        print (root[0][item][item4][item5].text)
                                        xml_sku_ip_addr.append(root[0][item][item4][item5].text)
                                        print ("\n")
                                        continue 
                                    else:
                                         # Error, "sku-name" or "sku- ip-addr" not found
                                         xml_sku_name.clear()
                                         xml_sku_ip_addr.clear()
                                         break 

                            len_xml_sku_name = len(xml_sku_name)
                            if len_xml_sku_name == 0:
                                print ("Error: <sku-name> not found in xml file!")
                                break

                            len_xml_sku_ip_addr =  len(xml_sku_ip_addr)
                            if len_xml_sku_ip_addr == 0:
                                print ("Error: <sku-ip-addr> not found in XML file!")
                                break
                            
                            if len_xml_sku_name != len_xml_sku_ip_addr:
                                print ("Error: <sku-name> and <sku-ip-addr> not match in XML file!")
                                break
       
                            xml_platform_sku.append(xml_sku_name[0])
                            xml_platform_sku.append(xml_sku_ip_addr[0])
                            #print ("append: ", xml_sku_name[0])
                            #print ("append: ", xml_sku_ip_addr[0])

        xml_sku_item_num.append(str(count_xml_sku_item))
                        
        if (tag_pf_name is None) or (tag_url_prefix is None) or (tag_url_postfix is None) or (tag_sku is None) or (len_xml_sku_name == 0) or (len_xml_sku_ip_addr == 0):
            if (tag_pf_name is None):
                printf ("Error: <platform-name> not found in xml file!")
            if (tag_url_prefix is None):
               printf ("Error: <url-prefix> not found in xml file!")
            if (tag_url_postfix is None):
               printf ("Error: <url-postfix> not found in xml file!")

            xml_sku_item_num.clear()
            xml_platform_sku.clear()
            print ("Error in XML file")
            break

    return xml_sku_item_num, xml_platform_sku


########################################################
### Function for getting web page directory listings ###
########################################################
def WebDirList(url, prefix_str, postfix_str):
    print (url)
    try:
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        if len(prefix_str) == 0:
            return [node.get('href') for node in soup.find_all('a') if node.get('href').endswith(postfix_str)]
        else:
            return [node.get('href') for node in soup.find_all('a') if node.get('href').startswith(prefix_str) and node.get('href').endswith(postfix_str)]
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:",errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print ("Request Error:",err)
        sys.exit(1)


########################################################
### Function for downloading a file from url         ###
########################################################
def download_file(url, fName):
    with open(fName, 'wb') as f:
        response = requests.get(url, stream=True)
        fSize_str = response.headers.get('content-length')
        if fSize_str is None:
            f.write(response.content)
        else:
            done = 0
            dsize = 0
            progress_percent = 0.0
            progress_str = '{}{}'.format('#' * done, '.' * (50-done))
            sys.stdout.write("\r[%s] %.1f%%" % (progress_str, progress_percent))
            sys.stdout.flush()
            time.sleep(0.01)
            fSize = int(fSize_str)
            for data in response.iter_content(chunk_size=max(int(fSize/1000), 1024*1024)):
                dsize += len(data)
                f.write(data)
                done = int(50*dsize/fSize)
                progress_str = '{}{}'.format('#' * done, '.' * (50-done))
                progress_percent = (dsize/fSize)*100
                sys.stdout.write("\r[%s] %.1f%%" % (progress_str, progress_percent))
                sys.stdout.flush()
                time.sleep(0.01)
    sys.stdout.write('\n')


########################################################
### Function for downloading deb file                ###
########################################################
def download_latest_build(cur_working_dir, url, max_build_num, deb_fname_prefix):
    filelen = 0
    url_deb = (url + str(max_build_num) + '/')
    file=''
    for file in WebDirList(url_deb, deb_fname_prefix, ext_deb):
        if len(file) != 0:
            print ("Found deb file:", file)
            # filenames contains with or without sku names
            # download only the shortest filename found.  
            if filelen == 0:
                filelen = len(file)
                target_filename = file
            else:
                if len(file) < filelen:
                    filelen = len(file)
                    target_filename = file
        else:
            print ("Error, file not found: ", file)
            sys.exit(1)

    url_deb_download = (url_deb + target_filename)
    print ("Downloading file from : " + url_deb_download)
    dir_file = (cur_working_dir + target_filename)
    # if file already, don't download
    if os.path.isfile(dir_file):
        return dir_file
    else:  
        download_file(url_deb_download, dir_file)

    #print ("dir_file=", dir_file)
    return dir_file

########################################################
### Function for checking latest EDA build number    ###
########################################################
def check_latest_build(url, fName):
    last_build_num = 0
    max_build_num = 0
    build_num = 0

    if os.path.exists(fName):
        with open(fName, 'r') as f:
            file_content = f.read()
            for textstring in re.findall('\d+', file_content):
                last_build_num = int(textstring)
                print ("Last build number : " + str(last_build_num))
        f.close()
    for url_link in WebDirList(url, '', '/'):
        for value in re.findall('\d+', url_link):
            build_num = int(value)
            if build_num > max_build_num:
                max_build_num = build_num
    print ("Maximum build number = " + str(max_build_num))
    if max_build_num > last_build_num:
        with open(fName, 'w') as f:
            f.write(str(max_build_num))
            f.close()
        return max_build_num
    else:
        return 0


########################################################
### Function for getting current working directory   ###
########################################################
def get_working_directory():
	dir_path = os.path.realpath(sys.argv[0])
	if os.path.isdir(dir_path):
		return dir_path
	else:
		return os.path.dirname(dir_path)


#############################################################
### Function for using custom dns resolver                ###
### Note:                                                 ###
###     Due to VPN connection, system dns resolver always ###
###     use system dns servers instead of the dns server  ###
###     for VPN. Hence, need to replace with custom dns   ###
###     resolver                                          ###
#############################################################
def custom_create_connection(address, *args, **kwargs):
	host, port = address
	print ("host=", host)
	print ("port=", port)

	hostname = CustomDNSResolver(host)
	return system_create_connection((hostname,port), *args, **kwargs)


########################################################
### custom dns resolver function 	     	     ###
########################################################
def CustomDNSResolver(host):
    custom_resolver = dns.resolver.Resolver()
    custom_resolver.nameservers = dell_vpn_nameservers
    result = custom_resolver.query(host)
    for data in result:
        print ("IPAddr = ", str(data))
        return str(data)


########################################################
### Main program                                     ###
########################################################
def main():
    diagOS_working_dir = (get_working_directory() + '/')
    ###print (diagOS_working_dir)
    platform_sku_xml_file = (diagOS_working_dir + 'platform-sku.xml')
    pf_sku_items, pf_sku_info = parseXMLFile(platform_sku_xml_file)
    pf_platform_count = len(pf_sku_items)
    pf_sku_data_count = len(pf_sku_info)
    ###print ("Number of platforms: " + str(pf_platform_count) + " : ")
    ###print (pf_sku_items)
    ###print ("Total number of items: " + str(pf_sku_data_count) + " : ")
    ###print (pf_sku_info)

    # replace the system create_connection with custom_create_connection
    connection.create_connection = custom_create_connection

    if (pf_platform_count == 0) or (pf_sku_data_count == 0):
        return
    else:
        # for each platform
        for item in range(pf_platform_count):
            data_count = pf_sku_items[item]
            #number of items in current platform
            ###print (data_count)
            sku_item_count = int(data_count) - 3
            sku_count = int(sku_item_count / 2)
            #number of sku
            ###print (sku_count)
            offset = 0
            if item != 0:
                for x in range(item):
                    offset += int(pf_sku_items[x])

            # diagOS_url = ('http://artifactory.force10networks.com/list/diag/' + diagOS_platform + '-DiagOS/DellEmc/diagos-diag/')
            # e.g. diagOS_url = http://artifactory.force10networks.com/list/diag/S5200-DiagOS/DellEmc/diagos-diag/
            diagOS_url_prefix = pf_sku_info[offset + 1]
            if not diagOS_url_prefix.endswith('/'):
                diagOS_url_prefix = (pf_sku_info[offset + 1] + '/')

            diagOS_platform = pf_sku_info[offset + 0]

            diagOS_url_postfix = pf_sku_info[offset + 2]
            if not diagOS_url_postfix.endswith('/'):
                diagOS_url_postfix = (pf_sku_info[offset + 2] + '/')

            diagOS_url = diagOS_url_prefix + diagOS_platform + diagOS_url_postfix
            ###print (diagOS_url)
            # for each SKU
            for y in range(sku_count):
                # diagOS_buildnum_fName = (diagOS_working_dir + diagOS_sku + '-DiagLastBuild.txt')
                # e.g. S5212F-DiagLastBuild.txt
                diagOS_sku = pf_sku_info[offset + 3 + y*2]
                print ("Checking for  " + diagOS_sku + "...")
                # create a SKU name directory if not yet exists
                if not os.path.exists(diagOS_sku):
                    os.makedirs(diagOS_sku)
                diagOS_buildnum_fName = (diagOS_working_dir + diagOS_sku + "/" + diagOS_platform + '-DiagLastBuild.txt')
                ###print (diagOS_buildnum_fName)
                deb_fname_prefix = ('dn-diags-' + diagOS_platform + "-DiagOS-")
                ###print (deb_fname_prefix)
                max_build_num = 0
                max_build_num = check_latest_build(diagOS_url, diagOS_buildnum_fName)
                # Only download image and run sku robot scrip if new build update is found
                if max_build_num > 0:
                    DiagOS_Dir_File = download_latest_build(diagOS_working_dir, diagOS_url, max_build_num, deb_fname_prefix)
                    ###print ("Getting path & name:", DiagOS_Dir_File)
                    Image_File = Path(DiagOS_Dir_File).name
                    Image_Dir_Path = Path(DiagOS_Dir_File).parent
                    ###print (Image_Dir_Path)
                    ###print (Image_File)
                    sku_ip = pf_sku_info[offset + 3 + y*2 + 1]
                    ###print (sku_ip)
                    cmd_opt1 = ("HOST:" + sku_ip)
                    cmd_opt2 = ("USERNAME:" + "root")
                    cmd_opt3 = ("PASSWORD:" + "calvin")
                    cmd_opt4 = ("FILE:" + Image_File)
                    cmd_opt5 = ("-d")
                    cmd_opt6 = (str(Image_Dir_Path) + "/" + diagOS_sku)
                    cmd_opt7 = ("-T")
                    cmd_opt8 = (str(Image_Dir_Path) + "/" + diagOS_sku + "/" + diagOS_sku + "-robot.robot")
                    ###print (cmd_opt6)
                    cmd = ['/usr/local/bin/robot', '-v', cmd_opt1, '-v', cmd_opt2, '-v', cmd_opt3, '-v', cmd_opt4, cmd_opt5, cmd_opt6, cmd_opt7, cmd_opt8]
                    print ("\n")
                    print (cmd)
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    o, e = proc.communicate()
                    print('Output: ' + o.decode('ascii'))
                    print('Error: '  + e.decode('ascii'))
                    print('code: ' + str(proc.returncode))
                else:
                    print ("No build updates found.")

                print ("\n")

    # restore back the system create_connection
    connection.create_connection = system_create_connection

    return

if __name__ == '__main__':
    main()

