import urllib.request
import json
import re
import urllib.request
import hashlib


def GetDynamicid():
    s = input("---请粘贴Bilibili动态的网址：---\n（形如 https://t.bilibili.com/xxxxxxx）\n")
    nums = re.findall(r'\d+', s)

    return nums[0]


def GetMiddleStr(content, startStr, endStr):
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]


def GetTotalRepost(Dynamic_id):
    global UP_UID
    DynamicAPI = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + Dynamic_id
    BiliJson = json.loads(urllib.request.urlopen(DynamicAPI).read())
    Total_count = BiliJson['data']['card']['desc']['repost']
    UP_UID = BiliJson['data']['card']['desc']['user_profile']['info']['uid']

    return Total_count


def GetUsers(Dynamic_id):
    total = GetTotalRepost(Dynamic_id)
    DynamicAPI = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id=" + Dynamic_id + "&offset="
    index = 0
    users = []
    while index < total:
        Tmp_DynamicAPI = DynamicAPI + str(index)
        try:
            BiliJson = json.loads(
                GetMiddleStr(urllib.request.urlopen(Tmp_DynamicAPI).read(), b"comments\":", b",\"total"))
            for BiliJson_dict in BiliJson:
                Bilibili_UID = str(BiliJson_dict['uid'])
                Bilibili_Uname = BiliJson_dict['uname']
                Bilibili_Comment = BiliJson_dict['comment']
                Bilibili_Hash = hashlib.sha256(Bilibili_UID.encode("utf-8")).hexdigest()

                user = {"uid": Bilibili_UID, "name": Bilibili_Uname, "hash": Bilibili_Hash, "comment": Bilibili_Comment}
                users.append(user)
        except:
            break

        index += 20

    users = sorted(users, key=lambda i: int(i['hash'], 16))

    return users


def binarySearch(arr, l, r, x):
    if r >= l:
        mid = int(l + (r - l) / 2)
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return l
