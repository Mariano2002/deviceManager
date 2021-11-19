from django.test import TestCase


list1 = [
"LANn_VLAN_ID",
"LANn_NAME",
"LANn_NETWORK_LIST",
"LANn_NOTES",
"LANn_L2_ISO",
"DHCPn_SERVER",
"DHCPn_SERVER_LEASE",
"DHCPn_SERVER_NETMASK",
"DHCPn_SERVER_POOL_START",
"DHCPn_SERVER_POOL_END",
"DHCPn_RESERVATION",
"DHCPn_LOG_ENABLE",
"DHCPn_SERVER_DNS",
"DHCPn_SERVER_WINS",
"DHCPn_OPTION_15",
"DHCPn_RELAY_OPTION_82",
"DHCPn_RELAY_SERVER",
]

list2 = [
"SN",
"NAME",
"DEVICE_ID",
"LAN_NETWORK_LIST",
"VLANS",
"LAN_MEDIA",
"LAN_L2_ISO",
"LAN_STROUTEn",
"DHCP_SERVER",
"DHCP_SERVER_LEASE",
"DHCP_SERVER_NETMASK",
"DHCP_SERVER_POOL_START",
"DHCP_SERVER_POOL_END",
"DHCP_RESERVATION",
"DHCP_LOG_ENABLE",
"DHCP_SERVER_DNS",
"DHCP_SERVER_WINS",
"DHCP_OPTION_15",
"DHCP_RELAY_OPTION_82",
"DHCP_RELAY_SERVER",
]
#
# for i in list1:
#     print(
#         '''
#                     <div class="col-md-4 mb-4">
#                       <div class="form-outline">
#                         {{ form.{}.as_hidden }}
#                         <input type="text" name="{}" id="{}" class="form-control form-control-lg" />
#                         <label class="form-label" for="{}">{}</label>
#                       </div>
#                     </div>
#         '''.format(i,i,i,i,i)
#     )
# import json
# text = '''[{"model": "inventari.device", "pk": 39, "fields": {"username": "mariano12", "SN": "2931-6D9E-545C", "NAME": "Device 1", "DEVICE_ID": 2243, "DEVICE_NOTES": "", "VLANS": "[]", "LAN_NETWORK_LIST": "", "LAN_MEDIA": "", "LAN_L2_ISO": "", "LAN_STROUTEn": "", "DHCP_SERVER": "", "DHCP_SERVER_LEASE": "", "DHCP_SERVER_NETMASK": "", "DHCP_SERVER_POOL_START": "", "DHCP_SERVER_POOL_END": "", "DHCP_RESERVATION": "", "DHCP_LOG_ENABLE": "", "DHCP_SERVER_DNS": "", "DHCP_SERVER_WINS": "", "DHCP_OPTION_15": "", "DHCP_RELAY_OPTION_82": "", "DHCP_RELAY_SERVER": ""}}, {"model": "inventari.device", "pk": 40, "fields": {"username": "mariano12", "SN": "2931-6D9E-545C", "NAME": "Device 1", "DEVICE_ID": 2243, "DEVICE_NOTES": "", "VLANS": "[]", "LAN_NETWORK_LIST": "", "LAN_MEDIA": "", "LAN_L2_ISO": "", "LAN_STROUTEn": "", "DHCP_SERVER": "", "DHCP_SERVER_LEASE": "", "DHCP_SERVER_NETMASK": "", "DHCP_SERVER_POOL_START": "", "DHCP_SERVER_POOL_END": "", "DHCP_RESERVATION": "", "DHCP_LOG_ENABLE": "", "DHCP_SERVER_DNS": "", "DHCP_SERVER_WINS": "", "DHCP_OPTION_15": "", "DHCP_RELAY_OPTION_82": "", "DHCP_RELAY_SERVER": ""}}, {"model": "inventari.device", "pk": 41, "fields": {"username": "mariano12", "SN": "2931-6D9E-545C", "NAME": "Device 1", "DEVICE_ID": 2243, "DEVICE_NOTES": "", "VLANS": "[]", "LAN_NETWORK_LIST": "", "LAN_MEDIA": "", "LAN_L2_ISO": "", "LAN_STROUTEn": "", "DHCP_SERVER": "", "DHCP_SERVER_LEASE": "", "DHCP_SERVER_NETMASK": "", "DHCP_SERVER_POOL_START": "", "DHCP_SERVER_POOL_END": "", "DHCP_RESERVATION": "", "DHCP_LOG_ENABLE": "", "DHCP_SERVER_DNS": "", "DHCP_SERVER_WINS": "", "DHCP_OPTION_15": "", "DHCP_RELAY_OPTION_82": "", "DHCP_RELAY_SERVER": ""}}]'''
# dict = json.loads(text)
#
# for i in dict:
#     inst = i['fields']
#     inst['username'] = request.user.username
#     devices.objects.create(**inst)


import re
# r = re.compile('.{4}-.{4}-.{4}$')
#
# r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$')
#
# r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}:[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
# r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')


#AB:CD:EF:01:23:45#127.0.0.1#optional-name-field

#192.168.0.1 192.168.0.2, default
#192.168.0.1 192.168.0.2


# r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
# r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3},')

# r = re.compile('.*\..*$')
# r = re.compile('[0-9]{1,4}$')
# r = re.compile('[A-Z]{2}:[A-Z]{2}:[A-Z]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}#[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}#')


# r = re.compile('.{4}-.{4}-.{4}$|.{4}.{4}.{4}$')
# if r.match('qwer2342dfwe') is None:
#    print('matches')
import re
import pandas as pd
cereal_df = pd.read_csv(r"C:\Users\Mariano\downloads\export (8).csv")



print(cereal_df)
list_headers = ['SN', 'LAN_NETWORK_LIST', 'LAN_MEDIA', 'LAN_L2_ISO', 'LAN_STROUTEn', 'DHCP_SERVER', 'DHCP_SERVER_LEASE',
           'DHCP_SERVER_NETMASK', 'DHCP_SERVER_POOL_START', 'DHCP_SERVER_POOL_END', 'DHCP_RESERVATION',
           'DHCP_LOG_ENABLE', 'DHCP_SERVER_DNS', 'DHCP_SERVER_WINS', 'DHCP_OPTION_15', 'DHCP_RELAY_OPTION_82',
           'DHCP_RELAY_SERVER']
df1 = cereal_df[list_headers]
print(df1)
username = "mariano"



headers = list(cereal_df.columns.values)
headers_new = headers[17:]
list_headers_b = []
while len(headers_new) != 0:
    headers_now = headers_new[:15]
    print(headers_now)
    headers_new = headers_new[15:]
    list_headers_b.append(headers_now)



list_vlans = []
for index, row in df1.iterrows():
    print(index)
    inst = {'username':username}
    for i in list_headers:
        if str(row[i]) == "nan":
            inst[i] = ""
        else:
            inst[i] = row[i]
    for hd in list_headers_b:
        for index1, row in cereal_df[hd].iterrows():
            vlan_inst = {}
            if index1 == index:
                for i in hd:
                    print(row[i])
                    if str(row[i]) == "nan":
                        vlan_inst[re.sub('\d', 'n', i.split("_")[0]).replace("nn","n")+"_"+"_".join(i.split("_")[1:])] = ""
                    else:
                        vlan_inst[re.sub('\d', 'n', i.split("_")[0]).replace("nn","n")+"_"+"_".join(i.split("_")[1:])] = row[i]
            if vlan_inst not in list_vlans:
                list_vlans.append(vlan_inst)


for i in list_vlans:
    print(i)









# headers = headers + [f'LAN{nr + 1}_NAME', f'LAN{nr + 1}_NETWORK_LIST', f'LAN{nr + 1}_L2_ISO', f'DHCP{nr + 1}_SERVER',
#                      f'DHCP{nr + 1}_SERVER_LEASE', f'DHCP{nr + 1}_SERVER_NETMASK', f'DHCP{nr + 1}_SERVER_POOL_START',
#                      f'DHCP{nr + 1}_SERVER_POOL_END', f'DHCP{nr + 1}_RESERVATION', f'DHCP{nr + 1}_LOG_ENABLE',
#                      f'DHCP{nr + 1}_SERVER_DNS', f'DHCP{nr + 1}_SERVER_WINS', f'DHCP{nr + 1}_OPTION_15',
#                      f'DHCP{nr + 1}_RELAY_OPTION_82', f'DHCP{nr + 1}_RELAY_SERVER']




