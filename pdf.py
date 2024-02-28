import sys
import io
import psycopg2
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from config import load_config
from datetime import datetime

# Obtener la fecha y hora actual
fecha = datetime.now()

# Extraer los componentes de día, mes y año
DD = fecha.day
MM = fecha.month
AAAA = fecha.year

def datos():
    """Traer datos de la tabla empleados"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT cedula, nombre, cargo, departamento FROM empleados WHERE cedula = %s", (str(cedula),))
                row = cur.fetchone()

                while row is not None:
                    print(row)

                    # PyPDF
                    packet = io.BytesIO()
                    can = canvas.Canvas(packet, pagesize=letter)
                    # x (de izquierda a derecha), y (de abajo hacia arriba)
                    can.setFont("Helvetica", 10)
                    if len(row[2]) >= 29:
                        cargo = row[2][:29]+"."
                    else:
                        cargo = row[2]
                    if len(row) >= 2: # Verificar si row tiene al menos 2 elementos
                        can.drawString(157, 694, row[1]) # Suponiendo que row[1] contiene el nombre
                    if len(row) >= 3: # Verificar si row tiene al menos 3 elementos
                        # Agregar otras llamadas drawString para otros valores de la fila
                        can.drawString(35, 655, cargo) # cargo
                        can.drawString(290, 655, row[3]) # departamento
                        can.drawString(495, 655, row[0]) # cedula
                        can.drawString(490, 694, str(DD))
                        can.drawString(523, 694, str(MM))
                        can.drawString(545, 694, str(AAAA))
                        can.drawString(185, 623, desde_str) # desde
                        can.drawString(333, 623, hasta_str) # hasta
                        can.drawString(487, 623, str(total_formatted)) # total
                        can.drawString(120, 595, fundamento) # fundamento
                        can.drawString(315, 433, encargado) # encargado
                        can.save()

                        # Mover al principio del búfer StringIO
                        packet.seek(0)

                        # Crear un nuevo PDF con ReportLab
                        new_pdf = PdfReader(packet)

                        # Leer el PDF existente
                        existing_pdf = PdfReader(open("/path/to/original.pdf", "rb"))
                        output = PdfWriter()

                        # Agregar el "marca de agua" (que es el nuevo PDF) en la página existente
                        page = existing_pdf.pages[0]
                        page.merge_page(new_pdf.pages[0])
                        output.add_page(page)

                        # Finalmente, escribir "output" en un archivo real
                        output_file_path = f"/path/to/solicitud_{cedula}.pdf"
                        with open(output_file_path, "wb") as output_stream:
                            output.write(output_stream)

                    row = cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    # Ruta del archivo de registro
    log_file_path = '/path/to/log.txt'
    # Abrir y leer los datos del archivo de registro
    with open(log_file_path, 'r') as file:
        log_data = file.readlines()

    # Extracting values from log_data
    if len(log_data) >= 1:
        log_data = log_data[0].split() # Dividing the line into individual elements
        cedula = log_data[0]
        fecha_desde = log_data[1]
        fecha_hasta = log_data[2]
        hora_desde = log_data[3]
        hora_hasta = log_data[4]
        # Joining the remaining elements as a single string
        general_info = " ".join(log_data[5:])
        # Splitting fundamento and encargado based on the pipe character
        fundamento, encargado = map(str.strip, general_info.split("|"))

        # Convertir cadenas en objetos datetime
        fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d')
        fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        hora_desde_dt = datetime.strptime(hora_desde, '%H:%M')
        hora_hasta_dt = datetime.strptime(hora_hasta, '%H:%M')

        # Combinar fecha y hora tanto para desde como para hasta
        desde_datetime = datetime.combine(fecha_desde_dt.date(), hora_desde_dt.time())
        hasta_datetime = datetime.combine(fecha_hasta_dt.date(), hora_hasta_dt.time())

        # Formatear fechas y horas como cadenas
        desde_str = desde_datetime.strftime('%d-%m / %H:%M')
        hasta_str = hasta_datetime.strftime('%d-%m / %H:%M')

        # Calcular la duración total en días, horas y minutos
        total = hasta_datetime - desde_datetime
        total_days = total.days
        total_hours, remainder_minutes = divmod(total.seconds, 3600)
        total_minutes = remainder_minutes // 60

        # Formatear la duración total como una cadena
        total_formatted = f"{total_days} días, {total_hours:02d}:{total_minutes:02d} hs"

        # Combinar cadenas de fecha y hora
        desde = f"{fecha_desde_dt.strftime('%d-%m / %H:%M')}"
        hasta = f"{fecha_hasta_dt.strftime('%d-%m / %H:%M')}"

        datos()
