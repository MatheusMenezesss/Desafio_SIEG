from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from service.parser import parse_chave, parse_valor
from service.api_client import submeter_gabarito
import config

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def criar_driver():
    print("[DEBUG] Criando o driver do navegador...")
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def main():
    

    driver = criar_driver()
    try:
        # 1. Executa o Login
        print("[*] Iniciando login no portal...")
        login_page = LoginPage(driver)
        login_page.logar()

        # 2. Acessa o botão específico
        print("[*] Acessando o botão específico...")
        botao_pesquisa = driver.find_element(By.XPATH, "//a[@href='/app/login']")
        botao_pesquisa.click()

        # 3. Clica no botão "Buscar"
        print("[*] Clicando no botão 'Buscar'...")
        botao_buscar = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Buscar']")
        botao_buscar.click()

        # 4. Aguarda os resultados e extrai os dados da tabela
        print("[*] Extraindo os resultados da tabela...")
        tabela = driver.find_element(By.XPATH, "//table")
        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        resultados = []
        for linha in linhas[1:]:  # Ignorar o cabeçalho
            colunas = linha.find_elements(By.TAG_NAME, "td")
            resultado = {
                "Emitente": colunas[0].text,
                "Emissao": colunas[1].text,
                "Status": colunas[2].text,
                "Valor": colunas[3].text,
            }
            resultados.append(resultado)

        print("[*] Resultados extraídos:")
        print(resultados)

        # 5. Mantém o navegador aberto para inspeção
        print("\n[✔] Extração concluída com sucesso!")
        print("[i] O navegador permanecerá aberto para inspeção.")
        input("\n[Pressione ENTER no terminal quando terminar de inspecionar a página...]")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()