```python { "name": "update flags.yaml - set cartFailure flag to on"}
import yaml
import json

# Load the YAML file
with open(f"/workspaces/{REPOSITORY_NAME}/flags.yaml", "r") as file:
    config = yaml.safe_load(file)

flags_json = json.loads(config['data']['demo.flagd.json'])

flags_json['flags']['cartFailure']['defaultVariant'] = "on"

# Change the defaultVariant of cartFailure from 'off' to 'on'
config['data']['demo.flagd.json'] = json.dumps(flags_json, indent=2)

#config['data']['demo.flagd.json']['flags']['cartFailure']['defaultVariant'] = 'on'

# Save the updated configuration to a new YAML file
with open(f"/workspaces/{REPOSITORY_NAME}/new_flags.yaml", 'w') as file:
    yaml.dump(config, file)
```