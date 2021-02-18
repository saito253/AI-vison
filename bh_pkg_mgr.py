#!/usr/bin/python3

import os

PKG_FILE = "/var/lib/dpkg/status"
LIC = "/usr/share/doc/"

pkg=0
dpd=0
lic=0
hmp=0
unknown=0

def get_license(pkg_name):
  global lic
  global unknown

  cnt=0

  LIC_FILE = LIC + pkg_name + "/copyright"
  if os.path.exists(LIC_FILE) == True:
    print("Copyright:",LIC_FILE)
    f_copyright = open(LIC_FILE, 'r')

    for data in f_copyright:
      name = data.split(" ")
      #datalist = f_copyright.readlines()
      if "License:" == name[0]:
        cnt=1
        print(data.strip('License: \r \n'),end='')
      elif "Public License:" == name[0]:
        cnt=1
        print(data.strip('License: \r \n'),end='')

    if cnt == 0:
      unknown += 1 
    else:
      lic += 1

    f_copyright.close()

def make_list():
  global pkg
  global dpd
  global lic
  global unknown
  global hmp
  f_status = open(PKG_FILE, 'r')

  #print (datalist)
  #datalist = f.readlines()
  #print(datalist,end='')

  for data in f_status:
    name = data.split(" ")

    if "Package:" == name[0]:
      print("-------------------------------------------------------------")
      print(data.rstrip('\n'))
      pkg += 1
      pkg_name = data.split()
      if "chromium-" in pkg_name[1]:
        continue
      get_license(pkg_name[1])
      
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
print("============= Pakeging License Summary ===========")
print("Package: ",pkg)
print("Depends: ",dpd)
print("License: ",lic)
print("Unknown License: ",unknown)
print("Homepage: ",hmp)
print("==================================================")

