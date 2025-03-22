import json

try:
    with open('cfg.json', 'r') as f:
        cfg = json.load(f)
except:
    with open('cfg.json', 'w') as f:
        default_config = {
            "key":"",
            "allow-read":True,
            "allow-write":False,
            "port":8192
        }
        json.dump(default_config, f, indent=4)
    print("Please configure cfg.json.")
    quit()