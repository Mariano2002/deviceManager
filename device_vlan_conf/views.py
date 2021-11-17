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
from io import StringIO
import zipfile


def import_json(file, username):
    dict = json.loads(file)

    for i in dict:
        inst = i['fields']
        inst['username'] = username
        device.objects.create(**inst)


# def import_csv(file, username):
#     pass

@login_required(login_url="/login")
def display(request):

    if request.method == 'POST':
        file = request.FILES['file'].read().decode('utf-8')
        if request.FILES['file'].name[-5:] == '.json':
            import_json(file, request.user.username)
        # elif request.FILES['file'].name[-4:] == '.csv':
            #import_csv(file, request.user.username)
        else:
            messages.error(request, 'Please upload a CSV or JSON file!')
        return redirect(display)

    else:
        form = UploadFileForm()

        items = device.objects.all().filter(username=request.user.username)
        for item in items:
            print(json.loads(item.VLANS))
            vlans = VLAN.objects.all().filter(id__in=json.loads(item.VLANS), username=request.user.username)
            VLANS_names = []
            for i in vlans:
                VLANS_names.append(i.LANn_NAME)
            item.VLANS_names = ", ".join(VLANS_names)
        print(items)
        vlans = VLAN.objects.all().filter(username=request.user.username)
        return render(request, 'display.html', {'devices':items, 'vlans':vlans, 'form':form})

def user_is_not_logged_in(user):
    return not user.is_authenticated

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(display)
        else:
            messages.error(request, 'Username or password in incorrect')
            return render(request, 'login.html', {})
    else:
        print(request.user)
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







@login_required(login_url="/login")
def add_device(request):
    if(request.method) == "POST":
        ids = request.POST.getlist("VLANS")
        ids.remove("")

        updated_data = request.POST.copy()
        updated_data.update({'VLANS': json.dumps(ids)})
        updated_data.update({'username': request.user.username})
        form = deviceForm(data=updated_data)

        if form.is_valid():
            print(form.errors)
            form.save()
            return redirect(display)
        else:
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
        form = VLANForm(data=updated_data)
        if form.is_valid():
            print(form.errors)
            form.save()
            return redirect(display)
        else:
            return redirect(add_vlan)
    else:
        form = VLANForm
        return render(request, 'add_vlan.html', {'form':form})



@login_required(login_url="/login")
def edit_device(request, device_id):
    if (request.method) == "POST":
        ids = request.POST.getlist("VLANS")
        ids.remove("")

        updated_data = request.POST.copy()
        updated_data.update({'VLANS': json.dumps(ids)})
        updated_data.update({'username': request.user.username})
        device_i = device.objects.all().filter(id=device_id, username=request.user.username)[0]
        form = deviceForm(data=updated_data, instance=device_i)

        if form.is_valid():
            print(form.errors)
            form.save()
            return redirect(display)
        else:
            return redirect(add_device)

    else:
        device_i = device.objects.all().filter(id=device_id, username=request.user.username)[0]


        vlans = VLAN.objects.all().filter(id__in=json.loads(device_i.VLANS), username=request.user.username)
        vlans_sel = []
        for nr, vlan in enumerate(vlans):
            vlans_sel.append(vlan.id)


        vlans = VLAN.objects.all().filter(username=request.user.username)
        vlans_dict = {}
        for nr,vlan in enumerate(vlans):
            if vlan.id in vlans_sel:
                vlans_dict[nr] = {"id":vlan.id, "name":vlan.LANn_NAME, "checked":True}
            else:
                vlans_dict[nr] = {"id":vlan.id, "name":vlan.LANn_NAME, "checked":False}


        form = deviceForm
        return render(request, 'edit_device.html', {'form': form, 'device':device_i,'vlans': vlans_dict})

@login_required(login_url="/login")
def duplicate_device(request, device_id):
    device_i = device.objects.all().filter(id=device_id, username=request.user.username)[0]
    device_i.pk = None
    device_i.save()
    return redirect(display)

@login_required(login_url="/login")
def delete_device(request, device_id):
    print(device_id)
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
            print(form.errors)
            form.save()
            return redirect(display)
        else:
            return redirect(add_device)

    else:
        vlan_i = VLAN.objects.all().filter(id=vlan_id, username=request.user.username)[0]

        form = VLANForm
        return render(request, 'edit_vlan.html', {'form': form, 'vlan':vlan_i})

@login_required(login_url="/login")
def duplicate_vlan(request, vlan_id):
    vlan_i = VLAN.objects.all().filter(id=vlan_id, username=request.user.username)[0]
    vlan_i.pk = None
    vlan_i.save()
    return redirect(display)

@login_required(login_url="/login")
def delete_vlan(request, vlan_id):
    print(vlan_id)
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
        ids = json.loads(request.POST.get("ids"))
        devices = device.objects.all().filter(id__in=ids, username=request.user.username)
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="export.csv"'},
        )
        headers = ['SN', 'LAN_NETWORK_LIST', 'LAN_MEDIA', 'LAN_L2_ISO', 'LAN_STROUTE1', 'DHCP_SERVER', 'DHCP_SERVER_LEASE', 'DHCP_SERVER_NETMASK', 'DHCP_SERVER_POOL_START', 'DHCP_SERVER_POOL_END', 'DHCP_RESERVATION', 'DHCP_LOG_ENABLE', 'DHCP_SERVER_DNS', 'DHCP_SERVER_WINS', 'DHCP_OPTION_15', 'DHCP_RELAY_OPTION_82', 'DHCP_RELAY_SERVER']
        bigger = 0
        for nr,i in enumerate(devices):
            if len(VLAN.objects.all().filter(id__in=json.loads(i.VLANS), username=request.user.username)) > bigger:
                bigger = len(VLAN.objects.all().filter(id__in=json.loads(i.VLANS), username=request.user.username))
        for nr in range(0,bigger):
            headers = headers+[f'LAN{nr+1}_NAME', f'LAN{nr+1}_NETWORK_LIST', f'LAN{nr+1}_L2_ISO', f'DHCP{nr+1}_SERVER', f'DHCP{nr+1}_SERVER_LEASE', f'DHCP{nr+1}_SERVER_NETMASK', f'DHCP{nr+1}_SERVER_POOL_START', f'DHCP{nr+1}_SERVER_POOL_END', f'DHCP{nr+1}_RESERVATION', f'DHCP{nr+1}_LOG_ENABLE', f'DHCP{nr+1}_SERVER_DNS', f'DHCP{nr+1}_SERVER_WINS', f'DHCP{nr+1}_OPTION_15', f'DHCP{nr+1}_RELAY_OPTION_82', f'DHCP{nr+1}_RELAY_SERVER']

        writer = csv.writer(response)
        writer.writerow(headers)

        for i in devices:
            list_write = [i.SN, i.LAN_NETWORK_LIST, i.LAN_MEDIA, i.LAN_L2_ISO, i.LAN_STROUTEn, i.DHCP_SERVER, i.DHCP_SERVER_LEASE, i.DHCP_SERVER_NETMASK, i.DHCP_SERVER_POOL_START, i.DHCP_SERVER_POOL_END, i.DHCP_RESERVATION, i.DHCP_LOG_ENABLE, i.DHCP_SERVER_DNS, i.DHCP_SERVER_WINS, i.DHCP_OPTION_15, i.DHCP_RELAY_OPTION_82, i.DHCP_RELAY_SERVER]
            for nr, u in enumerate(VLAN.objects.all().filter(id__in=json.loads(i.VLANS), username=request.user.username)):
                list_write = list_write+[u.LANn_NAME.replace("{ID}",str(i.DEVICE_ID)), u.LANn_NETWORK_LIST.replace("{ID}",str(i.DEVICE_ID)), u.LANn_L2_ISO.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_LEASE.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_NETMASK.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_POOL_START.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_POOL_END.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_RESERVATION.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_LOG_ENABLE.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_DNS.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_SERVER_WINS.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_OPTION_15.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_RELAY_OPTION_82.replace("{ID}",str(i.DEVICE_ID)), u.DHCPn_RELAY_SERVER.replace("{ID}",str(i.DEVICE_ID))]


            writer.writerow(list_write)

        return response

@login_required(login_url="/login")
@csrf_exempt
def export_json(request):
    devices = device.objects.all().filter(username=request.user.username)
    response = HttpResponse(
        content_type='json',
        headers={'Content-Disposition': 'attachment; filename="export.json"'},
    )


    mast_point = serializers.serialize("json", devices)
    response.write(mast_point)

    return response
