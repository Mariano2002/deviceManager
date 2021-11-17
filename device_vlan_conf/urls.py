from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', login_page, name='login_page'),

    path('login', login_page, name='login_page'),
    path('signup', signup, name='signup'),
    path('logout', logout_page, name="logout_page"),

    url(r'^$', display, name='display'),
    path('home', display, name='display'),
    path('add_device', add_device, name="add_device"),
    path('add_vlan', add_vlan, name="add_vlan"),


    path('edit_device/<path:device_id>', edit_device, name="edit_device"),
    path('delete_device/<path:device_id>', delete_device, name="delete_device"),
    path('duplicate_device/<path:device_id>', duplicate_device, name="duplicate_device"),
    path('clear_devices', clear_devices, name="clear_devices"),


    path('edit_vlan/<path:vlan_id>', edit_vlan, name="edit_vlan"),
    path('delete_vlan/<path:vlan_id>', delete_vlan, name="delete_vlan"),
    path('duplicate_vlan/<path:vlan_id>', duplicate_vlan, name="duplicate_vlan"),
    path('clear_vlans', clear_vlans, name="clear_vlans"),


    path('export_csv', export_csv, name="export_csv"),
    path('export_json', export_json, name="export_json"),




]