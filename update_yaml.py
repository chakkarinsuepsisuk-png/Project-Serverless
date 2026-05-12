import yaml

with open('monitoring-stack.yaml', 'r', encoding='utf-8') as f:
    docs = list(yaml.safe_load_all(f))

# Read the generated dashboard JSON
with open('dashboard.json', 'r', encoding='utf-8') as f:
    dashboard_json = f.read()

for doc in docs:
    if doc and doc.get('kind') == 'ConfigMap' and doc['metadata']['name'] == 'grafana-datasource-config':
        # Replace datasource config to include MySQL
        ds_content = """apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus-service.monitoring.svc.cluster.local:9090
    isDefault: false
    editable: true
  - name: MySQL
    type: mysql
    url: 34.158.49.62:3306
    database: it_repair
    user: root
    secureJsonData:
      password: "SuperSecretPassword123!"
    isDefault: true
    editable: true
"""
        doc['data']['datasource.yml'] = ds_content

    if doc and doc.get('kind') == 'ConfigMap' and doc['metadata']['name'] == 'grafana-dashboard-json':
        # Replace dashboard JSON
        doc['data']['it-repair-dashboard.json'] = dashboard_json

with open('monitoring-stack.yaml', 'w', encoding='utf-8') as f:
    yaml.dump_all(docs, f, default_flow_style=False)
