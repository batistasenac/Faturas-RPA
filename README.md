Resumo do Processo de Extração e Processamento de Faturas
1. Configuração do Ambiente
Instalação e Importação: Importa as bibliotecas necessárias, incluindo re, requests, os, cv2, time, pytesseract, csv, pandas, selenium e datetime.
Configuração do Tesseract OCR: Define o caminho para o executável do Tesseract OCR.
--------------------------------------------------------------------------------------------------------------------------------------------------

2. Configuração do WebDriver
Inicialização do WebDriver: Configura e inicializa o WebDriver do Firefox usando webdriver.Firefox() e GeckoDriverManager().
--------------------------------------------------------------------------------------------------------------------------------------------------

3. Acesso e Navegação na Página
Abrir Página: Acessa a página de desafios de OCR.
Maximizar Janela: Maximiza a janela do navegador para melhor visualização.
Extrair Dados: Cria uma função extrair_lista() para extrair informações da tabela de faturas, incluindo ID, data, vencimento e URL.
------------------------------------------------------------------------------------------------------------------------------------

4. Navegação entre Páginas
Loop de Navegação: Navega por todas as páginas clicando no botão "Next" e extrai os dados de cada página.
------------------------------------------------------------------------------------------------------------------------------------

5. Filtragem de Dados
Verificação de Vencimento: Define uma função data_vencida() para verificar se a fatura está vencida.
Filtrar Faturas Vencidas: Filtra a lista de faturas para obter apenas aquelas com data de vencimento vencida.
---------------------------------------------------------------------------------------------------------------------------------------

6. Download e Processamento de Imagens
Definir Diretório de Download: Define o diretório para onde as imagens das faturas serão salvas.
Função de Download: Cria uma função download_image() para baixar imagens das URLs.
Processar Imagens: Para cada fatura vencida, baixa a imagem, usa o OpenCV para carregar e o Tesseract OCR para extrair texto.
----------------------------------------------------------------------------------------------------------------------------------------

7. Extração de Dados das Imagens
Extração de Texto: Usa regex para extrair a data e o número da fatura do texto extraído das imagens.
Adicionar Dados ao Export Data: Adiciona os dados extraídos à lista export_data.
----------------------------------------------------------------------------------------------------

8. Exportação dos Dados
Criação do DataFrame: Converte a lista export_data para um DataFrame usando pandas.
Exportar para CSV: Usa df.to_csv() para exportar o DataFrame para um arquivo CSV com delimitador de ponto e vírgula.
---------------------------------------------------------------------------------------------------------------------

9. Finalização
Fechar Navegador: Fecha o navegador após a conclusão do processo.

----------------------------------------------------------------------------------------------------------

Observação: O projeto foi executado trazendo as imagens das faturas vencidas, localizadas na pasta imagens_faturas, com a finalidade de extrair informações solicitadas nas imagens.
