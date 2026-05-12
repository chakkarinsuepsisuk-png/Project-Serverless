import json
import yaml

# 1. Load the existing dashboard.json
with open('dashboard.json', 'r', encoding='utf-8') as f:
    dashboard = json.load(f)

# 2. Modify Panel 2
for panel in dashboard['panels']:
    if panel['id'] == 2:
        panel['targets'][0]['rawSql'] = "SELECT device as 'metric', count(*) as 'value' FROM tickets GROUP BY device"
        panel['options'] = {
            "pieType": "donut",
            "reduceOptions": {
                "values": True,
                "calcs": [],
                "fields": ""
            },
            "displayLabels": ["percent", "name"],
            "legend": {
                "displayMode": "table",
                "placement": "right",
                "showLegend": True,
                "values": ["value", "percent"]
            }
        }

# 3. Save it back
with open('dashboard.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard, f, indent=2, ensure_ascii=False)

# 4. Update monitoring-stack.yaml
with open('monitoring-stack.yaml', 'r', encoding='utf-8') as f:
    docs = list(yaml.safe_load_all(f))

dashboard_json_str = json.dumps(dashboard, indent=2, ensure_ascii=False)

for doc in docs:
    if doc and doc.get('kind') == 'ConfigMap' and doc['metadata']['name'] == 'grafana-dashboard-json':
        doc['data']['it-repair-dashboard.json'] = dashboard_json_str

with open('monitoring-stack.yaml', 'w', encoding='utf-8') as f:
    yaml.dump_all(docs, f, default_flow_style=False)
