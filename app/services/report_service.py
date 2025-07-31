from sqlalchemy.orm import Session
from jinja2 import Template
from app.db.models import Project

# 📧 Gmail Format
gmail_template = """
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

# 📧 Outlook Format (slightly different markdown)
outlook_template = """
Subject: Weekly Project Report – {{ project.name }}

Dear {{ project.manager }},

Here is your weekly project update:

Project Status: {{ project.status }}
Duration: {{ project.start_date }} → {{ project.end_date }}

Phases:
{% for phase in project.phases %}
- {{ phase.name }} → {{ phase.status }}
{% endfor %}

Tasks:
{% for phase in project.phases %}
{% for task in phase.tasks %}
- {{ task.name }} ({{ task.status }}) – ₹{{ task.actual_budget }}/₹{{ task.estimated_budget }}
{% endfor %}
{% endfor %}

Best regards,
Your AI Assistant
"""

# 📲 WhatsApp Format
whatsapp_template = """
Mall Construction – Weekly Summary 📊

👨‍💼 Manager: {{ project.manager }}
📅 Status: {{ project.status }}

Phases:
{% for phase in project.phases %}
✓ {{ phase.name }} – {{ phase.status }}
{% endfor %}

Tasks:
{% for phase in project.phases %}
{% for task in phase.tasks %}
- {{ task.name }} → {{ task.status }} (₹{{ task.actual_budget }})
{% endfor %}
{% endfor %}
"""

def generate_report(db: Session, channel: str):
    project = db.query(Project).first()

    if channel == "gmail":
        template = Template(gmail_template)
    elif channel == "outlook":
        template = Template(outlook_template)
    elif channel == "whatsapp":
        template = Template(whatsapp_template)
    else:
        raise ValueError("Unsupported channel")

    rendered = template.render(project=project)
    return {
        "channel": channel,
        "report": rendered
    }
