#!/usr/bin/python3

import subprocess
import os
import sys

PKG_FILE = "/var/lib/dpkg/status"
LIC = "/usr/share/doc/"

pkg=0
cpy=0
ver=0
dpd=0
lic=0
hmp=0
unknown=0

LIC_LIMIT = 10

def get_license(pkg_name):
  global lic
  global unknown
  global cpy

  cnt=0

  LIC_FILE = LIC + pkg_name + "/copyright"
  if os.path.exists(LIC_FILE) == True:
    if (len(sys.argv) > 1) and (sys.argv[1] == "copyright"):
        print("Copyright:",LIC_FILE)
        cpy+=1
    f_copyright = open(LIC_FILE, 'r')

    print('License: ', end='')
    for data in f_copyright:
      name = data.split(" ")
      if "License:" == name[0]:
        #print(data.strip('License:\r\n'), end='')
        print(data.replace('License:','').replace('\n',''), end='')
        cnt+=1
      elif "common-licenses" in data:
#       print(data.replace('License:','').replace('\n',''), end='')
        print(" ",data.replace('\n','')," ", end='')
        cnt+=1
      elif "(1) GPL-compatible" in data:
        print('GPL-compatible', end='')
        cnt+=1


#     if "chromium-" in pkg_name:
#       break
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
  chk=1
  f_status = open(PKG_FILE, 'r')

  for data in f_status:
    name = data.split(" ")

    if "Package:" == name[0]:
      pkg+=1
      if chk == 0:
        print("non")
      chk=0
    elif "Homepage:" == name[0]:
#     print(data.rstrip('\n'))
      print(data.replace('Homepage:','').replace('\n',''))
      hmp+=1
      chk=1

  f_status.close()


make_list()

print("\n")
if len(sys.argv) > 1:
  arg_name = sys.argv[1]
else:
  arg_name =""
print("command arg: ",len(sys.argv),arg_name)
print("============= Distribution Specific ==========")
result = subprocess.run(["lsb_release","-a"], stdout=subprocess.PIPE)
print("OS version: ",result.stdout.decode("utf-8"), end='')
result = subprocess.run(["uname","-r"], stdout=subprocess.PIPE)
print("OS version: ",result.stdout.decode("utf-8"), end='')
print("============= Pakeging License Summary ===========")
print("Package: ",pkg)
print("Version: ",ver)
print("Depends: ",dpd)
print("Unknown License: ",unknown)
print("Homepage: ",hmp)
print("==================================================")

