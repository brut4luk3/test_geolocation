import requests
from fpdf import FPDF

# Coordenadas das capitais do Brasil
coordenadas_capitais = {
    'Rio Branco': (-9.975377, -67.824897),
    'Maceió': (-9.649848, -35.708949),
    'Macapá': (0.035574, -51.070588),
    'Manaus': (-3.106409, -60.026420),
    'Salvador': (-12.971598, -38.501891),
    'Fortaleza': (-3.731861, -38.526670),
    'Brasília': (-15.779720, -47.929720),
    'Vitória': (-20.315590, -40.312800),
    'Goiânia': (-16.686898, -49.264787),
    'São Luís': (-2.538740, -44.282729),
    'Cuiabá': (-15.596411, -56.096276),
    'Campo Grande': (-20.448560, -54.629682),
    'Belo Horizonte': (-19.916681, -43.934493),
    'Belém': (-1.455626, -48.503521),
    'João Pessoa': (-7.121740, -34.882190),
    'Curitiba': (-25.429596, -49.271272),
    'Recife': (-8.054277, -34.881256),
    'Teresina': (-5.089214, -42.801410),
    'Rio de Janeiro': (-22.906847, -43.172897),
    'Natal': (-5.779257, -35.200916),
    'Porto Alegre': (-30.034632, -51.217699),
    'Porto Velho': (-8.760769, -63.900434),
    'Boa Vista': (2.819955, -60.671060),
    'Florianópolis': (-27.594870, -48.548220),
    'São Paulo': (-23.550520, -46.633308),
    'Aracaju': (-10.947247, -37.073072),
    'Palmas': (-10.183040, -48.331810)
}


def criar_documento_pdf(resultado):
    pdf = FPDF()
    pdf.add_page()

    for cidade, dados in resultado.items():
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=cidade, ln=1, align='L')
        pdf.cell(200, 10, txt=f"Latitude: {dados['latitude']}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"Longitude: {dados['longitude']}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"Cidade: {dados['cidade']}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"Estado: {dados['estado']}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"País: {dados['pais']}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"Response code: {dados['response_code']}", ln=1, align='L')
        pdf.cell(200, 10, txt='', ln=1, align='L')

    pdf.output("resultados.pdf")


def testar_geolocalizacao():
    resultado = {}

    for cidade, coordenadas in coordenadas_capitais.items():
        latitude, longitude = coordenadas
        data = {'latitude': latitude, 'longitude': longitude}
        response = requests.post('http://localhost:5000/api/geolocation', json=data)

        try:
            json_response = response.json()
        except ValueError:
            json_response = {}

        resultado[cidade] = {
            'latitude': latitude,
            'longitude': longitude,
            'cidade': json_response.get('cidade', 'Erro de resposta'),
            'estado': json_response.get('estado', 'Erro de resposta'),
            'pais': json_response.get('pais', 'Erro de resposta'),
            'response_code': response.status_code
        }

    # Testes de erro com coordenadas inválidas
    coordenadas_invalidas = [
        (200, 0),  # Latitude inválida (fora do intervalo -90 a 90)
        (-10, 200),  # Longitude inválida (fora do intervalo -180 a 180)
        (None, 0),  # Latitude ausente
        (0, None),  # Longitude ausente
        ('abc', 0),  # Latitude inválida (valor não numérico)
        (0, 'def'),  # Longitude inválida (valor não numérico)
    ]

    for i, coordenadas in enumerate(coordenadas_invalidas, start=1):
        latitude, longitude = coordenadas
        data = {'latitude': latitude, 'longitude': longitude}
        response = requests.post('http://localhost:5000/api/geolocation', json=data)
        response_code = response.status_code

        try:
            json_response = response.json()
        except ValueError:
            json_response = {}

        resultado[f'Teste de erro {i}'] = {
            'latitude': latitude,
            'longitude': longitude,
            'cidade': json_response.get('cidade', 'Erro de resposta'),
            'estado': json_response.get('estado', 'Erro de resposta'),
            'pais': json_response.get('pais', 'Erro de resposta'),
            'response_code': response_code
        }

    criar_documento_pdf(resultado)


if __name__ == '__main__':
    testar_geolocalizacao()