import json

dashboard = {
  "annotations": {"list": []},
  "editable": True,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": None,
  "links": [],
  "liveNow": False,
  "panels": [
    {
      "datasource": {"type": "mysql", "uid": "MySQL"},
      "gridPos": {"h": 8, "w": 8, "x": 0, "y": 0},
      "id": 1,
      "options": {
        "orientation": "horizontal",
        "showValue": "auto",
        "legend": {"displayMode": "list", "placement": "bottom", "showLegend": False}
      },
      "targets": [
        {
          "format": "table",
          "group": [],
          "metricColumn": "none",
          "rawQuery": True,
          "rawSql": "SELECT name as 'Name', count(*) as 'Total' FROM tickets GROUP BY name ORDER BY Total DESC LIMIT 5",
          "refId": "A",
          "select": [[{"params": ["value"], "type": "column"}]],
          "timeColumn": "time",
          "where": [{"name": "$__timeFilter", "params": [], "type": "macro"}]
        }
      ],
      "title": "🥇 Top Users (ผู้แจ้งซ่อมบ่อยที่สุด)",
      "type": "barchart",
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {"fillOpacity": 80, "lineWidth": 1}
        },
        "overrides": []
      }
    },
    {
      "datasource": {"type": "mysql", "uid": "MySQL"},
      "gridPos": {"h": 8, "w": 8, "x": 8, "y": 0},
      "id": 2,
      "options": {
        "pieType": "donut",
        "legend": {"displayMode": "list", "placement": "bottom", "showLegend": True}
      },
      "targets": [
        {
          "format": "table",
          "rawQuery": True,
          "rawSql": "SELECT device as 'Device', count(*) as 'Total' FROM tickets GROUP BY device",
          "refId": "A"
        }
      ],
      "title": "💻 Device Types (สัดส่วนอุปกรณ์ที่ส่งซ่อม)",
      "type": "piechart",
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {"hideFrom": {"legend": False, "tooltip": False, "viz": False}}
        },
        "overrides": []
      }
    },
    {
      "datasource": {"type": "mysql", "uid": "MySQL"},
      "gridPos": {"h": 8, "w": 16, "x": 0, "y": 8},
      "id": 3,
      "options": {
        "showHeader": True,
        "sortBy": [{"desc": True, "displayName": "ID"}]
      },
      "targets": [
        {
          "format": "table",
          "rawQuery": True,
          "rawSql": "SELECT id as 'ID', name as 'User', device as 'Device', issue as 'Issue' FROM tickets ORDER BY id DESC LIMIT 5",
          "refId": "A"
        }
      ],
      "title": "🆕 Recent Tickets (รายการแจ้งซ่อมล่าสุด)",
      "type": "table",
      "fieldConfig": {"defaults": {"custom": {"align": "auto", "displayMode": "auto"}}, "overrides": []}
    },
    {
      "datasource": {"type": "mysql", "uid": "MySQL"},
      "gridPos": {"h": 8, "w": 8, "x": 16, "y": 0},
      "id": 4,
      "options": {
        "colorMode": "value",
        "graphMode": "none",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
        "textMode": "auto"
      },
      "targets": [
        {
          "format": "table",
          "rawQuery": True,
          "rawSql": "SELECT count(*) as 'Total Tickets' FROM tickets",
          "refId": "A"
        }
      ],
      "title": "📈 Total Tickets (ยอดรวมแจ้งซ่อม)",
      "type": "stat",
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "thresholds"},
          "thresholds": {"mode": "absolute", "steps": [{"color": "blue", "value": None}]}
        },
        "overrides": []
      }
    }
  ],
  "schemaVersion": 38,
  "style": "dark",
  "tags": ["business", "tickets"],
  "templating": {"list": []},
  "time": {"from": "now-6h", "to": "now"},
  "timepicker": {},
  "timezone": "",
  "title": "IT Repair Business Dashboard",
  "uid": "it-repair-biz",
  "version": 1
}

with open("dashboard.json", "w", encoding="utf-8") as f:
    json.dump(dashboard, f, indent=2, ensure_ascii=False)
