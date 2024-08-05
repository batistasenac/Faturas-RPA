import re
import requests
import os
import cv2
import time
import pytesseract
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime


# Desafio Técnico doc9 #
 
# Nesta etapa é realizado a configuração do caminho para o Tesseract OCR #
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Pessoal\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# Nesta etapa Configura o WebDriver #
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

# Abre a página do desafio com a URL
driver.get('https://rpachallengeocr.azurewebsites.net')

#Maximiza a página do navegador
driver.maximize_window()
time.sleep(5)

# Lista para armazenar os dados das faturas
dados = []

# Criado uma função para extrair informações da fatura,incluindo ID, data,vencimento e URL
def extrair_lista():
   
    table = driver.find_element(By.TAG_NAME, 'table')

    for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        id = cells[0].text.strip()
        data = cells[1].text.strip()
        vencimento_data = cells[2].text.strip()
        url = cells[3].find_element(By.TAG_NAME, 'a').get_attribute('href')
        dados.append({
            'ID': id,
            'Data da Fatura': data,
            'Data de Vencimento': vencimento_data,
            'URL da Fatura': url
        })

# Extrair dados da página inicial 
extrair_lista()

# Navega por todas as páginas clicando no botão NEXT e extrai os dados de cada página
while True:
    try:
        botao_next = driver.find_element(By.XPATH, '//a[text()="Next"]')  # Ajuste o seletor conforme necessário
        if 'disabled' in botao_next.get_attribute('class') or botao_next.get_attribute('aria-disabled') == 'true':
            print("Chegou à última página.")
            break  
            # Sai do loop se o botão "Next" está desativado    
        botao_next.click()
        time.sleep(5)  
        
        # Extrair dados da nova página
        extrair_lista()
    except Exception as e:
        print("Não foi possível encontrar o botão 'Next' ou houve um erro:", e)
        break  
        # Sai do loop se o botão "Next" não for encontrado ou houver um erro
        
# Exibe os dados extraídos da tabela
for dado in dados:
# Imprime cada item individualmente
    print(dado)  

# Verificação de Vencimento: Define uma função data_vencida() para verificar se a fatura está vencida.
def data_vencida(vencimento):
    hoje = datetime.today().date()
    vencimento = datetime.strptime(vencimento, '%d-%m-%Y').date()
    return vencimento < hoje

# Filtrar Faturas Vencidas: Filtra a lista de faturas para encontrar apenas datas de vencimento vencidas.
filtro_data_vencimento = list(filter(lambda dado: data_vencida(dado['Data de Vencimento']), dados))

# Exibe as faturas vencidas
print("Faturas com data de vencimento vencida:")
for dado in filtro_data_vencimento:
    print(dado)

# Define o diretório para onde as imagens das faturas serão salvas 
# Lembrando que para incluir um novo caminho é necessário incluir o caminho no download diretório

download_diretorio = "C:\\Users\\Pessoal\\Desktop\\Teste_Tecnico\\imagem_faturas"

# Cria uma função download_image() para baixar imagens das URLs.
def download_image(url, pasta):
    try:
        resposta = requests.get(url, stream=True)
        resposta.raise_for_status()  # Verifica se a solicitação foi bem-sucedida

        filename = url.split('/')[-1]
        caminho_pasta = os.path.join(pasta, filename)

        # Salva a imagem no diretório especificado
        with open(caminho_pasta, 'wb') as file:
            for chunk in resposta.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Imagem salva: {caminho_pasta}")
        return caminho_pasta
    except Exception as e:
        print(f"Erro ao baixar a imagem de {url}: {e}")
        return None

# Verifique se o diretório existe ou não
if not os.path.exists(download_diretorio):
    print(f"Erro: Diretório {download_diretorio} não existe")
else:

    # Lista para armazenar os dados a serem exportados
    exportar_faturas = []

    # Processar apenas imagens associadas as faturas vencidas relacionadas as urls
    for dado in filtro_data_vencimento:
        nome_arquivo = dado['URL da Fatura'].split('/')[-1]
        caminho_pasta = os.path.join(download_diretorio, nome_arquivo)

        # Faz o Download da imagem
        caminho_imagem = download_image(dado['URL da Fatura'], download_diretorio)

        # Verifica se a imagem foi baixada corretamente com extensão jpg e jpeg e se possui valores
        if caminho_imagem and caminho_imagem.lower().endswith(('.jpg', '.jpeg')):
            # Carrega a imagem usando a função imread
            imagem = cv2.imread(caminho_imagem)
            
            if imagem is None:
                print(f"Erro ao carregar a imagem {caminho_imagem}")
                continue

            try:
                # Extrair texto da imagem usando Tesseract OCR
                texto_extraido = pytesseract.image_to_string(imagem)
                
                # Extrair data e número da fatura usando regex para data e número da fatura que está na imagem
                data_encontrada = re.findall(r'\d{4}-\d{2}-\d{2}', texto_extraido)
                numero_fatura = re.findall(r'#(\d+)', texto_extraido)

                # Verificar e imprimir informações
                if data_encontrada and numero_fatura:
                    print(f"URL da Fatura: {dado['URL da Fatura']}")
                    print(f"Data da Fatura: {data_encontrada[0]}")
                    print(f"Número da Fatura: {numero_fatura[0]}")

                    # Adicionar todoos dados extraídos à lista
                    exportar_faturas.append({
                        'URL da Fatura': dado['URL da Fatura'],
                        'Data da Fatura': data_encontrada[0],
                        'Numero da Fatura': numero_fatura[0]
                    })
                else:
                    print(f"Nenhuma data ou número da fatura encontrado na imagem")

            except Exception as e:
                print(f"Erro ao extrair texto da imagem {caminho_imagem}: {e}")
  
        
    # Convertendo os dados para um DataFrame do pandas
    df = pd.DataFrame(exportar_faturas)

    # Caminho para o arquivo CSV
    caminho_arquivo_excel = "C:\\Users\\Pessoal\\Desktop\\Teste_Tecnico\\faturas_vencidas.csv"

    # Exporta o DataFrame para um arquivo CSV com o delimitador de ponto e vírgula sem o indíce 
    df.to_csv(caminho_arquivo_excel, index=False, sep=';',encoding='utf-8')



# Fecha o navegador
driver.quit()
