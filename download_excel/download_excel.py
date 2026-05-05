"""
Download automático de Excel do sistema da empresa.
Configurar as credenciais e seletores CSS/XPath no config.json e neste arquivo.
"""
import json
import os
import sys
import time
import logging
import shutil
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


# ── Configuração de log ───────────────────────────────────────────────────────
log_dir = Path(os.getenv("APPDATA", ".")) / "DownloadExcel"
log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "download_excel.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# ── Carrega configurações ─────────────────────────────────────────────────────
def carregar_config() -> dict:
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        log.error("Arquivo config.json não encontrado em: %s", config_path)
        sys.exit(1)
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


# ── Cria driver do Chrome ─────────────────────────────────────────────────────
def criar_driver(pasta_download: str, headless: bool) -> webdriver.Chrome:
    Path(pasta_download).mkdir(parents=True, exist_ok=True)

    prefs = {
        "download.default_directory": pasta_download,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,
    }
    options = Options()
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ── Aguarda download concluir ─────────────────────────────────────────────────
def aguardar_download(pasta: str, timeout: int) -> str | None:
    pasta_path = Path(pasta)
    prazo = time.time() + timeout
    while time.time() < prazo:
        arquivos = [
            f for f in pasta_path.iterdir()
            if f.suffix in (".xlsx", ".xls", ".csv")
            and not f.name.endswith(".crdownload")
            and not f.name.endswith(".tmp")
        ]
        if arquivos:
            mais_recente = max(arquivos, key=lambda f: f.stat().st_mtime)
            if time.time() - mais_recente.stat().st_mtime < 10:
                return str(mais_recente)
        time.sleep(1)
    return None


# ── Fluxo principal ───────────────────────────────────────────────────────────
def executar(cfg: dict) -> None:
    driver = criar_driver(cfg["pasta_download"], cfg.get("headless", True))
    wait = WebDriverWait(driver, 20)

    try:
        # ── 1. Login ──────────────────────────────────────────────────────────
        log.info("Acessando página de login: %s", cfg["url_login"])
        driver.get(cfg["url_login"])

        # ╔══════════════════════════════════════════════════════════════════╗
        # ║  AJUSTE OS SELETORES ABAIXO CONFORME O SITE DA SUA EMPRESA      ║
        # ║  Use F12 no Chrome > inspecionar elemento > copiar seletor CSS   ║
        # ╚══════════════════════════════════════════════════════════════════╝

        # Campo de usuário  →  troque o seletor conforme o site
        campo_usuario = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username'], input[type='email'], #usuario"))
        )
        campo_usuario.clear()
        campo_usuario.send_keys(cfg["usuario"])
        log.info("Usuário preenchido.")

        # Campo de senha  →  troque o seletor conforme o site
        campo_senha = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password'], #senha")
        campo_senha.clear()
        campo_senha.send_keys(cfg["senha"])

        # Botão de login  →  troque o seletor conforme o site
        botao_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], #btnLogin")
        botao_login.click()
        log.info("Login enviado, aguardando redirecionamento...")

        # ── 2. Navegação até o relatório ──────────────────────────────────
        # Exemplo: aguarda menu principal carregar após login
        wait.until(EC.url_changes(cfg["url_login"]))
        log.info("Login efetuado. URL atual: %s", driver.current_url)

        # ╔══════════════════════════════════════════════════════════════════╗
        # ║  ADICIONE AQUI OS PASSOS DE NAVEGAÇÃO DO SEU SISTEMA            ║
        # ║  Exemplos comentados abaixo — descomente e ajuste o necessário  ║
        # ╚══════════════════════════════════════════════════════════════════╝

        # Exemplo: clicar em menu "Relatórios"
        # wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Relatórios"))).click()

        # Exemplo: clicar em submenu "Exportar Excel"
        # wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Exportar Excel"))).click()

        # Exemplo: preencher data inicial
        # campo_data = wait.until(EC.presence_of_element_located((By.ID, "dataInicio")))
        # campo_data.clear()
        # campo_data.send_keys(datetime.now().strftime("%d/%m/%Y"))

        # Exemplo: clicar botão de gerar/baixar
        # wait.until(EC.element_to_be_clickable((By.ID, "btnExportarExcel"))).click()

        # ── 3. Aguarda o arquivo ser baixado ──────────────────────────────
        log.info("Aguardando download do Excel em: %s", cfg["pasta_download"])
        arquivo = aguardar_download(cfg["pasta_download"], cfg.get("aguardar_download_segundos", 30))

        if not arquivo:
            log.error("Download não concluído no tempo esperado.")
            sys.exit(1)

        # ── 4. Renomeia com a data de hoje ────────────────────────────────
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        nome_final = cfg.get("nome_arquivo_final", "relatorio_{data}.xlsx").replace("{data}", data_hoje)
        destino = Path(cfg["pasta_download"]) / nome_final

        if destino.exists():
            destino.unlink()
        shutil.move(arquivo, destino)
        log.info("Arquivo salvo em: %s", destino)

    except TimeoutException as e:
        log.error("Timeout aguardando elemento: %s", e)
        driver.save_screenshot(str(log_dir / "erro_screenshot.png"))
        sys.exit(1)
    except NoSuchElementException as e:
        log.error("Elemento não encontrado: %s", e)
        driver.save_screenshot(str(log_dir / "erro_screenshot.png"))
        sys.exit(1)
    finally:
        driver.quit()


if __name__ == "__main__":
    log.info("=== Iniciando download automático de Excel ===")
    cfg = carregar_config()
    executar(cfg)
    log.info("=== Concluído com sucesso ===")
