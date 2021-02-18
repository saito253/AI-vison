#!/usr/bin/python3

import os

PKG_FILE = "/var/lib/dpkg/status"
LIC = "/usr/share/doc/"


def get_license(pkg_name):
  val = 0
  cnt = 0
  lic = LIC + pkg_name + "/copyright"
  if os.path.exists(lic) == True:
    print("Copyright:",lic)
    f_copyright = open(lic, 'r')

    for data in f_copyright:
      name = data.split(" ")
      #datalist = f_copyright.readlines()
      if "License:" == name[0]:
        print(data.rstrip('\n'))
        val = 1
        cnt += 1
        if cnt > 5:
          break
      elif "Public License:" == name[0]:
        print(data.rstrip('\n'))
        val = 1
        cnt += 1
        if cnt > 5:
          break

    f_copyright.close()
  return val

def make_list():
  pkg=0
  dpd=0
  lic=0
  hmp=0

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
      lic += get_license(pkg_name[1])
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

  print("\n")
  print("=================== SUMMARY ====================")
  print("Package: ",pkg)
  print("Depends: ",dpd)
  print("License: ",lic)
  print("Homepage: ",hmp)

make_list()


