from .forms import *
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import csv
from django.http import HttpResponse
from django.core import serializers
from django.urls import reverse
import re
import pandas as pd

from io import StringIO
def import_json(file, username):
    dict = json.loads(file.split("\n")[0])

    for i in dict:
        inst = i['fields']
        inst['username'] = username
        # print(inst)
        try:
            if validate_davice(inst) == False:
                # print(111)
                return False
            device.objects.create(**inst)
        except:
            # print(222)
            return False

    dict = json.loads(file.split("\n")[1])

    for i in dict:
        inst = i['fields']
        inst['username'] = username
        if validate_vlan(inst) == False or inst['LANn_NAME'] =='':
            # print(3333)
            return False
        VLAN.objects.create(**inst)
    return True

def import_csv(df_in, username):
    list_headers = ['SN', 'LAN_NETWORK_LIST', 'LAN_MEDIA', 'LAN_L2_ISO', 'LAN_STROUTEn', 'DHCP_SERVER', 'DHCP_SERVER_LEASE',
               'DHCP_SERVER_NETMASK', 'DHCP_SERVER_POOL_START', 'DHCP_SERVER_POOL_END', 'DHCP_RESERVATION',
               'DHCP_LOG_ENABLE', 'DHCP_SERVER_DNS', 'DHCP_SERVER_WINS', 'DHCP_OPTION_15', 'DHCP_RELAY_OPTION_82',
               'DHCP_RELAY_SERVER']
    df1 = df_in[list_headers]

    headers = list(df_in.columns.values)
    headers_new = headers[17:]
    list_headers_b = []
    while len(headers_new) != 0:
        headers_now = headers_new[:15]
        # print(headers_now)
        headers_new = headers_new[15:]
        list_headers_b.append(headers_now)

    list_vlans = []
    for index, row in df1.iterrows():
        id_ja = 1
        list_is = device.objects.values_list('DEVICE_ID', flat=True)
        inst = {'username':username}
        for i in list_headers:
            if str(row[i]) == "nan":
                inst[i] = ""
            else:
                inst[i] = row[i]

        while id_ja in list_is:
            id_ja += 1

        inst['DEVICE_ID'] = id_ja
        # print(inst)
        vlan_ids = []
        for hd in list_headers_b:
            for index1, row in df_in[hd].iterrows():
                vlan_inst = {}
                if index1 == index:
                    for i in hd:
                        # print(row[i])
                        if str(row[i]) == "nan":
                            vlan_inst[re.sub('\d', 'n', i.split("_")[0]).replace("nn","n")+"_"+"_".join(i.split("_")[1:])] = ""
                        else:
                            vlan_inst[re.sub('\d', 'n', i.split("_")[0]).replace("nn","n")+"_"+"_".join(i.split("_")[1:])] = row[i]
                # print(len(vlan_inst))
                if len(vlan_inst) != 15:
                    continue
                idv_ja = 1
                listv_is = VLAN.objects.values_list('LANn_VLAN_ID', flat=True)
                while idv_ja in listv_is:
                    idv_ja += 1
                vlan_inst['username'] = username
                vlan_inst['LANn_VLAN_ID'] = idv_ja
                # print(vlan_inst)
                if validate_vlan(vlan_inst) != False and vlan_inst['LANn_NAME'] !='':
                    vlan_ids.append(idv_ja)
                    VLAN.objects.create(**vlan_inst)

        inst['VLANS'] = json.dumps(vlan_ids)
        device.objects.create(**inst)

@login_required(login_url="/login")
def display(request):

    if request.method == 'POST':
        try:
            file = request.FILES['file'].read().decode('utf-8')
            TESTDATA = StringIO(file)
            df_in = pd.read_csv(TESTDATA, sep=',')
            if request.FILES['file'].name[-5:] == '.json':
                if import_json(file, request.user.username) == False:
                    messages.error(request, 'Device ID or VLAN ID already exists!')

            elif request.FILES['file'].name[-4:] == '.csv':
                import_csv(df_in, request.user.username)
            else:
                messages.error(request, 'Please upload a CSV or JSON file!')
        except:
            messages.error(request, 'Please upload a CSV or JSON file!')

        return redirect(display)

    else:
        form = UploadFileForm()

        items = device.objects.all().filter(username=request.user.username)
        for item in items:
            VLANS_names = []
            try:
                vlans = VLAN.objects.all().filter(LANn_VLAN_ID__in=json.loads(item.VLANS), username=request.user.username)
                for i in vlans:
                    VLANS_names.append(i.LANn_NAME+"-"+str(i.LANn_VLAN_ID) )
            except:
                pass
            item.VLANS_names = ", ".join(VLANS_names)
        # print(items)
        vlans = VLAN.objects.all().filter(username=request.user.username)
        return render(request, 'display.html', {'devices':items, 'vlans':vlans, 'form':form})

def user_is_not_logged_in(user):
    return not user.is_authenticated

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect(display)
        else:
            messages.error(request, 'Username or password in incorrect')
            return render(request, 'login.html', {})
    else:
        # print(request.user)
        if request.user.is_anonymous:
            return render(request, 'login.html',)
        return redirect(display)

@user_passes_test(user_is_not_logged_in, login_url=display)
def signup(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login_page)
    context = {"form":form}
    return render(request, 'registration.html', context)

@login_required(login_url=login_page)
def logout_page(request):
    logout(request)
    return redirect(login_page)



def validate_davice(device):
    r = re.compile('.{4}-.{4}-.{4}$|.{4}.{4}.{4}$')
    if r.match(device['SN']) is None and device['SN'] != "":
        # print(1)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$')
    if r.match(device['LAN_NETWORK_LIST']) is None and device['LAN_NETWORK_LIST'] != "":
        # print(2)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}:[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(device['LAN_STROUTEn']) is None and device['LAN_STROUTEn'] != "":
        # print(3)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(device['DHCP_SERVER_POOL_START']) is None and device['DHCP_SERVER_POOL_START'] != "":
        # print(4)
        return False
    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(device['DHCP_SERVER_NETMASK']) is None and device['DHCP_SERVER_NETMASK'] != "":
        # print(5)
        return False
    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(device['DHCP_SERVER_POOL_END']) is None and device['DHCP_SERVER_POOL_END'] != "":
        # print(6)
        return False


    r = re.compile('[A-Z]{2}:[A-Z]{2}:[A-Z]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}#[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}#')
    if r.match(device['DHCP_RESERVATION']) is None and device['DHCP_RESERVATION'] != "":
        # print(7)
        return False


    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(device['DHCP_SERVER_DNS']) is None and device['DHCP_SERVER_DNS'] != "":
        # print(8)
        return False
    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(device['DHCP_RELAY_SERVER']) is None and device['DHCP_RELAY_SERVER'] != "":
        # print(9)
        return False


    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3},')
    if r.match(device['DHCP_SERVER_WINS']) is None and device['DHCP_SERVER_WINS'] != "":
        # print(10)
        return False



def validate_vlan(vlan):
    try:
        if int(vlan['LANn_VLAN_ID']) > 4094:
            # print(1111)
            return False
    except:
        pass

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$')
    if r.match(vlan['LANn_NETWORK_LIST'].replace('{ID}','0')) is None and vlan['LANn_NETWORK_LIST'] != "":
        # print(2222)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(vlan['DHCPn_SERVER_NETMASK'].replace('{ID}','0')) is None and vlan['DHCPn_SERVER_NETMASK'] != "":
        # print(3)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(vlan['DHCPn_SERVER_POOL_START'].replace('{ID}','0')) is None and vlan['DHCPn_SERVER_POOL_START'] != "":
        # print(4)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(vlan['DHCPn_SERVER_POOL_END'].replace('{ID}','0')) is None and vlan['DHCPn_SERVER_POOL_END'] != "":
        # print(5)
        return False

    r = re.compile('[A-Z]{2}:[A-Z]{2}:[A-Z]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}#[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}#')
    if r.match(vlan['DHCPn_RESERVATION'].replace('{ID}','0')) is None and vlan['DHCPn_RESERVATION'] != "":
        # print(6)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(vlan['DHCPn_SERVER_DNS'].replace('{ID}','0')) is None and vlan['DHCPn_SERVER_DNS'] != "":
        # print(7)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3},')
    if r.match(vlan['DHCPn_SERVER_WINS'].replace('{ID}','0')) is None and vlan['DHCPn_SERVER_WINS'] != "":
        # print(8)
        return False

    r = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if r.match(vlan['DHCPn_RELAY_SERVER'].replace('{ID}','0')) is None and vlan['DHCPn_RELAY_SERVER'] != "":
        # print(9)
        return False






@login_required(login_url="/login")
def add_device(request):
    if(request.method) == "POST":
        ids = request.POST.getlist("VLANS")
        ids.remove("")

        updated_data = request.POST.copy()
        updated_data.update({'VLANS': json.dumps(ids)})
        updated_data.update({'username': request.user.username})
        if validate_davice(updated_data) == False:
            messages.error(request, 'One of the field\'s format is wrong!')
            return redirect(add_device)
        form = deviceForm(data=updated_data)

        if form.is_valid():
            # print(form.errors)
            form.save()
            return redirect(display)
        else:
            messages.error(request, 'One of the field\'s format is wrong or you are using a duplicated ID!')
            return redirect(add_device)

    else:
        vlans = VLAN.objects.all().filter(username=request.user.username)
        vlans_dict = {}
        for nr,vlan in enumerate(vlans):
            vlans_dict[nr] = {"id":vlan.id, "name":vlan.LANn_NAME}
        form = deviceForm
        return render(request, 'add_device.html', {'form':form, 'vlans':vlans_dict})

@login_required(login_url="/login")
def add_vlan(request):
    if(request.method) == "POST":
        updated_data = request.POST.copy()
        updated_data.update({'username': request.user.username})
        if validate_vlan(updated_data) == False:
            messages.error(request, 'One of the field\'s format is wrong!')
            return redirect(add_vlan)
        form = VLANForm(data=updated_data)
        if form.is_valid():
            form.save()
            return redirect(display)
        else:

            # print(form.errors)
            messages.error(request, 'One of the field\'s format is wrong or you are using a duplicated ID!')
            return redirect(add_vlan)
    else:
        form = VLANForm
        return render(request, 'add_vlan.html', {'form':form})



@login_required(login_url="/login")
def edit_device(request, device_id):
    if (request.method) == "POST":
        ids = request.POST.getlist("VLANS")
        # print(ids)
        ids.remove("")

        updated_data = request.POST.copy()
        updated_data.update({'VLANS': json.dumps(ids)})
        updated_data.update({'username': request.user.username})
        device_i = device.objects.all().filter(id=device_id, username=request.user.username)[0]
        form = deviceForm(data=updated_data, instance=device_i)

        if form.is_valid():
            form.save()
            return redirect(display)
        else:
            # print("false")
            messages.error(request, 'One of the field\'s format is wrong or you are using a duplicated ID!')
            return redirect(reverse('edit_device', kwargs={'device_id':device_id}))

    else:
        device_i = device.objects.all().filter(id=device_id, username=request.user.username)[0]

        vlans_sel = []
        try:
            vlans = VLAN.objects.all().filter(LANn_VLAN_ID__in=json.loads(device_i.VLANS), username=request.user.username)
            for nr, vlan in enumerate(vlans):
                vlans_sel.append(vlan.LANn_VLAN_ID)
        except:
            pass

        vlans = VLAN.objects.all().filter(username=request.user.username)
        vlans_dict = {}
        for nr,vlan in enumerate(vlans):
            if vlan.LANn_VLAN_ID in vlans_sel:
                vlans_dict[nr] = {"id":vlan.LANn_VLAN_ID, "name":vlan.LANn_NAME, "checked":True}
            else:
                vlans_dict[nr] = {"id":vlan.LANn_VLAN_ID, "name":vlan.LANn_NAME, "checked":False}


        form = deviceForm
        return render(request, 'edit_device.html', {'form': form, 'device':device_i,'vlans': vlans_dict})

@login_required(login_url="/login")
def duplicate_device(request, device_id):
    device_i = device.objects.all().filter(id=device_id, username=request.user.username)[0]
    device_i.pk = None
    id_ja = 1
    list_is = device.objects.values_list('DEVICE_ID', flat=True)
    while id_ja in list_is:
        id_ja += 1
    device_i.DEVICE_ID = id_ja
    device_i.save()
    return redirect(display)

@login_required(login_url="/login")
def delete_device(request, device_id):
    # print(device_id)
    device.objects.all().filter(id=device_id, username=request.user.username)[0].delete()
    return redirect(display)

@login_required(login_url="/login")
def clear_devices(request):
    device.objects.all().filter(username=request.user.username).delete()
    return redirect(display)



@login_required(login_url="/login")
def edit_vlan(request, vlan_id):
    if (request.method) == "POST":

        vlan_i = VLAN.objects.all().filter(id=vlan_id, username=request.user.username)[0]

        updated_data = request.POST.copy()
        updated_data.update({'username': request.user.username})
        form = VLANForm(data=updated_data, instance=vlan_i)

        if form.is_valid():
            # print(form.errors)
            form.save()
            return redirect(display)
        else:
            messages.error(request, 'One of the field\'s format is wrong or you are using a duplicated ID!')
            return redirect(reverse('edit_vlan', kwargs={'vlan_id':vlan_id}))

    else:
        vlan_i = VLAN.objects.all().filter(id=vlan_id, username=request.user.username)[0]

        form = VLANForm
        return render(request, 'edit_vlan.html', {'form': form, 'vlan':vlan_i})

@login_required(login_url="/login")
def duplicate_vlan(request, vlan_id):
    vlan_i = VLAN.objects.all().filter(id=vlan_id, username=request.user.username)[0]
    vlan_i.pk = None
    id_ja = 1
    list_is = VLAN.objects.values_list('LANn_VLAN_ID', flat=True)
    while id_ja in list_is:
        id_ja += 1
    vlan_i.LANn_VLAN_ID = id_ja
    vlan_i.save()
    return redirect(display)

@login_required(login_url="/login")
def delete_vlan(request, vlan_id):
    # print(vlan_id)
    VLAN.objects.all().filter(id=vlan_id, username=request.user.username)[0].delete()
    return redirect(display)

@login_required(login_url="/login")
def clear_vlans(request):
    VLAN.objects.all().filter(username=request.user.username).delete()
    return redirect(display)

@login_required(login_url="/login")
@csrf_exempt
def export_csv(request):
    if request.method == "POST":
        # print("here")
        ids = json.loads(request.POST.get("ids"))
        devices = device.objects.all().filter(id__in=ids, username=request.user.username)
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="export.csv"'},
        )
        headers = ['SN', 'LAN_NETWORK_LIST', 'LAN_MEDIA', 'LAN_L2_ISO', 'LAN_STROUTEn', 'DHCP_SERVER', 'DHCP_SERVER_LEASE', 'DHCP_SERVER_NETMASK', 'DHCP_SERVER_POOL_START', 'DHCP_SERVER_POOL_END', 'DHCP_RESERVATION', 'DHCP_LOG_ENABLE', 'DHCP_SERVER_DNS', 'DHCP_SERVER_WINS', 'DHCP_OPTION_15', 'DHCP_RELAY_OPTION_82', 'DHCP_RELAY_SERVER']
        bigger = 0
        for nr,i in enumerate(devices):
            if len(VLAN.objects.all().filter(LANn_VLAN_ID__in=json.loads(i.VLANS), username=request.user.username)) > bigger:
                bigger = len(VLAN.objects.all().filter(LANn_VLAN_ID__in=json.loads(i.VLANS), username=request.user.username))
        for nr in range(0,bigger):
            headers = headers+[f'LAN{nr+1}_NAME', f'LAN{nr+1}_NETWORK_LIST', f'LAN{nr+1}_L2_ISO', f'DHCP{nr+1}_SERVER', f'DHCP{nr+1}_SERVER_LEASE', f'DHCP{nr+1}_SERVER_NETMASK', f'DHCP{nr+1}_SERVER_POOL_START', f'DHCP{nr+1}_SERVER_POOL_END', f'DHCP{nr+1}_RESERVATION', f'DHCP{nr+1}_LOG_ENABLE', f'DHCP{nr+1}_SERVER_DNS', f'DHCP{nr+1}_SERVER_WINS', f'DHCP{nr+1}_OPTION_15', f'DHCP{nr+1}_RELAY_OPTION_82', f'DHCP{nr+1}_RELAY_SERVER']

        writer = csv.writer(response)
        writer.writerow(headers)

        for i in devices:
            list_write = [i.SN, i.LAN_NETWORK_LIST, i.LAN_MEDIA, i.LAN_L2_ISO, i.LAN_STROUTEn, i.DHCP_SERVER, i.DHCP_SERVER_LEASE, i.DHCP_SERVER_NETMASK, i.DHCP_SERVER_POOL_START, i.DHCP_SERVER_POOL_END, i.DHCP_RESERVATION, i.DHCP_LOG_ENABLE, i.DHCP_SERVER_DNS, i.DHCP_SERVER_WINS, i.DHCP_OPTION_15, i.DHCP_RELAY_OPTION_82, i.DHCP_RELAY_SERVER]
            for nr, u in enumerate(VLAN.objects.all().filter(LANn_VLAN_ID__in=json.loads(i.VLANS), username=request.user.username)):
                list_write = list_write+[u.LANn_NAME.replace("{ID}",str(i.DEVICE_ID)), u.LANn_NETWORK_LIST.replace("{ID}",str(i.DEVICE_ID)), u.LANn_L2_ISO.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_LEASE.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_NETMASK.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_POOL_START.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_POOL_END.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_RESERVATION.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_LOG_ENABLE.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_DNS.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_WINS.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_OPTION_15.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_RELAY_OPTION_82.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_RELAY_SERVER.replace("{ID}",str(i.DEVICE_ID))]


            writer.writerow(list_write)

        return response

@login_required(login_url="/login")
@csrf_exempt
def export_json(request):
    devices = device.objects.all().filter(username=request.user.username)
    vlans = VLAN.objects.all().filter(username=request.user.username)
    response = HttpResponse(
        content_type='json',
        headers={'Content-Disposition': 'attachment; filename="export.json"'},
    )


    mast_point = serializers.serialize("json", devices)
    response.write(mast_point+"\n")
    mast_point = serializers.serialize("json", vlans)
    response.write(mast_point)

    return response
