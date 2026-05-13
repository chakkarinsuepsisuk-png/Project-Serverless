import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics  # <--- 1. เพิ่มบรรทัดนี้

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # <--- 2. เพิ่มบรรทัดนี้ (เปิดใช้งาน /metrics อัตโนมัติ)


# แก้ Docker เอ๋อ









# ... โค้ดส่วนที่เหลือของเดิมปล่อยไว้เหมือนเดิมได้เลย ...
# ดึงการตั้งค่าฐานข้อมูลจาก Environment Variable (ถ้าไม่มีจะใช้ค่า Default)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "it_repair")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ออกแบบตารางเก็บข้อมูล
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device = db.Column(db.String(100), nullable=False)
    issue = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')

# สร้างตารางอัตโนมัติ
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"DB Init Error: {e}")

@app.route('/', methods=['GET'])
def index():
    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return render_template('index.html', tickets=tickets)

@app.route('/ticket', methods=['POST'])
def add_ticket():
    name = request.form.get('name')
    device = request.form.get('device')
    issue = request.form.get('issue')
    
    if name and device and issue:
        new_ticket = Ticket(name=name, device=device, issue=issue)
        db.session.add(new_ticket)
        db.session.commit()
        
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    ticket = Ticket.query.get(id)
    if ticket:
        ticket.status = request.form.get('status', 'Pending')
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)