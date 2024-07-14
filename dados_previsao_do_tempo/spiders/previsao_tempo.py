import scrapy
import smtplib
from email.message import EmailMessage
import schedule


class PrevisaoTempoSpider(scrapy.Spider):
    name = 'previsao_tempo'

    def start_requests(self):
        # Abrir um site de previsão de tempo e acessa-ló
        urls = [
            'https://www.tempo.com/duque-de-caxias.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Coletar os dados meteorologicos
    #  - Extrair a temperatura atual.
    #  - Extrair a condição do tempo atual (ex. ensolarado, nublado, etc.).
    #  - Extrair a previsão para os próximos 3 dias (temperatura e condição do tempo)

    def parse(self, response):
        contador = 0  # Inicializa um contador
        for tempo in response.xpath('//span[@class="col day_col"]'):
            if contador < 4:  # Verifica se ainda não atingiu o limite de 3 dias
                yield {
                    'Dia': tempo.xpath('.//span[@class="subtitle-m"]/text()').get(),
                    'Temperatua máxima e mínima': tempo.xpath(
                        './/span[@class="max changeUnitT"]/text()').get() + " / " + tempo.xpath(
                        './/span[@class="min changeUnitT"]/text()').get(),
                    'Condição atual': tempo.xpath('.//img[@class="simbW"]/@alt').get()
                }
                contador += 1  # Incrementa o contador
            else:
                break  # Sai do loop se já processou 3 dias


# Não vejo necessidade de tratar os dados, pois retornam no formato que eu desejo.
# pipeline.py -> retorna no formato excel 

# CONFIGURAÇÕES DE ENVIO DE EMAIL
def enviar_email():
    EMAIL_ADDRESS = 'xxxxxxxxxxxxxxxxxxxx'
    EMAIL_PASSWORD = 'xxxxxxxxxxxxx'

    # Enviar um email com os dados coletados

    mail = EmailMessage()
    mail['Subject'] = 'Previsão do tempo'
    mensagem = 'Previsão do tempo para os próximos 3 dias: \n\n'
    mail['From'] = EMAIL_ADDRESS
    mail['To'] = 'xxxxxxxxxxxxxxxxxxxxx'
    mail.add_header('Content-Type', 'text/plain')
    mail.set_payload(mensagem.encode('utf-8'))

    # Anexar os dados coletados ao email
    with open('dados.csv', 'rb') as f:
        dados = f.read()
        nome_arquivo = f.name
        mail.add_attachment(dados, filename=nome_arquivo, maintype='application', subtype='octet-stream')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(mail)

# fazer o agendamento do script 

schedule.every().day.at("08:00").do(PrevisaoTempoSpider)
schedule.every().day.at("08:00").do(enviar_email)
