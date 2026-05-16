# 🚀 ระบบ API แจ้งซ่อมอุปกรณ์ไอทีเบื้องต้น — ENG23 3074

> ระบบ API แจ้งซ่อมอุปกรณ์ไอทีเบื้องต้น สร้างด้วย Python Flask containerize ด้วย Docker และ deploy บน Kubernetes ผ่าน Jenkins pipeline แบบอัตโนมัติ พร้อมระบบ Monitoring ด้วย Prometheus และ Grafana

---

## 👥 สมาชิกในกลุ่ม

| รหัสนักศึกษา | ชื่อ-นามสกุล | ความรับผิดชอบ |
|-------------|-------------|---------------|
| B6613389 | นายจักริน สืบสีสุก | Python Flask API, Database Design, Frontend |
| B6607838 | นายเสกสรร นามนุ | Git, Docker, Jenkins Pipeline (CI/CD) |
| B6643577 | นายพีรพงศ์ ลิมปศรีตระกูล | Kubernetes, Google Cloud Platform (GCP), Infrastructure |

---

## 📌 ภาพรวมโปรเจค

### แอปพลิเคชัน
- **ชื่อ:** IT Repair Ticketing System (ระบบแจ้งซ่อมอุปกรณ์ไอทีเบื้องต้น)
- **ประเภท:** REST API และ Web Application
- **ภาษา / Framework:** Python (Flask) สำหรับฝั่ง Backend และ HTML/CSS/JavaScript สำหรับหน้า Web Frontend
- **คำอธิบาย:** ระบบ API และเว็บแอปพลิเคชันสำหรับรับแจ้งปัญหาและติดตามสถานะการซ่อมอุปกรณ์ไอทีเบื้องต้น โปรเจกต์นี้ช่วยแก้ปัญหาข้อมูลแจ้งซ่อมตกหล่นและเพิ่มความสะดวกให้ผู้ใช้งานสามารถตรวจสอบสถานะได้ด้วยตนเอง นอกจากนี้ระบบยังทำงานบนสถาปัตยกรรมคอนเทนเนอร์ที่มีการ Deploy อัตโนมัติ ทำให้มีความเสถียรและดูแลรักษาง่าย

### Architecture Diagram
````
Developer (Team)
        │
        ▼  git push
     GitHub ──── webhook ────▶ Jenkins CI/CD
                                     │
         ┌───────────────────────────┼──────────────────────────┐
         ▼                           ▼                          ▼
     Checkout               Test Application            Build Docker Image
                                                               │
                                                               ▼
                                                       Push to Docker Hub
                                                       (yaichakkarin/it-repair-api)
                                                               │
                               ┌───────────────────────────────┤
                               ▼                               ▼
                           Terraform                        Ansible
                     (Provision Cloud SQL              (Verify Dependencies
                       MySQL บน GCP)                    & Environment)
                               │                               │
                               └───────────────┬───────────────┘
                                               ▼
                                   GKE Cluster (Google Kubernetes Engine)
                              ┌────────────────────────────────────┐
                              │  Namespace: default                │
                              │  ┌──────────┐  ┌──────────┐       │
                              │  │  Pod 1   │  │  Pod 2   │       │
                              │  │[Flask API]│  │[Flask API]│      │
                              │  └──────────┘  └──────────┘       │
                              │  Service: it-repair-api-svc        │
                              │  (LoadBalancer → 34.21.183.215:80) │
                              │                                    │
                              │  Namespace: monitoring             │
                              │  ┌──────────┐  ┌──────────┐       │
                              │  │Prometheus│  │ Grafana  │       │
                              │  │  :9090   │  │  :3000   │       │
                              │  └──────────┘  └──────────┘       │
                              └────────────────┬───────────────────┘
                                               │ (Database Connection)
                                               ▼
                                  Google Cloud Platform (GCP)
                                    [ Cloud SQL (MySQL 8.0) ]
                                    Project: it-repair-b6643577
                                    Region: asia-southeast1
````
---

## 📁 โครงสร้าง Repository
````
Project-Serverless/
├── app/
│   ├── app.py                  # โค้ดหลักของ API (Python Flask) จัดการข้อมูลแจ้งซ่อม + /metrics endpoint
│   ├── requirements.txt        # ไลบรารีที่ต้องใช้ (flask, pymysql, sqlalchemy, prometheus-flask-exporter)
│   ├── Dockerfile              # คำสั่งสร้าง Docker image สำหรับแพ็กแอปพลิเคชัน
│   └── templates/
│       └── index.html          # หน้าเว็บฟอร์มแจ้งซ่อมและตารางแสดงสถานะ
│
├── k8s/
│   ├── deployment.yaml         # กำหนดการสร้าง Pods (2 replicas) ของแอปพลิเคชัน Flask
│   └── service.yaml            # เปิด Service แบบ LoadBalancer ให้เข้าถึงแอปจากภายนอก
│
├── terraform/
│   └── main.tf                 # Provision Cloud SQL (MySQL 8.0) บน GCP (project: it-repair-b6643577)
│
├── ansible/
│   ├── inventory               # กำหนด hosts สำหรับ Ansible (localhost)
│   └── playbook.yml            # Verify ความพร้อมของ Docker, kubectl และ Monitoring stack
│
├── monitoring/
│   ├── prometheus.yml          # Config Prometheus (scrape จาก it-repair-api-svc.default.svc.cluster.local:80)
│   └── grafana-dashboard.json  # Dashboard JSON สำหรับ import เข้า Grafana
│
├── monitoring-stack.yaml       # Kubernetes manifest รวม Prometheus + Grafana (namespace: monitoring)
├── Jenkinsfile                 # กำหนด CI/CD pipeline ครบ 6 stages
└── README.md                   # อธิบายภาพรวมโปรเจกต์ การตั้งค่า และรายชื่อสมาชิกกลุ่ม
````
---

## ⚙️ สิ่งที่ต้องติดตั้งก่อน (Prerequisites)

ตรวจสอบให้แน่ใจว่าติดตั้งทุก tool ครบก่อนรันโปรเจค

| Tool | Version | หน้าที่ |
|------|---------|---------| 
| Git | ≥ 2.x | จัดการ source code และทำงานร่วมกันผ่าน GitHub |
| Python | ≥ 3.9 | พัฒนาและทดสอบระบบหลังบ้าน (Flask API) |
| Docker | ≥ 24.x | สร้างและรัน container สำหรับแอปพลิเคชัน |
| Jenkins | ≥ 2.4xx | ระบบ CI/CD automation ควบคุมการ Build & Deploy |
| Terraform | ≥ 1.x | Provision infrastructure จัดการทรัพยากรบน GCP |
| Ansible | ≥ 2.15 | Verify environment และตรวจสอบความพร้อมก่อน Deploy |
| kubectl | ≥ 1.28 | สั่งงานและจัดการ Kubernetes cluster |
| GKE (Google Kubernetes Engine) | latest | Managed Kubernetes cluster บน Google Cloud Platform |
| gcloud CLI | latest | จัดการ resource และฐานข้อมูล (Cloud SQL) บน Google Cloud |
| Prometheus | ≥ 2.x | เก็บ metrics สถานะการทำงานของระบบและ API |
| Grafana | ≥ 10.x | แสดง dashboard ตรวจสอบข้อมูล Ticket และสถานะระบบ |

---

## 🏃 วิธีรันโปรเจค (Quick Start)

### 1. Clone Repository
```bash
git clone https://github.com/chakkarinsuepsisuk-png/Project-Serverless.git
cd PROJECT-SERVERLESS
```

### 2. Build & Push Docker Image
```bash
cd app
docker build -t yaichakkarin/it-repair-api:latest .
docker push yaichakkarin/it-repair-api:latest
cd ..
```

### 3. Deploy ลง GKE Cluster
เชื่อมต่อ GKE cluster แล้ว Apply ไฟล์ Manifest เพื่อสร้าง Pods และ Service
```bash
gcloud container clusters get-credentials my-cluster --region asia-southeast1 --project it-repair-b6643577
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 4. Deploy Monitoring Stack (Prometheus + Grafana)
```bash
kubectl apply -f monitoring-stack.yaml
```

### 5. เข้าถึงหน้า Dashboard และ Monitoring
| บริการ | URL | Login |
|--------|-----|-------|
| IT Repair Web App | http://34.21.183.215:80 | - |
| Grafana Dashboard | http://136.110.45.119:3000 | admin / admin |

---

## 🔄 CI/CD Pipeline (Jenkins)

### ลำดับการทำงานของ Pipeline (6 Stages)

```
Checkout SCM ──▶ Checkout ──▶ Test Application ──▶ Build Docker Image ──▶ Push to Docker Hub ──▶ Debug ──▶ Deploy Infrastructure (IaC) ──▶ Deploy to Kubernetes ──▶ Deploy Monitoring Stack ──▶ Post Actions
```

| Stage | คำอธิบาย |
|-------|----------|
| **Checkout SCM** | Jenkins ดึงโค้ดจาก GitHub ผ่าน SCM configuration |
| **Checkout** | ดึงโค้ดล่าสุดของโปรเจกต์จาก GitHub Repository |
| **Test Application** | ทดสอบ syntax โค้ด Python ด้วย `py_compile` เพื่อตรวจสอบ Syntax Error เบื้องต้น |
| **Build Docker Image** | Build Source Code (Flask) ให้เป็น Docker Image ตามคำสั่งใน Dockerfile |
| **Push to Docker Hub** | อัปโหลด Docker Image ขึ้น Docker Hub (`yaichakkarin/it-repair-api:latest`) |
| **Debug** | ตรวจสอบ environment และ configuration ก่อน Deploy |
| **Deploy Infrastructure (IaC)** | รัน `terraform apply` เพื่อ Provision Cloud SQL บน GCP และรัน Ansible playbook เพื่อ Verify environment |
| **Deploy to Kubernetes** | Apply Manifest ไฟล์ทั้งหมดและ restart deployment บน GKE เพื่อดึง image ใหม่ |
| **Deploy Monitoring Stack** | Apply `monitoring-stack.yaml` และ restart Prometheus + Grafana บน namespace `monitoring` |
| **Post Actions** | แจ้งผลลัพธ์การรัน Pipeline (Pipeline completed successfully!) |

### วิธีตั้งค่า Jenkins
1. ติดตั้ง Jenkins และเปิดที่ http://localhost:8081
2. ติดตั้ง plugin: **Git**, **Pipeline**, **Docker Pipeline**
3. เพิ่ม credentials สำหรับ Docker Hub (ชื่อ `dockerhub-credentials`)
4. สร้าง Pipeline job ชื่อ `it-repair-api` และชี้ไปที่ repository PROJECT-SERVERLESS
5. ตั้งค่า Webhook ใน GitHub:
   - ไปที่ **Settings → Webhooks → Add webhook**
   - Payload URL: `http://[jenkins-host]:8081/github-webhook/`
   - Content type: `application/json`
   - ติ๊ก trigger: **Just the push event**

---

## 🏗️ Infrastructure as Code

### Terraform — Provision Cloud SQL บน GCP
```bash
cd terraform
terraform init      # ดาวน์โหลด provider plugins
terraform plan      # ตรวจสอบว่าจะสร้างอะไรบ้าง
terraform apply     # สร้าง resource จริง
```
> **สิ่งที่ Terraform สร้าง:** Cloud SQL instance ชื่อ `it-repair-db-fast` (MySQL 7.0, tier: db-f1-micro) บน GCP project `it-repair-b6643577` region `asia-southeast1` พร้อมสร้าง database ชื่อ `it_repair` และ user `root`

### Ansible — Verify Environment
```bash
cd ansible
ansible-playbook -i inventory playbook.yml
```
> **สิ่งที่ Ansible ทำ:** ตรวจสอบความพร้อมของ environment ก่อน Deploy ได้แก่ ยืนยันว่า Docker, kubectl และ Monitoring stack พร้อมทำงาน รวมถึงสร้าง config directory ที่จำเป็น

⚠️ **หมายเหตุ:** Ansible ใช้ `catchError` ใน Pipeline เพื่อไม่ให้ Pipeline ล้มเหลวหากรันในสภาพแวดล้อมที่ไม่มี Node จริง

---

## ☸️ Kubernetes Deployment

### Apply Manifests ด้วยตัวเอง
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### ตรวจสอบสถานะ
```bash
kubectl get pods -n default
kubectl get svc  -n default
```

### ผลลัพธ์ที่ควรจะได้
```
NAME                                    READY   STATUS    RESTARTS   AGE
it-repair-api-7f69c9966b-jdhkj          1/1     Running   0          2m
it-repair-api-7f69c9966b-h4hfx          1/1     Running   0          2m

NAME                TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)        AGE
it-repair-api-svc   LoadBalancer   10.x.x.x       34.21.183.215    80:xxxxx/TCP   2m
```

### เข้าถึงแอปพลิเคชัน
แอปพลิเคชันเข้าถึงได้ผ่าน External IP ของ LoadBalancer:

- **IT Repair Web App:** http://34.21.183.215:80

---

## 📊 Monitoring

### ภาพรวม
Prometheus และ Grafana ถูก deploy บน Kubernetes ใน namespace `monitoring` ผ่านไฟล์ `monitoring-stack.yaml` โดยอัตโนมัติใน Pipeline

```bash
# Deploy monitoring stack
kubectl apply -f monitoring-stack.yaml

# ตรวจสอบสถานะ
kubectl get pods -n monitoring
kubectl get svc  -n monitoring
```

### Prometheus — เก็บ Metrics
- **Config file:** `monitoring/prometheus.yml`
- **Scrape interval:** 15 วินาที
- **Target endpoint:** `it-repair-api-svc.default.svc.cluster.local:80` (ภายใน Cluster)
- **UI:** http://localhost:9090 (ต้องทำ port-forward ก่อน)

```bash
kubectl port-forward svc/prometheus-service -n monitoring 9090:9090
```

### Grafana — แสดง Dashboard
- **Image:** `grafana/grafana:latest`
- **Data sources:** Prometheus + MySQL (Cloud SQL)
- **URL:** http://136.110.45.119:3000
- **Login:** admin / admin

Dashboard ถูก provision อัตโนมัติผ่าน ConfigMap (`monitoring-stack.yaml`) ไม่ต้อง import เพิ่มเติม

### Panels ใน Grafana Dashboard (IT Repair Business Dashboard)

| Panel | Data Source | SQL / Metric | แสดงข้อมูลอะไร |
|-------|-------------|--------------|----------------|
| 🏆 Top Users | MySQL | `SELECT name, count(*) FROM tickets GROUP BY name` | ผู้แจ้งซ่อมบ่อยที่สุด 5 อันดับ (Bar Chart) |
| 💻 Device Types | MySQL | `SELECT device, count(*) FROM tickets GROUP BY device` | สัดส่วนอุปกรณ์ที่ส่งซ่อม (Pie Chart) |
| 🆕 Recent Tickets | MySQL | `SELECT id, name, device, issue FROM tickets ORDER BY id DESC LIMIT 5` | รายการแจ้งซ่อมล่าสุด (Table) |
| 📈 Total Tickets | MySQL | `SELECT count(*) FROM tickets` | ยอดรวมแจ้งซ่อมทั้งหมด (Stat) |

---

## 🌿 Branching Strategy

```text
main        ──── โค้ดที่พร้อม production, trigger CI/CD pipeline อัตโนมัติ
big         ──── พัฒนาและรวมโค้ดก่อน merge ขึ้น main
```

| Branch | Protected | คำอธิบาย |
|--------|-----------|----------|
| `main` | ✅ | trigger pipeline CI/CD อัตโนมัติเมื่อมีการ push/merge |
| `big` | ❌ | ใช้พัฒนาและรวมโค้ดก่อน merge ขึ้น main |

---

## 🧪 API Endpoints

| Method | Endpoint | คำอธิบาย |
|--------|----------|----------|
| `GET` | `/` | แสดงหน้าเว็บ (index.html) พร้อมรายการ Ticket ทั้งหมด |
| `GET` | `/metrics` | Prometheus metrics endpoint (จาก `prometheus-flask-exporter`) |
| `POST` | `/ticket` | สร้าง Ticket แจ้งซ่อมใหม่ (รับ `name`, `device`, `issue`) |
| `POST` | `/update_status/<id>` | อัปเดตสถานะ Ticket ตาม ID (รับ `status`) |

---

## 🐛 ปัญหาที่พบบ่อย (Troubleshooting)

**Pods ค้างอยู่ที่ `Pending` หรือ `CrashLoopBackOff`**
```bash
# ดู log และ events ของ pod ระบบแจ้งซ่อม
kubectl describe pod -l app=it-repair-api -n default
# ดูที่ส่วน Events ด้านล่างสุด: อาจเกิดจาก Image ไม่มีใน local, Resource ไม่พอ หรือแอปเชื่อมต่อ Database ไม่ได้
kubectl logs -l app=it-repair-api -n default
```

**Jenkins pipeline ล้มเหลวตอน Docker Build**
```bash
# ตรวจว่า Docker daemon รันอยู่
sudo systemctl status docker
# เพิ่ม jenkins user เข้า docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

**Prometheus แสดง target เป็น DOWN**
```bash
# ตรวจว่า Flask app เปิด /metrics endpoint ได้จริงใน Cluster
kubectl exec -it <pod-name> -n default -- curl http://localhost:80/metrics
# ตรวจสอบ prometheus config ใน monitoring-stack.yaml ว่า target ชี้ไปที่ service ถูกต้อง
# Target ที่ถูกต้อง: it-repair-api-svc.default.svc.cluster.local:80
```

**Grafana ไม่แสดงข้อมูล (No Data)**
```bash
# ตรวจสอบ pod ใน namespace monitoring
kubectl get pods -n monitoring
# ตรวจสอบ datasource MySQL ว่า IP ตรงกับ Cloud SQL จริงๆ
# ดู IP ปัจจุบันจาก terraform output
cd terraform && terraform output db_public_ip
```

**Image ไม่พบใน GKE cluster**
```bash
# ตรวจสอบว่า image ถูก push ขึ้น Docker Hub แล้ว
docker pull yaichakkarin/it-repair-api:latest
# restart deployment เพื่อดึง image ใหม่
kubectl rollout restart deployment it-repair-api -n default
```

---

## 📚 เอกสารอ้างอิง
- [Python Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.readthedocs.io/)
- [prometheus-flask-exporter](https://github.com/rycus86/prometheus_flask_exporter)
- [Google Cloud Platform (GCP) Documentation](https://cloud.google.com/docs)
- [Jenkinsfile Declarative Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Ansible Documentation](https://docs.ansible.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kind (Kubernetes in Docker)](https://kind.sigs.k8s.io/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Markdown Syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
