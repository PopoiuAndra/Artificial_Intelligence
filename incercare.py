import os
import sys

file = sys.argv[1]
print(file)

try:
    if os.path.exists(file) == False:
        raise FileExistsError
except FileExistsError as e:
    print(e)

f = open(file, "+r")
fileContent = f.read()
print(fileContent)

class FileEmpty (Exception):
    def __init__(self, *args):
        super().__init__(*args)

try:
    if len(fileContent) == 0:
        raise FileEmpty
except FileEmpty:
    print("File is empty")

addresses = fileContent.split("\n")
addresses.sort()
print([i for i in addresses])

setAddresses = set(addresses)
print([i for i in setAddresses])

ip4 = [i for i in addresses if i.count(".") == 3]
print([i for i in ip4])

newip4 = []
for i in ip4:
    ok = 0
    i = str(i)
    for j in range(0, 4):
        if int(i.split(".")[j]) < 0 or int(i.split(".")[j]) > 255: # int is new
            ok = 1
    if ok ==0:
        newip4.append(i)
print([i for i in newip4])


ip6 = [i for i in addresses if i.count(":") == 7]
print([i for i in ip6])

newip6 = []
for i in ip6:
    ok = 0
    i = str(i)
    for j in range(0, 8):
        if len(i.split(":")[j]) < 0 or len(i.split(":")[j]) > 4:
            ok = 1
    if ok ==0:
        newip6.append(i)
print([i for i in newip6])

addresses = newip4 + newip6 # new
setAddresses = set(addresses) # from above

print("Addresses:")
for i in setAddresses:
        print(i)

addresses = list(setAddresses) # new
addresses.sort()
addresses.sort(key = lambda x : x.count(":"))
print(addresses)

