from sqlalchemy.orm import Session
from jinja2 import Template
from app.db.models import Project

template = """
### 📝 Weekly Project Report

#### 📁 Project: {{ project.name }}
- Status: {{ project.status }}
- Manager: {{ project.manager }}
- Duration: {{ project.start_date }} → {{ project.end_date }}

**Phases:**
{% for phase in project.phases %}
{{ loop.index }}. {{ phase.name }} - {{ phase.status }}
{% endfor %}

**Tasks Summary:**
{% for phase in project.phases %}
{% for task in phase.tasks %}
- {{ task.name }} → {{ task.status }} (₹{{ task.estimated_budget }} est., ₹{{ task.actual_budget }} spent)
{% endfor %}
{% endfor %}
"""

def generate_report(db: Session):
    project = db.query(Project).first()
    rendered = Template(template).render(project=project)
    return {"report": rendered}
