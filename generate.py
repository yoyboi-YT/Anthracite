import random
import string
import json

try:
    with open('cfg.json', 'r') as f:
        cfg = json.load(f)
        if cfg.get("key") != "":
            print("There's already a key in the config.")
            quit()
        else:
            length = input("Length (default 64): ")
            try:
                length = int(length)
            except:
                length = 64
            allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace('"', '').replace('\\', '')
            new_key = ''.join(random.choice(allowed_chars) for _ in range(length))
            cfg["key"] = new_key
            with open('cfg.json', 'w') as f:
                json.dump(cfg, f, indent=4)
except FileNotFoundError:
    print("There's no config. Run main.py to make it.")