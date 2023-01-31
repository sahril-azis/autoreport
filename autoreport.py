import json
import requests
data = {
    "servername"  : " server test",
    "ip_raspi"  : "10.251.2.110",
    "command" : ["free -h"]
}
import subprocess
for i in data["command"]:
    proc = subprocess.Popen([i], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    # print(type(out.decode("utf-8")))
    output1 = out.decode("utf-8")
    print(output1)
    mem =output1.strip().split(" ")
    while("" in mem):
        mem.remove("")
    while("\n" in mem):
        mem.remove("\n")
    print("mem_total", mem)

    num = 0
    for m in mem :
        if num == 11:
            print('m ', m)
        if "\nSwap:" in m:
            print('swap ', m)
            m = m.replace("\nSwap:" , "")
        if 'M' in m:
            print('m ', m)
            try:
                m = m.replace("M", "")
                m_byte = float(m)
                print(m_byte)
            except:
                m_byte = m
        elif 'G' in m:
            # print('g ', m)
            try:
                m = m.replace("G", "")
                m_byte = float(m) * 1024
                print(m_byte)
            except:
                m_byte = m
        elif 'B' in m:
            # print('b ', m)
            try:
                m_byte = m.replace("B","")
                m_byte = float(m_byte) / (1024 **2)
            except:
                m_byte = m
        else:
            m_byte = m
        # print("mem_num ", m_byte)
        mem[num] = m_byte
        num = num + 1
        
    mem_total = str(mem[6])
    mem_used = str(mem[7])
    mem_buff_cache = str(mem[10])
    mem_shared = str(mem[9])
    mem_free = str(mem[8])
    mem_available = str(mem[11])
    mem_swap = str(mem[12])
    mem_used_2 = str(mem[13])
    mem_free_2 = str(mem[14])

    print(mem)


    message = "\n Total mem: " + mem_total + "\n used: " + mem_used + "\n buff cache: " + mem_buff_cache + "\n free: " + mem_free + "\n available: " + mem_available + "\n \n \n Total Swap: " + mem_swap + "\n used: " + mem_used_2 + "\n Free: " + mem_free_2
    print('message ', message)

    payload = json.dumps({
        
        "ip_raspi" : data["ip_raspi"],
        "total_memory" : int(float(mem_total)),
        "used_memory" : int(float(mem_used)),
        "free_memory" : int(float(mem_free)),
        "shared_memory" : int(float(mem_shared)),
        "buff_cache_memory" : int(float(mem_buff_cache)),
        "available_memory" : int(float(mem_available)),
        "total_swap" : int(float(mem_swap)),
        "used_swap" : int(float(mem_used_2)),
        "free_swap" : int(float(mem_free_2))
        # "data" : message
    })

    url = "http://agum.digitalresume.id/api/set-memory-raspi"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print("response ", response.text)