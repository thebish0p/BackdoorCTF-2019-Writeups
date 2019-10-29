# Challenge
>Kratos is back with another one of his weird encryption schemes, confident he'll stump sin3point14 with this one. This time we' were only able to recover a small snippet of the encryption code. Show him up!
>
>http://backdoor.static.beast.sdslabs.co/static/MineCraft/mine.py
>
>http://backdoor.static.beast.sdslabs.co/static/MineCraft/flag.enc

# Checking the files

Started with reading the `mine.py` script :

```python
def revmine(block):
    bl = block
    i = 0
    while True:
        i+=1
        sid = hexhash(long_to_bytes(block['nonce'])+long_to_bytes(i)+block['prev'].encode('utf-8'))
        if sid[:3] == '000':
            bl['data'] = i
            bl['self'] = sid
            bl['nonce'] = (s1*i+s2)%s3
            return bl
```

After checking the `flag.enc` file, you can notice that it's a list with JSON array elements all having the same format:

`{"self": "0006360358c874c74db5405a05f6a1f2292ef51a4259d680904fb9dff1c6065f", "hashalg": "sha256", "prev": "00059001dc03d12843d751d77380193db2744b20688709e4aa0b66aec25b663a", "data": 3266, "nonce": 9612}`

# Sorting `flag.enc`

So first of all I had to sort the list by using the fact the we had a `prev` parameter. 
Now for the starting point we had one of these `prev` parameters with a value of `0000000000000000` as shown below:

`{"self": "000696a373a18fd86df43d463bb6b45562d1969e7d4face2c57dadc42a3d9900", "hashalg": "sha256", "prev": "0000000000000000", "data": 1463, "nonce": 168627}`

Wrote this script to sort it: 

```python
unsorted = [{"self": "0006360358c874c74db5405a05f6a1f2292ef51a4259d680904fb9dff1c6065f", "hashalg": "sha256", "prev": "00059001dc03d12843d751d77380193db2744b20688709e4aa0b66aec25b663a", "data": 3266, "nonce": 9612}, {"self": "0001c29e66d881b64d52c3047cd7cabb42627ae7a391bd91366179c0986313ae", "hashalg": "sha256", "prev": "00024c6de28c0f4a79975b883438eb68a13d23a32306db532fc0695caf925c73", "data": 1884, "nonce": 82297}, {"self": "000d2754912042d664297a06cabeca18caba043e20a596380c55d9884d504c0d", "hashalg": "sha256", "prev": "000bcf82ac772e8ab1a81bb7cb345767222adbc84a15148f14fd7d4b0c928ece", "data": 96, "nonce": 135881}, {"self": "000cc5baf584f2e60f2d15b13fda597bfe73cf8d01f6af6f2ccb7c16e38961ec", "hashalg": "sha256", "prev": "00077571e98da3d6ea8c548cd3ad79b4f1a4184ef919162d9f9e4e0336510754", "data": 2191, "nonce": 108759}, {"self": "000e460df9c4d20988ebb005b32c795254344a541cb5bba62a525f31938cf453", "hashalg": "sha256", "prev": "00095a61d6d80787b5b87b08a61980e7cd2d5b5c5efd834b9b18d45cac728746", "data": 1508, "nonce": 12775}, {"self": "000bcf82ac772e8ab1a81bb7cb345767222adbc84a15148f14fd7d4b0c928ece", "hashalg": "sha256", "prev": "000438380a0b40f3c305ee6978126ea99fad449435b38b13094b830ccdc63279", "data": 2924, "nonce": 93731}, {"self": "00037ac7cc89ed20beb21b711ff8a61335433f34040ae514297166bc232c57e8", "hashalg": "sha256", "prev": "000c6b2546012ecd628cee3fc069486d01620194d73c4ddcbcf3d91e63c5aa62", "data": 1246, "nonce": 123410}, {"self": "000cb3cd8754e5fff7090d83d40c8def7148472b82a74ed3e399799731265ab4", "hashalg": "sha256", "prev": "00005fd4066a0bbc11b9f4cabdec2b45da2081b1247e37be8371bb49bb4380fb", "data": 4043, "nonce": 76839}, {"self": "000a301d1a676a95d666cd232f8d39d820ea418e25b6ff7181cb7d195387bc6b", "hashalg": "sha256", "prev": "0004997ceb55ffc2c4668b8e8cc793fdb35f71b882dfa3a901a301cc27e9d23b", "data": 623, "nonce": 144788}, {"self": "000b0465f128e7665ad65a88058b1b3cd47e5fac09bf255f376e38b6ab1953c0", "hashalg": "sha256", "prev": "000cc5baf584f2e60f2d15b13fda597bfe73cf8d01f6af6f2ccb7c16e38961ec", "data": 262, "nonce": 110080}, {"self": "000785c0ab42b1f302e4fac06c993329cd04182cb0b6937580a6c513d31a47e3", "hashalg": "sha256", "prev": "0005e26d1603f90023055da92c6da4105f5658cc04e8cff5df3b68318020d53e", "data": 1064, "nonce": 50878}, {"self": "000205a1f746ce4d7e85201e4dfdb8b8fcd51a4fc7792d63f067acf3c38ed4eb", "hashalg": "sha256", "prev": "000e460df9c4d20988ebb005b32c795254344a541cb5bba62a525f31938cf453", "data": 3953, "nonce": 58008}, {"self": "000aecec3740a8f74e515bbc972151b1a12ad65241ad40eaea6e3eda599ca0da", "hashalg": "sha256", "prev": "000cfa99368782e33834cfba222ebb9253c7601ffc48828c10e35f3677dd0767", "data": 3135, "nonce": 36015}, {"self": "00059001dc03d12843d751d77380193db2744b20688709e4aa0b66aec25b663a", "hashalg": "sha256", "prev": "0000d24c81093053b703c6f8f9af47b0d82db9cb705bdfa6ec7c332f7fa59959", "data": 1506, "nonce": 100358}, {"self": "00024c6de28c0f4a79975b883438eb68a13d23a32306db532fc0695caf925c73", "hashalg": "sha256", "prev": "000e0a9e7803407d694e661f55c381fdc419f2443dd08834b18eac7e6ca8e663", "data": 538, "nonce": 145210}, {"self": "00068eb9ca8118fb1c36e6506735b9c36b367295bafd5cb69ca924c96912654e", "hashalg": "sha256", "prev": "0001c29e66d881b64d52c3047cd7cabb42627ae7a391bd91366179c0986313ae", "data": 7653, "nonce": 148147}, {"self": "00021ab3a179e72d866237dc0a1b06154bea14f364a28b52f27a71c9d50844c5", "hashalg": "sha256", "prev": "000b0465f128e7665ad65a88058b1b3cd47e5fac09bf255f376e38b6ab1953c0", "data": 1652, "nonce": 158747}, {"self": "0005e26d1603f90023055da92c6da4105f5658cc04e8cff5df3b68318020d53e", "hashalg": "sha256", "prev": "00068eb9ca8118fb1c36e6506735b9c36b367295bafd5cb69ca924c96912654e", "data": 18415, "nonce": 94814}, {"self": "000306cced42beebc205528556da2768eeb89ef0fb14c159ad0aa983173e0d2d", "hashalg": "sha256", "prev": "00047ed893413ad3493edad7fc5fb0978b328abc7879de174a679145709b837f", "data": 1736, "nonce": 58094}, {"self": "0000d24c81093053b703c6f8f9af47b0d82db9cb705bdfa6ec7c332f7fa59959", "hashalg": "sha256", "prev": "000aecec3740a8f74e515bbc972151b1a12ad65241ad40eaea6e3eda599ca0da", "data": 1104, "nonce": 17867}, {"self": "000e6abeebc1d08583e4aa28fd9432bd3caf54b721bd5a297257657ce0237d47", "hashalg": "sha256", "prev": "000205a1f746ce4d7e85201e4dfdb8b8fcd51a4fc7792d63f067acf3c38ed4eb", "data": 1226, "nonce": 66864}, {"self": "000f7b4a89a94e4ce20ce8de7167019d868f4c08e885628ce8db4151922bfcbd", "hashalg": "sha256", "prev": "000306cced42beebc205528556da2768eeb89ef0fb14c159ad0aa983173e0d2d", "data": 1212, "nonce": 36782}, {"self": "00007098ba1dc82839480ee7eba6c33ee1fa862817b0d23688249cac98e23fa9", "hashalg": "sha256", "prev": "000d28d1dfbdc471ccd5f9ad101cd1135f2e8e489e7c1c19a112973e050fa176", "data": 9684, "nonce": 152499}, {"self": "000cfa99368782e33834cfba222ebb9253c7601ffc48828c10e35f3677dd0767", "hashalg": "sha256", "prev": "000cb3cd8754e5fff7090d83d40c8def7148472b82a74ed3e399799731265ab4", "data": 598, "nonce": 59792}, {"self": "000af0317d944684e0609b12e83269d2f4e08ec6e62e4f8a45354b13b9b3ac02", "hashalg": "sha256", "prev": "0003f76fab1f9eb0da494187daaea480ca2913f7c7332977a4f0484bac55a812", "data": 10127, "nonce": 159119}, {"self": "000c6b2546012ecd628cee3fc069486d01620194d73c4ddcbcf3d91e63c5aa62", "hashalg": "sha256", "prev": "00067bba440d65b9a20a9d6e1dd4b95a3269e09ede1ffba2d98a429dbd6209ce", "data": 6611, "nonce": 58723}, {"self": "0003f76fab1f9eb0da494187daaea480ca2913f7c7332977a4f0484bac55a812", "hashalg": "sha256", "prev": "00021ab3a179e72d866237dc0a1b06154bea14f364a28b52f27a71c9d50844c5", "data": 7824, "nonce": 169585}, {"self": "00077571e98da3d6ea8c548cd3ad79b4f1a4184ef919162d9f9e4e0336510754", "hashalg": "sha256", "prev": "000e6abeebc1d08583e4aa28fd9432bd3caf54b721bd5a297257657ce0237d47", "data": 3280, "nonce": 139029}, {"self": "000696a373a18fd86df43d463bb6b45562d1969e7d4face2c57dadc42a3d9900", "hashalg": "sha256", "prev": "0000000000000000", "data": 1463, "nonce": 168627}, {"self": "0004997ceb55ffc2c4668b8e8cc793fdb35f71b882dfa3a901a301cc27e9d23b", "hashalg": "sha256", "prev": "000785c0ab42b1f302e4fac06c993329cd04182cb0b6937580a6c513d31a47e3", "data": 501, "nonce": 38337}, {"self": "00067bba440d65b9a20a9d6e1dd4b95a3269e09ede1ffba2d98a429dbd6209ce", "hashalg": "sha256", "prev": "00007098ba1dc82839480ee7eba6c33ee1fa862817b0d23688249cac98e23fa9", "data": 223, "nonce": 33336}, {"self": "00095a61d6d80787b5b87b08a61980e7cd2d5b5c5efd834b9b18d45cac728746", "hashalg": "sha256", "prev": "000f7b4a89a94e4ce20ce8de7167019d868f4c08e885628ce8db4151922bfcbd", "data": 6797, "nonce": 167808}, {"self": "00047ed893413ad3493edad7fc5fb0978b328abc7879de174a679145709b837f", "hashalg": "sha256", "prev": "000d2754912042d664297a06cabeca18caba043e20a596380c55d9884d504c0d", "data": 1525, "nonce": 140375}, {"self": "000438380a0b40f3c305ee6978126ea99fad449435b38b13094b830ccdc63279", "hashalg": "sha256", "prev": "00037ac7cc89ed20beb21b711ff8a61335433f34040ae514297166bc232c57e8", "data": 1404, "nonce": 107981}, {"self": "000e0a9e7803407d694e661f55c381fdc419f2443dd08834b18eac7e6ca8e663", "hashalg": "sha256", "prev": "0006360358c874c74db5405a05f6a1f2292ef51a4259d680904fb9dff1c6065f", "data": 681, "nonce": 74259}, {"self": "00005fd4066a0bbc11b9f4cabdec2b45da2081b1247e37be8371bb49bb4380fb", "hashalg": "sha256", "prev": "000696a373a18fd86df43d463bb6b45562d1969e7d4face2c57dadc42a3d9900", "data": 253, "nonce": 98980}, {"self": "000d28d1dfbdc471ccd5f9ad101cd1135f2e8e489e7c1c19a112973e050fa176", "hashalg": "sha256", "prev": "000a301d1a676a95d666cd232f8d39d820ea418e25b6ff7181cb7d195387bc6b", "data": 971, "nonce": 136984}]
current = "0000000000000000"
sortedlist = []
while True:
    for elem in unsorted:
        if elem["prev"] == current:
            sortedlist.append(elem)
            current = elem["self"]
    if len(unsorted) == len(sortedlist):
        break
print(sortedlist)
```
# Getting the FLAG

Wrote a script to bruteforce through the ASCII table in order to get the same sha256 hashed `self` parameter as shown below :

```python
import hashlib
from Crypto.Util.number import long_to_bytes

sortedlist = [{'nonce': 168627, 'self': '000696a373a18fd86df43d463bb6b45562d1969e7d4face2c57dadc42a3d9900', 'prev': '0000000000000000', 'data': 1463, 'hashalg': 'sha256'}, {'nonce': 98980, 'self': '00005fd4066a0bbc11b9f4cabdec2b45da2081b1247e37be8371bb49bb4380fb', 'prev': '000696a373a18fd86df43d463bb6b45562d1969e7d4face2c57dadc42a3d9900', 'data': 253, 'hashalg': 'sha256'}, {'nonce': 76839, 'self': '000cb3cd8754e5fff7090d83d40c8def7148472b82a74ed3e399799731265ab4', 'prev': '00005fd4066a0bbc11b9f4cabdec2b45da2081b1247e37be8371bb49bb4380fb', 'data': 4043, 'hashalg': 'sha256'}, {'nonce': 59792, 'self': '000cfa99368782e33834cfba222ebb9253c7601ffc48828c10e35f3677dd0767', 'prev': '000cb3cd8754e5fff7090d83d40c8def7148472b82a74ed3e399799731265ab4', 'data': 598, 'hashalg': 'sha256'}, {'nonce': 36015, 'self': '000aecec3740a8f74e515bbc972151b1a12ad65241ad40eaea6e3eda599ca0da', 'prev': '000cfa99368782e33834cfba222ebb9253c7601ffc48828c10e35f3677dd0767', 'data': 3135, 'hashalg': 'sha256'}, {'nonce': 17867, 'self': '0000d24c81093053b703c6f8f9af47b0d82db9cb705bdfa6ec7c332f7fa59959', 'prev': '000aecec3740a8f74e515bbc972151b1a12ad65241ad40eaea6e3eda599ca0da', 'data': 1104, 'hashalg': 'sha256'}, {'nonce': 100358, 'self': '00059001dc03d12843d751d77380193db2744b20688709e4aa0b66aec25b663a', 'prev': '0000d24c81093053b703c6f8f9af47b0d82db9cb705bdfa6ec7c332f7fa59959', 'data': 1506, 'hashalg': 'sha256'}, {'nonce': 9612, 'self': '0006360358c874c74db5405a05f6a1f2292ef51a4259d680904fb9dff1c6065f', 'prev': '00059001dc03d12843d751d77380193db2744b20688709e4aa0b66aec25b663a', 'data': 3266, 'hashalg': 'sha256'}, {'nonce': 74259, 'self': '000e0a9e7803407d694e661f55c381fdc419f2443dd08834b18eac7e6ca8e663', 'prev': '0006360358c874c74db5405a05f6a1f2292ef51a4259d680904fb9dff1c6065f', 'data': 681, 'hashalg': 'sha256'}, {'nonce': 145210, 'self': '00024c6de28c0f4a79975b883438eb68a13d23a32306db532fc0695caf925c73', 'prev': '000e0a9e7803407d694e661f55c381fdc419f2443dd08834b18eac7e6ca8e663', 'data': 538, 'hashalg': 'sha256'}, {'nonce': 82297, 'self': '0001c29e66d881b64d52c3047cd7cabb42627ae7a391bd91366179c0986313ae', 'prev': '00024c6de28c0f4a79975b883438eb68a13d23a32306db532fc0695caf925c73', 'data': 1884, 'hashalg': 'sha256'}, {'nonce': 148147, 'self': '00068eb9ca8118fb1c36e6506735b9c36b367295bafd5cb69ca924c96912654e', 'prev': '0001c29e66d881b64d52c3047cd7cabb42627ae7a391bd91366179c0986313ae', 'data': 7653, 'hashalg': 'sha256'}, {'nonce': 94814, 'self': '0005e26d1603f90023055da92c6da4105f5658cc04e8cff5df3b68318020d53e', 'prev': '00068eb9ca8118fb1c36e6506735b9c36b367295bafd5cb69ca924c96912654e', 'data': 18415, 'hashalg': 'sha256'}, {'nonce': 50878, 'self': '000785c0ab42b1f302e4fac06c993329cd04182cb0b6937580a6c513d31a47e3', 'prev': '0005e26d1603f90023055da92c6da4105f5658cc04e8cff5df3b68318020d53e', 'data': 1064, 'hashalg': 'sha256'}, {'nonce': 38337, 'self': '0004997ceb55ffc2c4668b8e8cc793fdb35f71b882dfa3a901a301cc27e9d23b', 'prev': '000785c0ab42b1f302e4fac06c993329cd04182cb0b6937580a6c513d31a47e3', 'data': 501, 'hashalg': 'sha256'}, {'nonce': 144788, 'self': '000a301d1a676a95d666cd232f8d39d820ea418e25b6ff7181cb7d195387bc6b', 'prev': '0004997ceb55ffc2c4668b8e8cc793fdb35f71b882dfa3a901a301cc27e9d23b', 'data': 623, 'hashalg': 'sha256'}, {'nonce': 136984, 'self': '000d28d1dfbdc471ccd5f9ad101cd1135f2e8e489e7c1c19a112973e050fa176', 'prev': '000a301d1a676a95d666cd232f8d39d820ea418e25b6ff7181cb7d195387bc6b', 'data': 971, 'hashalg': 'sha256'}, {'nonce': 152499, 'self': '00007098ba1dc82839480ee7eba6c33ee1fa862817b0d23688249cac98e23fa9', 'prev': '000d28d1dfbdc471ccd5f9ad101cd1135f2e8e489e7c1c19a112973e050fa176', 'data': 9684, 'hashalg': 'sha256'}, {'nonce': 33336, 'self': '00067bba440d65b9a20a9d6e1dd4b95a3269e09ede1ffba2d98a429dbd6209ce', 'prev': '00007098ba1dc82839480ee7eba6c33ee1fa862817b0d23688249cac98e23fa9', 'data': 223, 'hashalg': 'sha256'}, {'nonce': 58723, 'self': '000c6b2546012ecd628cee3fc069486d01620194d73c4ddcbcf3d91e63c5aa62', 'prev': '00067bba440d65b9a20a9d6e1dd4b95a3269e09ede1ffba2d98a429dbd6209ce', 'data': 6611, 'hashalg': 'sha256'}, {'nonce': 123410, 'self': '00037ac7cc89ed20beb21b711ff8a61335433f34040ae514297166bc232c57e8', 'prev': '000c6b2546012ecd628cee3fc069486d01620194d73c4ddcbcf3d91e63c5aa62', 'data': 1246, 'hashalg': 'sha256'}, {'nonce': 107981, 'self': '000438380a0b40f3c305ee6978126ea99fad449435b38b13094b830ccdc63279', 'prev': '00037ac7cc89ed20beb21b711ff8a61335433f34040ae514297166bc232c57e8', 'data': 1404, 'hashalg': 'sha256'}, {'nonce': 93731, 'self': '000bcf82ac772e8ab1a81bb7cb345767222adbc84a15148f14fd7d4b0c928ece', 'prev': '000438380a0b40f3c305ee6978126ea99fad449435b38b13094b830ccdc63279', 'data': 2924, 'hashalg': 'sha256'}, {'nonce': 135881, 'self': '000d2754912042d664297a06cabeca18caba043e20a596380c55d9884d504c0d', 'prev': '000bcf82ac772e8ab1a81bb7cb345767222adbc84a15148f14fd7d4b0c928ece', 'data': 96, 'hashalg': 'sha256'}, {'nonce': 140375, 'self': '00047ed893413ad3493edad7fc5fb0978b328abc7879de174a679145709b837f', 'prev': '000d2754912042d664297a06cabeca18caba043e20a596380c55d9884d504c0d', 'data': 1525, 'hashalg': 'sha256'}, {'nonce': 58094, 'self': '000306cced42beebc205528556da2768eeb89ef0fb14c159ad0aa983173e0d2d', 'prev': '00047ed893413ad3493edad7fc5fb0978b328abc7879de174a679145709b837f', 'data': 1736, 'hashalg': 'sha256'}, {'nonce': 36782, 'self': '000f7b4a89a94e4ce20ce8de7167019d868f4c08e885628ce8db4151922bfcbd', 'prev': '000306cced42beebc205528556da2768eeb89ef0fb14c159ad0aa983173e0d2d', 'data': 1212, 'hashalg': 'sha256'}, {'nonce': 167808, 'self': '00095a61d6d80787b5b87b08a61980e7cd2d5b5c5efd834b9b18d45cac728746', 'prev': '000f7b4a89a94e4ce20ce8de7167019d868f4c08e885628ce8db4151922bfcbd', 'data': 6797, 'hashalg': 'sha256'}, {'nonce': 12775, 'self': '000e460df9c4d20988ebb005b32c795254344a541cb5bba62a525f31938cf453', 'prev': '00095a61d6d80787b5b87b08a61980e7cd2d5b5c5efd834b9b18d45cac728746', 'data': 1508, 'hashalg': 'sha256'}, {'nonce': 58008, 'self': '000205a1f746ce4d7e85201e4dfdb8b8fcd51a4fc7792d63f067acf3c38ed4eb', 'prev': '000e460df9c4d20988ebb005b32c795254344a541cb5bba62a525f31938cf453', 'data': 3953, 'hashalg': 'sha256'}, {'nonce': 66864, 'self': '000e6abeebc1d08583e4aa28fd9432bd3caf54b721bd5a297257657ce0237d47', 'prev': '000205a1f746ce4d7e85201e4dfdb8b8fcd51a4fc7792d63f067acf3c38ed4eb', 'data': 1226, 'hashalg': 'sha256'}, {'nonce': 139029, 'self': '00077571e98da3d6ea8c548cd3ad79b4f1a4184ef919162d9f9e4e0336510754', 'prev': '000e6abeebc1d08583e4aa28fd9432bd3caf54b721bd5a297257657ce0237d47', 'data': 3280, 'hashalg': 'sha256'}, {'nonce': 108759, 'self': '000cc5baf584f2e60f2d15b13fda597bfe73cf8d01f6af6f2ccb7c16e38961ec', 'prev': '00077571e98da3d6ea8c548cd3ad79b4f1a4184ef919162d9f9e4e0336510754', 'data': 2191, 'hashalg': 'sha256'}, {'nonce': 110080, 'self': '000b0465f128e7665ad65a88058b1b3cd47e5fac09bf255f376e38b6ab1953c0', 'prev': '000cc5baf584f2e60f2d15b13fda597bfe73cf8d01f6af6f2ccb7c16e38961ec', 'data': 262, 'hashalg': 'sha256'}, {'nonce': 158747, 'self': '00021ab3a179e72d866237dc0a1b06154bea14f364a28b52f27a71c9d50844c5', 'prev': '000b0465f128e7665ad65a88058b1b3cd47e5fac09bf255f376e38b6ab1953c0', 'data': 1652, 'hashalg': 'sha256'}, {'nonce': 169585, 'self': '0003f76fab1f9eb0da494187daaea480ca2913f7c7332977a4f0484bac55a812', 'prev': '00021ab3a179e72d866237dc0a1b06154bea14f364a28b52f27a71c9d50844c5', 'data': 7824, 'hashalg': 'sha256'}, {'nonce': 159119, 'self': '000af0317d944684e0609b12e83269d2f4e08ec6e62e4f8a45354b13b9b3ac02', 'prev': '0003f76fab1f9eb0da494187daaea480ca2913f7c7332977a4f0484bac55a812', 'data': 10127, 'hashalg': 'sha256'}]
flag = ""

for j in range(len(sortedlist)): 
    b = sortedlist[j] 
    sid = b['self'] 
    pre = b['prev'] 
    data = b['data'] 
    for i in range(256) : 
        h = hashlib.sha256()
        h.update(chr(i) + long_to_bytes(data) + pre.encode('utf-8'))  
        if h.hexdigest() == sid : 
            flag += chr(i) 
            print flag 
            break
```

The output revealed the flag as shown below:
```
f
fl
fla
flag
flag{
flag{1
flag{13
flag{133
flag{1337
flag{1337_
flag{1337_c
flag{1337_cr
flag{1337_cr3
flag{1337_cr33
flag{1337_cr33p
flag{1337_cr33p3
flag{1337_cr33p3r
flag{1337_cr33p3r_
flag{1337_cr33p3r_k
flag{1337_cr33p3r_kn
flag{1337_cr33p3r_kn0
flag{1337_cr33p3r_kn0w
flag{1337_cr33p3r_kn0ws
flag{1337_cr33p3r_kn0ws_
flag{1337_cr33p3r_kn0ws_4
flag{1337_cr33p3r_kn0ws_4b
flag{1337_cr33p3r_kn0ws_4b0
flag{1337_cr33p3r_kn0ws_4b0u
flag{1337_cr33p3r_kn0ws_4b0ut
flag{1337_cr33p3r_kn0ws_4b0ut_
flag{1337_cr33p3r_kn0ws_4b0ut_b
flag{1337_cr33p3r_kn0ws_4b0ut_b1
flag{1337_cr33p3r_kn0ws_4b0ut_b10
flag{1337_cr33p3r_kn0ws_4b0ut_b10c
flag{1337_cr33p3r_kn0ws_4b0ut_b10ck
flag{1337_cr33p3r_kn0ws_4b0ut_b10cks
flag{1337_cr33p3r_kn0ws_4b0ut_b10cks}
```
