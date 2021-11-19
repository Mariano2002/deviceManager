from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *





class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class deviceForm(forms.ModelForm):
    class Meta:
        model = device
        fields = ('username', 'SN', 'NAME', 'DEVICE_ID', 'DEVICE_NOTES', 'LAN_NETWORK_LIST', 'VLANS', 'LAN_MEDIA', 'LAN_L2_ISO', 'LAN_STROUTEn', 'DHCP_SERVER', 'DHCP_SERVER_LEASE', 'DHCP_SERVER_NETMASK', 'DHCP_SERVER_POOL_START', 'DHCP_SERVER_POOL_END', 'DHCP_RESERVATION', 'DHCP_LOG_ENABLE', 'DHCP_SERVER_DNS', 'DHCP_SERVER_WINS', 'DHCP_OPTION_15', 'DHCP_RELAY_OPTION_82', 'DHCP_RELAY_SERVER')




class VLANForm(forms.ModelForm):
    class Meta:
        model = VLAN
        fields = ('username', 'LANn_VLAN_ID', 'LANn_NAME', 'LANn_NETWORK_LIST', 'LANn_NOTES', 'LANn_L2_ISO', 'DHCPn_SERVER', 'DHCPn_SERVER_LEASE', 'DHCPn_SERVER_NETMASK', 'DHCPn_SERVER_POOL_START', 'DHCPn_SERVER_POOL_END', 'DHCPn_RESERVATION', 'DHCPn_LOG_ENABLE', 'DHCPn_SERVER_DNS', 'DHCPn_SERVER_WINS', 'DHCPn_OPTION_15', 'DHCPn_RELAY_OPTION_82', 'DHCPn_RELAY_SERVER')


class UploadFileForm(forms.Form):
    file = forms.FileField()

