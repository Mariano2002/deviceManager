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
import json
text = '''[{"model": "inventari.device", "pk": 39, "fields": {"username": "mariano12", "SN": "2931-6D9E-545C", "NAME": "Device 1", "DEVICE_ID": 2243, "DEVICE_NOTES": "", "VLANS": "[]", "LAN_NETWORK_LIST": "", "LAN_MEDIA": "", "LAN_L2_ISO": "", "LAN_STROUTEn": "", "DHCP_SERVER": "", "DHCP_SERVER_LEASE": "", "DHCP_SERVER_NETMASK": "", "DHCP_SERVER_POOL_START": "", "DHCP_SERVER_POOL_END": "", "DHCP_RESERVATION": "", "DHCP_LOG_ENABLE": "", "DHCP_SERVER_DNS": "", "DHCP_SERVER_WINS": "", "DHCP_OPTION_15": "", "DHCP_RELAY_OPTION_82": "", "DHCP_RELAY_SERVER": ""}}, {"model": "inventari.device", "pk": 40, "fields": {"username": "mariano12", "SN": "2931-6D9E-545C", "NAME": "Device 1", "DEVICE_ID": 2243, "DEVICE_NOTES": "", "VLANS": "[]", "LAN_NETWORK_LIST": "", "LAN_MEDIA": "", "LAN_L2_ISO": "", "LAN_STROUTEn": "", "DHCP_SERVER": "", "DHCP_SERVER_LEASE": "", "DHCP_SERVER_NETMASK": "", "DHCP_SERVER_POOL_START": "", "DHCP_SERVER_POOL_END": "", "DHCP_RESERVATION": "", "DHCP_LOG_ENABLE": "", "DHCP_SERVER_DNS": "", "DHCP_SERVER_WINS": "", "DHCP_OPTION_15": "", "DHCP_RELAY_OPTION_82": "", "DHCP_RELAY_SERVER": ""}}, {"model": "inventari.device", "pk": 41, "fields": {"username": "mariano12", "SN": "2931-6D9E-545C", "NAME": "Device 1", "DEVICE_ID": 2243, "DEVICE_NOTES": "", "VLANS": "[]", "LAN_NETWORK_LIST": "", "LAN_MEDIA": "", "LAN_L2_ISO": "", "LAN_STROUTEn": "", "DHCP_SERVER": "", "DHCP_SERVER_LEASE": "", "DHCP_SERVER_NETMASK": "", "DHCP_SERVER_POOL_START": "", "DHCP_SERVER_POOL_END": "", "DHCP_RESERVATION": "", "DHCP_LOG_ENABLE": "", "DHCP_SERVER_DNS": "", "DHCP_SERVER_WINS": "", "DHCP_OPTION_15": "", "DHCP_RELAY_OPTION_82": "", "DHCP_RELAY_SERVER": ""}}]'''
dict = json.loads(text)

for i in dict:
    inst = i['fields']
    inst['username'] = request.user.username
    devices.objects.create(**inst)