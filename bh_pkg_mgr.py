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
n_param=0

LIC_LIMIT = 10
MAX_PARAM = 5

def get_license(pkg_name):
  global lic
  global unknown
  global cpy
  global n_param

  cnt=0

  LIC_FILE = LIC + pkg_name + "/copyright"
  if os.path.exists(LIC_FILE) == True:
    print("Copyright:",LIC_FILE)
    cpy+=1
    n_param += 1
    f_copyright = open(LIC_FILE, 'r')

    print('License: ', end='')
    n_param += 1
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

  else:
    unknown += 1 
    n_param += 2
    print("Copyright: unknown\r")
    print("License: unknown\r")

def make_list():
  global pkg
  global lic
  global ver
  global dpd
  global hmp
  global n_param

  f_status = open(PKG_FILE, 'r')

  for data in f_status:
    name = data.split(" ")

    if "Package:" == name[0]:
      if n_param > 0 & n_param < 5 :
        print("Homepage: unknown\r")
      n_param = 0
      print("-------------------------------------------------------------")
      print(data.rstrip('\n'))
      pkg += 1
      n_param += 1
      pkg_name = data.split()
      get_license(pkg_name[1])
      
    elif "Version:" == name[0]:
      print(data.rstrip('\n'))
      ver += 1
      n_param += 1
  # elif "Depends:" == name[0]:
  #   print(data.rstrip('\n'))
  #   dpd += 1
  # elif "Description:" in data:
  #   print(data.rstrip('\n'))
  # elif "License" in data:
  #   print(data.rstrip('\n'))
    elif "Homepage:" == name[0]:
      print(data.rstrip('\n'))
      hmp += 1
      n_param += 1

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
print("Reliability: ",'{:.2%}'.format(lic/pkg))
print("Unknown License: ",unknown)
print("Homepage: ",hmp)
print("Copyright:",cpy)
print("==================================================")

