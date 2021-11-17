from django.db import models


class device(models.Model):
    LAN_L2_ISO_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    DHCP_SERVER_choices = (
        ('Enable', 'Enable'),
        ('Disable', 'Disable'),
        ('Relay', 'Relay'),
    )
    DHCP_LOG_ENABLE_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    DHCP_RELAY_OPTION_82_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    username = models.CharField(max_length=300, blank=False,)
    SN = models.CharField(max_length=14, blank=False,  help_text='1234-5678-90AB')
    NAME = models.CharField(max_length=100, blank=False,  help_text="Device 1")
    DEVICE_ID = models.IntegerField(blank=False,  help_text="150")
    DEVICE_NOTES = models.CharField(max_length=999, blank=True, help_text="This is a device")
    VLANS = models.CharField(max_length=9999, blank=True)
    LAN_NETWORK_LIST = models.CharField(max_length=25, blank=True,  help_text='192.168.0.1/24')
    LAN_MEDIA = models.CharField(max_length=20, blank=True,)
    LAN_L2_ISO = models.CharField(max_length=3, choices=LAN_L2_ISO_choices, blank=True, help_text='yes, no')
    LAN_STROUTEn = models.CharField(max_length=60, blank=True, help_text='172.16.0.0/12:192.168.0.1')
    DHCP_SERVER = models.CharField(max_length=7, choices=DHCP_SERVER_choices, blank=True, help_text='enable, disable, relay')
    DHCP_SERVER_LEASE = models.CharField(max_length=20, blank=True, help_text='86400')
    DHCP_SERVER_NETMASK = models.CharField(max_length=20, blank=True, help_text='255.255.255.0')
    DHCP_SERVER_POOL_START = models.CharField(max_length=20, blank=True, help_text='192.168.0.1')
    DHCP_SERVER_POOL_END = models.CharField(max_length=20, blank=True, help_text='192.168.0.255')
    DHCP_RESERVATION = models.CharField(max_length=60, blank=True, help_text='AB:CD:EF:01:23:45#127.0.0.1#optional-name-field')
    DHCP_LOG_ENABLE = models.CharField(max_length=3, choices=DHCP_LOG_ENABLE_choices,  blank=True, help_text='yes, no')
    DHCP_SERVER_DNS = models.CharField(max_length=60, blank=True, help_text='192.168.0.1 192.168.0.2')
    DHCP_SERVER_WINS = models.CharField(max_length=60, blank=True, help_text='192.168.0.1 192.168.0.2, default')
    DHCP_OPTION_15 = models.CharField(max_length=20, blank=True, help_text='example.com')
    DHCP_RELAY_OPTION_82 = models.CharField(max_length=3, choices=DHCP_RELAY_OPTION_82_choices,  blank=True, help_text='yes, no')
    DHCP_RELAY_SERVER = models.CharField(max_length=60, blank=True, help_text='192.168.0.1 192.168.0.2')

    def __str__(self):
        return "That's a model!"




class VLAN(models.Model):
    LANn_L2_ISO_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    DHCPn_SERVER_choices = (
        ('Enable', 'Enable'),
        ('Disable', 'Disable'),
        ('Relay', 'Relay'),
    )

    DHCPn_LOG_ENABLE_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    DHCPn_RELAY_OPTION_82_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    username = models.CharField(max_length=300, blank=False,)
    LANn_VLAN_ID = models.IntegerField(blank=False, help_text='1-4094')
    LANn_NAME = models.CharField(max_length=100, blank=False, help_text='"VLAN 1", "Marketing Network", etc')
    LANn_NETWORK_LIST = models.CharField(max_length=25, blank=True, help_text='192.168.0.1/24')
    LANn_NOTES = models.CharField(max_length=999, blank=True, help_text="Notes for the VLAN")
    LANn_L2_ISO = models.CharField(max_length=3, choices=LANn_L2_ISO_choices, blank=True, help_text='yes, no')
    DHCPn_SERVER = models.CharField(max_length=7, choices=DHCPn_SERVER_choices, blank=True, help_text='enable, disable, relay')
    DHCPn_SERVER_LEASE = models.CharField(max_length=20, blank=True, help_text='86400')
    DHCPn_SERVER_NETMASK = models.CharField(max_length=20, blank=True, help_text='255.255.255.0')
    DHCPn_SERVER_POOL_START = models.CharField(max_length=20, blank=True, help_text='192.168.0.1')
    DHCPn_SERVER_POOL_END = models.CharField(max_length=20, blank=True, help_text='192.168.0.255')
    DHCPn_RESERVATION = models.CharField(max_length=60, blank=True, help_text='AB:CD:EF:01:23:45#127.0.0.1#optional-name-field')
    DHCPn_LOG_ENABLE = models.CharField(max_length=3, choices=DHCPn_LOG_ENABLE_choices, blank=True, help_text='yes, no')
    DHCPn_SERVER_DNS = models.CharField(max_length=60, blank=True, help_text='192.168.0.1 192.168.0.2')
    DHCPn_SERVER_WINS = models.CharField(max_length=60, blank=True, help_text='192.168.0.1 192.168.0.2, default')
    DHCPn_OPTION_15 = models.CharField(max_length=20, blank=True, help_text='example.com')
    DHCPn_RELAY_OPTION_82 = models.CharField(max_length=3, choices=DHCPn_RELAY_OPTION_82_choices, blank=True, help_text='yes, no')
    DHCPn_RELAY_SERVER = models.CharField(max_length=60, blank=True, help_text='192.168.0.1 192.168.0.2')


    def __str__(self):
        return "That's a model!"
