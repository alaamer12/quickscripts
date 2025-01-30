with open("keys", 'r') as f:
    keys = f.read().splitlines()

with open("values", 'r') as f:
    values = f.read().splitlines()

# make a dict of keys and values
key_value_dict = dict(zip(keys, values))
import pprint
pprint.pprint(key_value_dict)