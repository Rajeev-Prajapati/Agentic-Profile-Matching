from pathlib import Path
from random import Random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document

rng = Random(42)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'resumes'
OUT.mkdir(parents=True, exist_ok=True)

categories = [
 ('React Developer',25,['React','JavaScript','TypeScript','HTML','CSS','Redux','Jest','Next.js','Docker','AWS']),
 ('Python Django Developer',20,['Python','Django','Django REST Framework','PostgreSQL','Redis','Celery','Docker','AWS','pytest']),
 ('Java Spring Boot Developer',15,['Java','Spring Boot','Hibernate','SQL','Microservices','Docker','Kafka','JUnit']),
 ('Full Stack Developer',15,['React','JavaScript','Python','Django','REST API','PostgreSQL','Docker','Git']),
 ('ML Engineer',15,['Python','scikit-learn','Pandas','NumPy','PyTorch','ChromaDB','RAG','MLflow','SQL']),
 ('DevOps Engineer',10,['Linux','Docker','Kubernetes','AWS','Terraform','Jenkins','GitHub Actions','Python']),
]
first = ['Aarav','Diya','Kabir','Meera','Rohan','Ananya','Ishaan','Priya','Vivaan','Nisha','Arjun','Kavya','Aditya','Sara','Neel','Riya','Dev','Tara','Ayaan','Ira']
last = ['Sharma','Patel','Verma','Gupta','Mehta','Rao','Singh','Nair','Iyer','Kapoor','Joshi','Das']
styles = getSampleStyleSheet()

def make_text(i, role, pool):
    name = f'{first[(i-1)%len(first)]} {last[((i-1)//len(first))%len(last)]}'
    years = rng.choice([1,2,3,4,5,6,7,8,9])
    count = rng.randint(3,min(8,len(pool)))
    skills = rng.sample(pool,count)
    # Mix in some deliberate missing skills so ranking is meaningful.
    project = f'Built a {role.lower()} solution using {", ".join(skills[:3])}; implemented testing, deployment and performance improvements.'
    return '\n'.join([
        f'Candidate ID: candidate_{i:03d}', f'Name: {name}', f'Target Role: {role}',
        f'Professional Experience: {years} years', f'Skills: {", ".join(skills)}',
        f'Education: B.Tech in Computer Science (synthetic)',
        f'Work Experience: Software Engineer, Example Technology Solutions; {years} years in {role.lower()} responsibilities.',
        f'Project: {project}',
        'Note: This is a synthetic resume for testing. All identities and employment details are fictional.'
    ])

def write_pdf(path,text):
    story=[]
    for line in text.splitlines():
        story.append(Paragraph(line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'),styles['Normal']))
        story.append(Spacer(1,8))
    SimpleDocTemplate(str(path)).build(story)

def write_docx(path,text):
    doc=Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(path)

n=0
for role,count,pool in categories:
    for _ in range(count):
        n+=1
        text=make_text(n,role,pool)
        extension = '.pdf' if n<=50 else '.docx' if n<=80 else '.txt'
        path=OUT/f'candidate_{n:03d}{extension}'
        if extension=='.pdf': write_pdf(path,text)
        elif extension=='.docx': write_docx(path,text)
        else: path.write_text(text,encoding='utf-8')
        print(f'Created: {path.name}')
print(f'Generated {n} synthetic resumes in {OUT}')
