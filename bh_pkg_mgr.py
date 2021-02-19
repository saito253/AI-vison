#!/usr/bin/python3

import subprocess
import os

PKG_FILE = "/var/lib/dpkg/status"
LIC = "/usr/share/doc/"

pkg=0
ver=0
dpd=0
lic=0
hmp=0
unknown=0

LIC_LIMIT = 10

def get_license(pkg_name):
  global lic
  global unknown

  cnt=0

  LIC_FILE = LIC + pkg_name + "/copyright"
  if os.path.exists(LIC_FILE) == True:
#   print("Copyright:",LIC_FILE)
    f_copyright = open(LIC_FILE, 'r')

    print('License:', end='')
    for data in f_copyright:
      name = data.split(" ")
      if "License:" == name[0]:
        #print(data.strip('License:\r\n'), end='')
        print(data.replace('License:','').replace('\n',''), end='')
        cnt+=1
      elif "Public License:" == name[0]:
        #print(data.replace('License:\r\n',''), end='')
        print(data.replace('License:','').replace('\n',''), end='')
        cnt+=1

      if "chromium-" in pkg_name:
        break
      if cnt > LIC_LIMIT:
        break

    if cnt == 0:
      unknown += 1 
      print(' unknown\r')
    else:
      lic += 1
      print('\r')


    f_copyright.close()

def make_list():
  global pkg
  global lic
  global ver
  global dpd
  global unknown
  global hmp
  f_status = open(PKG_FILE, 'r')

  for data in f_status:
    name = data.split(" ")

    if "Package:" == name[0]:
      print("-------------------------------------------------------------")
      print(data.rstrip('\n'))
      pkg += 1
      pkg_name = data.split()
      get_license(pkg_name[1])
      
    elif "Version:" == name[0]:
      print(data.rstrip('\n'))
      ver += 1
    elif "Depends:" == name[0]:
      print(data.rstrip('\n'))
      dpd += 1
  # elif "Description:" in data:
  #   print(data.rstrip('\n'))
  # elif "License" in data:
  #   print(data.rstrip('\n'))
    elif "Homepage:" == name[0]:
      print(data.rstrip('\n'))
      hmp += 1

  f_status.close()


make_list()

print("\n")
print("============= Distribution Specific ==========")
result = subprocess.run(["lsb_release","-a"], stdout=subprocess.PIPE)
print("OS version: ",result.stdout.decode("utf-8"), end='')
result = subprocess.run(["uname","-r"], stdout=subprocess.PIPE)
print("OS version: ",result.stdout.decode("utf-8"), end='')
print("============= Pakeging License Summary ===========")
print("Package: ",pkg)
print("Version: ",ver)
print("Depends: ",dpd)
print("License: ",lic)
print("Unknown License: ",unknown)
print("Homepage: ",hmp)
print("==================================================")

