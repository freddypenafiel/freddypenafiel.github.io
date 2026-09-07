import os
from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_circular_image(input_path, output_path, size=(300, 300)):
    if not os.path.exists(input_path):
        return None
    img = Image.open(input_path).convert("RGBA")
    # Crop center square
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize(size, Image.Resampling.LANCZOS)
    
    # Create circular mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    
    # Create final image with white circular border
    output = Image.new("RGBA", size, (232, 93, 38, 0))
    output.paste(img, (0, 0), mask=mask)
    
    # Draw white border around the circle
    draw_out = ImageDraw.Draw(output)
    border_width = 8
    draw_out.ellipse((border_width//2, border_width//2, size[0]-border_width//2, size[1]-border_width//2), outline=(255, 255, 255, 255), width=border_width)
    
    output.save(output_path, "PNG")
    return output_path

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sidebar_width = 185

    def draw_sidebar(self):
        self.saveState()
        # Sidebar Background
        self.setFillColor(colors.HexColor("#E85D26"))
        self.rect(0, 0, self.sidebar_width, A4[1], fill=True, stroke=False)
        
        # Photo
        circle_img = "imagenes/foto_circulo.png"
        if os.path.exists(circle_img):
            img_size = 110
            img_x = (self.sidebar_width - img_size) / 2
            img_y = A4[1] - img_size - 30
            self.drawImage(circle_img, img_x, img_y, width=img_size, height=img_size, mask='auto')
        
        # Name and Title
        self.setFillColor(colors.white)
        self.setFont("Helvetica-Bold", 17)
        self.drawCentredString(self.sidebar_width / 2, A4[1] - 165, "Freddy Peñafiel")
        
        self.setFillColor(colors.HexColor("#FED7AA"))
        self.setFont("Helvetica", 11)
        self.drawCentredString(self.sidebar_width / 2, A4[1] - 182, "Desarrollador Web Frontend")
        
        # Separator Line
        self.setStrokeColor(colors.HexColor("#FFFFFF"))
        self.setLineWidth(0.8)
        self.line(20, A4[1] - 198, self.sidebar_width - 20, A4[1] - 198)
        
        # Helper for sidebar sections
        y_cursor = A4[1] - 225
        
        def draw_section_header(title, y):
            self.setFillColor(colors.white)
            self.setFont("Helvetica-Bold", 10.5)
            self.drawString(20, y, title)
            # Small underline below section header
            self.setLineWidth(1.5)
            self.setStrokeColor(colors.white)
            self.line(20, y - 4, 20 + self.stringWidth(title, "Helvetica-Bold", 10.5), y - 4)
            return y - 18

        def draw_sidebar_text(items, y):
            for item in items:
                if isinstance(item, tuple):
                    self.setFont("Helvetica-Bold", 8.8)
                    self.setFillColor(colors.white)
                    self.drawString(20, y, item[0])
                    label_w = self.stringWidth(item[0], "Helvetica-Bold", 8.8) + 4
                    self.setFont("Helvetica", 8.8)
                    self.setFillColor(colors.HexColor("#FFF7ED"))
                    self.drawString(20 + label_w, y, item[1])
                    y -= 14
                else:
                    self.setFont("Helvetica", 8.8)
                    self.setFillColor(colors.HexColor("#FFF7ED"))
                    self.drawString(20, y, item)
                    y -= 14
            return y - 12

        # CONTACTO
        y_cursor = draw_section_header("CONTACTO", y_cursor)
        y_cursor = draw_sidebar_text([
            ("▪ Ubicación:", "Azogues, Ecuador"),
            ("▪ Móvil:", "+593 99 895 2547"),
            ("▪ Correo:", "freddypeco1024@gmail.com"),
            ("▪ LinkedIn:", "linkedin.com/in/freddpena"),
            ("▪ Portafolio:", "freddypenafiel.github.io")
        ], y_cursor)

        # IDIOMAS
        y_cursor = draw_section_header("IDIOMAS", y_cursor)
        y_cursor = draw_sidebar_text([
            ("Español:", "Nativo"),
            ("Inglés A2:", "Certificado Oficial (120h)")
        ], y_cursor)

        # TECNOLOGÍAS
        y_cursor = draw_section_header("TECNOLOGÍAS", y_cursor)
        y_cursor = draw_sidebar_text([
            "▪ HTML5 / CSS3 · JavaScript",
            "▪ Python · Java / C#",
            "▪ Git & GitHub · SQL / BD",
            "▪ Ciberseguridad & Redes Cisco"
        ], y_cursor)

        # HABILIDADES BLANDAS
        y_cursor = draw_section_header("HABILIDADES BLANDAS", y_cursor)
        y_cursor = draw_sidebar_text([
            "▪ Responsabilidad y Puntualidad",
            "▪ Trabajo en equipo proactivo",
            "▪ Integridad y ética profesional",
            "▪ Autodidacta y adaptable",
            "▪ Comunicación efectiva"
        ], y_cursor)

        self.restoreState()

    def showPage(self):
        self.draw_sidebar()
        super().showPage()

def generate_pdf():
    create_circular_image("imagenes/foto.jpg", "imagenes/foto_circulo.png")
    
    pdf_path = "CV_Freddy_Penafiel.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=200,  # 185 sidebar + 15 margin
        rightMargin=20,
        topMargin=25,
        bottomMargin=20
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_sec_title = ParagraphStyle(
        'SecTitle',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor('#E85D26'),
        spaceAfter=4
    )
    
    style_body = ParagraphStyle(
        'BodyText',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor('#1E293B')
    )
    
    style_job_header = ParagraphStyle(
        'JobHeader',
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=13,
        textColor=colors.HexColor('#0F172A')
    )
    
    style_job_sub = ParagraphStyle(
        'JobSub',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#475569'),
        spaceAfter=3
    )
    
    style_bullet = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=10
    )

    style_cert_title = ParagraphStyle(
        'CertTitle',
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor('#0F172A')
    )

    style_cert_date = ParagraphStyle(
        'CertDate',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9,
        textColor=colors.HexColor('#FFFFFF'),
        alignment=1
    )

    story = []
    
    def section_header(title):
        t = Table([[Paragraph(title, style_sec_title)]], colWidths=[375])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1.2, colors.HexColor('#E85D26')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
        ]))
        return KeepTogether([t, Spacer(1, 5)])

    # 1. PERFIL PROFESIONAL
    story.append(section_header("PERFIL PROFESIONAL"))
    story.append(Paragraph(
        "Desarrollador web frontend en formación, con sólida experiencia práctica en proyectos institucionales "
        "reales y conocimientos en ciberseguridad, redes e ingeniería de prompts (IA). Me apasiona transformar "
        "ideas en soluciones digitales funcionales, limpias y accesibles. Me caracteriza el compromiso con la "
        "excelencia, la ética en el trabajo y la disposición constante para aprender y aportar valor a cualquier equipo.",
        style_body
    ))
    story.append(Spacer(1, 10))

    # 2. EXPERIENCIA
    story.append(section_header("EXPERIENCIA"))
    
    def add_experience(title, date_str, subtitle, bullets):
        header_table = Table([
            [Paragraph(title, style_job_header), Paragraph(f"<b><font color='#E85D26'>{date_str}</font></b>", ParagraphStyle('RDate', fontName='Helvetica', fontSize=8.5, alignment=2))]
        ], colWidths=[270, 105])
        header_table.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        
        items = [header_table, Paragraph(subtitle, style_job_sub)]
        for b in bullets:
            items.append(Paragraph(f"<font color='#E85D26'>▪</font> {b}", style_bullet))
        items.append(Spacer(1, 6))
        story.append(KeepTogether(items))

    add_experience(
        "Desarrollador — Prácticas de Vinculación", "Nov 2025 – Ene 2026",
        "GAD Municipal del Cantón Biblián · Dirección de Sistemas e Informática (96 horas)",
        [
            "Desarrollé un plan integral de mantenimiento para toda la flota vehicular municipal.",
            "Diseñé e implementé el sistema para seguimiento preventivo y correctivo de vehículos.",
            "Certificado institucional por alta capacidad técnica, responsabilidad y colaboración."
        ]
    )

    add_experience(
        "Desarrollador — Prácticas Pre-Profesionales", "Jun 2026 – Ago 2026",
        "Empresa Eléctrica Azogues C.A. · Área de Informática (96 horas)",
        [
            "Desarrollo web y levantamiento de requerimientos para SAR Reclamos y Sistema PAC.",
            "Gestión en PostgreSQL, Python (Django) e integración de IA (Copilot).",
            "Migración y configuración de servidores de producción Windows, redes y virtualización."
        ]
    )

    add_experience(
        "Desarrollador — Proyecto PACTE", "2024 – 2025",
        "Instituto Superior Tecnológico del Austro · Azogues",
        [
            "Desarrollo de soluciones tecnológicas aplicadas a necesidades del entorno local.",
            "Trabajo colaborativo en proyectos de vinculación comunitaria e institucional."
        ]
    )

    add_experience(
        "Desarrollador — Juego BCI (Brain-Computer Interface)", "2024 – 2025",
        "Proyecto Académico · IST del Austro",
        [
            "Desarrollo de un videojuego controlado por ondas cerebrales integrando hardware BCI y Python.",
            "Proyecto innovador que fusiona neurotecnología con desarrollo de software moderno."
        ]
    )
    story.append(Spacer(1, 2))

    # 3. EDUCACIÓN
    story.append(section_header("EDUCACIÓN"))
    edu_table = Table([
        [Paragraph("Tecnología Superior en Desarrollo de Software", style_job_header), 
         Paragraph("<b><font color='#E85D26'>2023 – Actualidad</font></b>", ParagraphStyle('RDate2', fontName='Helvetica', fontSize=8.5, alignment=2))],
        [Paragraph("<i>Instituto Superior Tecnológico del Austro · Azogues, Cañar</i><br/><font color='#475569'>3er Ciclo en curso | Enfoque en Desarrollo Web, Algoritmos y Programación</font>", style_body), ""]
    ], colWidths=[270, 105])
    edu_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('SPAN', (0,1), (1,1))
    ]))
    story.append(KeepTogether([edu_table, Spacer(1, 10)]))

    # 4. CERTIFICACIONES (2x4 Grid of Cards)
    story.append(section_header("CERTIFICACIONES INSTITUCIONALES"))
    
    def make_cert_card(title, issuer, date_str):
        date_p = Paragraph(f"<b>{date_str}</b>", style_cert_date)
        content_p = Paragraph(f"{title}<br/><font color='#64748B'>{issuer}</font>", style_cert_title)
        
        card_table = Table([
            [date_p],
            [content_p]
        ], colWidths=[180])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#E85D26')),
            ('BACKGROUND', (0,1), (0,1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,0), 2),
            ('BOTTOMPADDING', (0,0), (-1,0), 2),
            ('TOPPADDING', (0,1), (-1,1), 4),
            ('BOTTOMPADDING', (0,1), (-1,1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        return card_table

    certs_data = [
        [
            make_cert_card("10,000 Prompters Ecuador (IA)", "Gobierno Ecuador & Dubai Future Foundation", "2026"),
            make_cert_card("Conceptos básicos de redes", "Cisco Networking Academy", "Jun 2026")
        ],
        [
            make_cert_card("Direccionamiento de red y solución IP", "Cisco Networking Academy", "Jun 2026"),
            make_cert_card("Soporte y Seguridad de red", "Cisco Networking Academy", "Jun 2026")
        ],
        [
            make_cert_card("Introducción a Cisco Packet Tracer", "Cisco Networking Academy", "May 2026"),
            make_cert_card("Python Essentials 1 & 2", "Cisco Networking Academy", "Dic 2025")
        ],
        [
            make_cert_card("Introduction to Cybersecurity", "Cisco Networking Academy", "Ago 2025"),
            make_cert_card("Inglés Nivel A2 — 120 horas", "Ministerio del Trabajo Ecuador", "Feb 2026")
        ]
    ]

    grid_table = Table(certs_data, colWidths=[184, 184])
    grid_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(KeepTogether([grid_table, Spacer(1, 8)]))

    # 5. REFERENCIA Y PIE DE PÁGINA
    story.append(section_header("REFERENCIA PROFESIONAL"))
    ref_table = Table([
        [Paragraph("<b>Ing. Cristian Paulino Cáceres Ortega</b> · <font color='#475569'>Coordinador de Carrera de Desarrollo de Software</font><br/>"
                   "Instituto Superior Tecnológico del Austro · <b>Tel:</b> 0995121479", style_body)]
    ], colWidths=[375])
    ref_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(KeepTogether([ref_table, Spacer(1, 10)]))

    # Footer
    footer_p = Paragraph(
        "<font color='#94A3B8'>Freddy G. Peñafiel Contreras · C.I. 0302886403 · Azogues, Cañar, Ecuador · Portafolio: freddypenafiel.github.io</font>",
        ParagraphStyle('Footer', fontName='Helvetica', fontSize=7.3, alignment=1)
    )
    story.append(footer_p)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("CV generado con éxito en:", pdf_path)

if __name__ == "__main__":
    generate_pdf()
