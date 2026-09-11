import json
import os
import re
import time
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from service.parser import parse_chave, parse_valor
from service.api_client import submeter_gabarito
import config


CAMINHO_JSON = "data/resultados.json"
PASTA_DOWNLOADS = os.path.abspath("data/downloads")


# ---------------------------------------------------------------------------
# Setup do driver
# ---------------------------------------------------------------------------

def criar_driver():
    print("[DEBUG] Criando o driver do navegador...")
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    os.makedirs(PASTA_DOWNLOADS, exist_ok=True)
    prefs = {
        "download.default_directory": PASTA_DOWNLOADS,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        # evita abrir o PDF no viewer interno do Chrome e força o download
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ---------------------------------------------------------------------------
# Popups (pesquisa de satisfação, novidades, cookies)
# ---------------------------------------------------------------------------

def fechar_popup_overlay(driver, timeout=2):
    """Fecha qualquer popup do tipo .np-overlay (serve tanto para a pesquisa
    de satisfação quanto para o aviso de novidade, já que os dois usam a
    mesma estrutura + botão 'Fechar')."""
    try:
        popup = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".np-overlay"))
        )
        botao_fechar = popup.find_element(
            By.XPATH, ".//button[contains(normalize-space(), 'Fechar')]"
        )
        botao_fechar.click()

        WebDriverWait(driver, 3).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".np-overlay"))
        )
        print("[+] Popup (.np-overlay) fechado.")
        return True

    except TimeoutException:
        return False
    except StaleElementReferenceException:
        return False


def aceitar_cookies(driver, timeout=2):
    try:
        botao = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(normalize-space(), 'Aceitar')]")
            )
        )
        botao.click()
        print("[+] Banner de cookies aceito.")
    except TimeoutException:
        pass


def tratar_popups(driver):
    """Fecha, em sequência, todos os popups que podem estar na tela
    (pode haver mais de um .np-overlay empilhado)."""
    while fechar_popup_overlay(driver, timeout=2):
        pass
    aceitar_cookies(driver)


def verificar_captcha(driver):
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "form[action='/app/captcha']")
            )
        )
        print("\n[!] Verificação de segurança detectada.")
        print("[!] Resolva a operação no navegador.")
        input("[*] Pressione ENTER depois de concluir a verificação...")
        return True
    except TimeoutException:
        return False


# ---------------------------------------------------------------------------
# Persistência incremental em JSON
# ---------------------------------------------------------------------------

def carregar_resultados_existentes(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def salvar_resultado(caminho, registro):
    """Concatena um novo registro no arquivo JSON sem perder o que já
    foi salvo (lê tudo, faz append, regrava)."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    resultados = carregar_resultados_existentes(caminho)
    resultados.append(registro)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Download do PDF
# ---------------------------------------------------------------------------

def esperar_download(pasta, arquivos_antes, timeout=30):
    def arquivos_prontos():
        atuais = set(os.listdir(pasta))
        novos = atuais - arquivos_antes
        return [
            f for f in novos
            if not f.startswith(".")          # arquivos temporários ocultos do Chrome
            and not f.endswith(".crdownload")
            and not f.endswith(".tmp")
        ]

    inicio = time.time()
    candidato = None
    while time.time() - inicio < timeout:
        prontos = arquivos_prontos()
        if prontos:
            candidato = os.path.join(pasta, prontos[0])
            break
        time.sleep(0.3)

    if not candidato:
        return None

    # espera o tamanho do arquivo parar de mudar, garantindo que o Chrome
    # terminou de gravar (evita pegar o arquivo "pela metade")
    tamanho_anterior = -1
    while time.time() - inicio < timeout:
        try:
            tamanho_atual = os.path.getsize(candidato)
        except OSError:
            time.sleep(0.3)
            continue
        if tamanho_atual == tamanho_anterior and tamanho_atual > 0:
            return candidato
        tamanho_anterior = tamanho_atual
        time.sleep(0.3)

    return candidato


def baixar_pdf(driver, identificador):
    arquivos_antes = set(os.listdir(PASTA_DOWNLOADS))
    try:
        botao_pdf = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(normalize-space(.), 'Baixar PDF')]"
                " | //a[contains(normalize-space(.), 'Baixar PDF')]"
            ))
        )
        botao_pdf.click()
    except TimeoutException:
        print(f"[!] Botão 'Baixar PDF' não encontrado para {identificador}.")
        return None

    caminho_baixado = esperar_download(PASTA_DOWNLOADS, arquivos_antes)
    if not caminho_baixado:
        print(f"[!] Download do PDF não concluiu a tempo para {identificador}.")
        return None

    nome_seguro = identificador.replace("/", "-").strip()
    novo_caminho = os.path.join(PASTA_DOWNLOADS, f"{nome_seguro}.pdf")
    try:
        if os.path.exists(novo_caminho):
            os.remove(novo_caminho)
        os.rename(caminho_baixado, novo_caminho)
    except OSError as e:
        print(f"[!] Falha ao renomear PDF de {identificador}: {e}")
        return caminho_baixado  # mantém o caminho original em vez de perder o arquivo
    print(f"[+] PDF salvo em {novo_caminho}")
    return novo_caminho


# ---------------------------------------------------------------------------
# Extração da página de detalhe
# ---------------------------------------------------------------------------

def pegar_valor_por_label(driver, texto_label):
    """
    Busca o valor associado a um rótulo na página de detalhe, assumindo que
    o valor é o elemento-irmão seguinte ao rótulo.

    ATENÇÃO: ajuste este XPath se a estrutura real do HTML da página de
    detalhe for diferente (ex.: rótulo e valor dentro do mesmo <td>, ou uma
    tabela com <th>/<td>). Se me mandar o HTML dessa página eu deixo isso
    preciso.
    """
    try:
        xpath = (
            f"//*[self::td or self::th or self::span or self::div or self::dt]"
            f"[contains(normalize-space(.), '{texto_label}')]"
            f"/following-sibling::*[1]"
        )
        elemento = driver.find_element(By.XPATH, xpath)
        return elemento.text.strip()
    except Exception:
        return None


def extrair_detalhe(driver):
    tratar_popups(driver)
    return {
        "chave_acesso": pegar_valor_por_label(driver, "Chave de acesso"),
        "cnpj": pegar_valor_por_label(driver, "CNPJ"),
        "valor_total": pegar_valor_por_label(driver, "Valor total"),
    }


# ---------------------------------------------------------------------------
# Loop principal de coleta
# ---------------------------------------------------------------------------

def extrair_itens_formato_tabela(driver):
    tabelas = driver.find_elements(By.TAG_NAME, "table")
    if not tabelas:
        return None

    linhas = tabelas[0].find_elements(By.TAG_NAME, "tr")
    itens = []
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if not colunas:
            continue
        try:
            link_detalhe = colunas[-1].find_element(By.TAG_NAME, "a").get_attribute("href")
        except Exception:
            link_detalhe = None

        itens.append({
            "numero": colunas[0].text.strip(),
            "emitente": colunas[1].text.strip(),
            "emissao": colunas[2].text.strip(),
            "status": colunas[3].text.strip(),
            "valor": colunas[4].text.strip(),
            "link_detalhe": link_detalhe,
        })
    return itens


def extrair_itens_formato_lista(driver):
    itens_li = driver.find_elements(By.CSS_SELECTOR, "ul.notas-list li")
    if not itens_li:
        return None

    itens = []
    for li in itens_li:
        try:
            link = li.find_element(By.TAG_NAME, "a")
            emitente = link.text.strip()
            link_detalhe = link.get_attribute("href")
        except Exception:
            emitente, link_detalhe = None, None

        try:
            status = li.find_element(By.CSS_SELECTOR, "span.badge").text.strip()
        except Exception:
            status = None

        try:
            texto_kv = li.find_element(By.CSS_SELECTOR, "div.kv").text.strip()
        except Exception:
            texto_kv = ""

        # Ex.: "Nota 132796/7 · 68228210703321 · 2025-12-20 · R$ 334,49"
        m = re.match(
            r"Nota\s+([\d/]+)\s*·\s*(\d+)\s*·\s*([\d-]+)\s*·\s*R\$\s*([\d\.,]+)",
            texto_kv,
        )
        if m:
            numero, cnpj, emissao, valor = m.groups()
        else:
            numero, cnpj, emissao, valor = None, None, None, None
            print(f"[!] Não consegui interpretar a linha: '{texto_kv}'")

        itens.append({
            "numero": numero,
            "emitente": emitente,
            "emissao": emissao,
            "status": status,
            "valor": valor,
            "cnpj": cnpj,
            "link_detalhe": link_detalhe,
        })
    return itens


def processar_pagina(driver):
    tratar_popups(driver)
    print("[*] Aguardando resultados...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table, ul.notas-list"))
        )
    except TimeoutException:
        print("[!] Nem <table> nem <ul class='notas-list'> apareceram. HTML atual do <main>:")
        try:
            print(driver.find_element(By.TAG_NAME, "main").get_attribute("outerHTML")[:4000])
        except Exception:
            print(driver.page_source[:4000])
        raise

    # Guarda os dados ANTES de navegar para o detalhe, pra não sofrer com
    # StaleElementReferenceException depois que a página mudar.
    itens_da_pagina = extrair_itens_formato_tabela(driver)
    if itens_da_pagina is None:
        itens_da_pagina = extrair_itens_formato_lista(driver) or []

    print(f"[+] {len(itens_da_pagina)} itens encontrados nesta página.")

    for item in itens_da_pagina:
        numero = item["numero"]
        link_detalhe = item.pop("link_detalhe")

        if not link_detalhe:
            print(f"[!] Sem link de detalhe para {numero}, salvando só os dados da tabela.")
            salvar_resultado(CAMINHO_JSON, item)
            continue

        print(f"[*] Abrindo detalhe de {numero}...")
        driver.get(link_detalhe)

        detalhe = extrair_detalhe(driver)
        pdf_path = baixar_pdf(driver, numero)

        # não deixa um campo None do detalhe sobrescrever um valor que já
        # veio certo da listagem (ex.: cnpj já extraído do formato em lista)
        detalhe_valido = {k: v for k, v in detalhe.items() if v is not None}
        registro = {**item, **detalhe_valido, "pdf": pdf_path}
        salvar_resultado(CAMINHO_JSON, registro)

        driver.back()
        tratar_popups(driver)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table, ul.notas-list"))
        )


def ja_esta_nos_resultados(driver):
    """Detecta se a página atual já é a de resultados, para não tentar
    clicar num botão 'Buscar' que pode não existir nesta rodada."""
    try:
        driver.find_element(By.CSS_SELECTOR, "table, ul.notas-list")
        return True
    except Exception:
        return False


def ir_para_proxima_pagina(driver):
    try:
        link_proxima = driver.find_element(By.PARTIAL_LINK_TEXT, "próxima")
    except Exception:
        return False
    link_proxima.click()
    return True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    driver = criar_driver()
    try:
        print("[*] Iniciando login no portal...")
        login_page = LoginPage(driver)
        login_page.logar()

        tratar_popups(driver)

        print("[*] Acessando o botão específico...")
        for tentativa in range(3):
            try:
                botao_pesquisa = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
                )
                botao_pesquisa.click()
                break
            except StaleElementReferenceException:
                print(f"[!] Botão foi atualizado. Tentativa {tentativa + 1}/3...")

        tratar_popups(driver)

        if ja_esta_nos_resultados(driver):
            print("[*] Já está na página de resultados, pulando o clique em 'Buscar'.")
        else:
            print("[*] Clicando no botão 'Buscar'...")
            try:
                botao_buscar = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(normalize-space(.), 'Buscar')]"
                        " | //input[@type='submit' and contains(@value, 'Buscar')]"
                    ))
                )
                botao_buscar.click()
            except TimeoutException:
                print("[*] Nenhum botão 'Buscar' encontrado. Assumindo que a busca "
                      "já foi disparada pelo clique anterior.")

        verificar_captcha(driver)
        tratar_popups(driver)

        pagina = 1
        while True:
            print(f"\n[=] Processando página {pagina}...")
            processar_pagina(driver)

            if not ir_para_proxima_pagina(driver):
                print("[✔] Não há mais páginas. Extração concluída.")
                break

            tratar_popups(driver)
            pagina += 1

        print(f"\n[✔] Todos os dados foram salvos em {CAMINHO_JSON}")
        print(f"[✔] PDFs salvos em {PASTA_DOWNLOADS}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()