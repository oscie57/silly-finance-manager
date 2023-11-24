import json

def get_json():
    with open('data.json', 'r', encoding='UTF-8') as f:
        return json.load(f)
    
def write_json(data):
    with open('data.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4)

def check_ip(request):
    """Check if the request is coming from a whitelisted IP."""

    with open('whitelist.txt', 'r', encoding='UTF-8') as f:
        whitelist = f.read().splitlines()

    for ip in whitelist:
        if request.remote_addr == ip:
            return True
    if request.remote_addr == "127.0.0.1":
        return True
    else:
        return False