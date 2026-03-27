from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .predict import predict_role
from .recommd import recommend_skills

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        skills = request.POST.get("skills")

        role = predict_role(skills)
        missing = recommend_skills(skills, role)

        request.session['name'] = name
        request.session['role'] = role
        request.session['skills'] = skills
        request.session['missing'] = missing

        return render(request, "builder/result.html", {
            "name": name,
            "role": role,
            "skills": skills,
            "missing": missing
        })

    return render(request, "builder/index.html")


def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    name = request.session.get('name')
    role = request.session.get('role')
    skills = request.session.get('skills')
    missing = request.session.get('missing')

    content = []

    content.append(Paragraph("<b>RESUME</b>", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"<b>Name:</b> {name}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Role:</b> {role}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Skills:</b>", styles['Heading2']))
    for skill in skills.split(","):
        content.append(Paragraph(f"- {skill}", styles['Normal']))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Recommended Skills:</b>", styles['Heading2']))
    for skill in missing:
        content.append(Paragraph(f"- {skill}", styles['Normal']))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Summary:</b>", styles['Heading2']))
    content.append(Paragraph(
        f"Aspiring {role} with skills in {skills}. Actively improving in {', '.join(missing)}.",
        styles['Normal']
    ))

    doc.build(content)

    return response
