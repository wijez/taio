import time
import logging
import multiprocessing


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constant import taio_constant
from settings import Settings
from process_zip import delete_pdf_files, count_log_lines

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('taio-bill')
settings = Settings()


edge_options = Options()
prefs = {
    "download.default_directory": settings.download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
edge_options.add_experimental_option("prefs", prefs)
# edge_options.add_argument("--headless")
# edge_options.add_argument("--disable-gpu")
driver = webdriver.Edge(options=edge_options)
wait = WebDriverWait(driver, 30)
driver.maximize_window()
logger.info("Starting...")
driver.get(taio_constant.URL)
logger.info(f'Loading {taio_constant.URL}...')
driver.find_element(By.XPATH, value=taio_constant.FIELD_ACCOUNT).send_keys(settings.account)
time.sleep(taio_constant.DELAY_TIME_SKIP)
driver.find_element(By.XPATH, value=taio_constant.FIELD_PASSWORD).send_keys(settings.password)
time.sleep(taio_constant.DELAY_TIME_SKIP)
driver.find_element(By.XPATH, value=taio_constant.BUTTON_LOGIN).click()
time.sleep(taio_constant.DELAY_TIME_LOAD_PAGE)
driver.find_element(By.XPATH, value=taio_constant.BUTTON_BILL).click()
time.sleep(taio_constant.DELAY_TIME_SKIP)


def log_info():
    number = driver.find_element(By.XPATH, value=taio_constant.NUMBER).text
    logger.info(f"number {number}")
    log_entry = f" number {number}\n"

    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)


def move_current_page():
    line = count_log_lines('log.txt')
    print("line", line)
    result = line // 10
    row = (line % 10) + 2
    taio_constant.update_row(row)
    next_page = result % 5
    next_5_page = result // 5
    for _ in range(next_5_page):
        taio_constant.update_next_5_page(_)
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, taio_constant.NEXT_5_PAGE)))
        next_page_button.click()
        time.sleep(taio_constant.SLEEP)
    for _ in range(next_page):
        taio_constant.update_next_page(_, next_5_page)
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, taio_constant.PAGE)))
        next_page_button.click()
        time.sleep(taio_constant.SLEEP)


move_current_page()
current_row = wait.until(EC.element_to_be_clickable((By.XPATH, taio_constant.ROW)))
current_row.click()
time.sleep(taio_constant.DELAY_TIME_LOAD_PAGE)


def enable_move(first_pos):
    for _ in range(first_pos):
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, taio_constant.NEXT_PAGE)))
        next_page_button.click()
        time.sleep(taio_constant.SLEEP)


def process_page(first_pos, worker):
    enable_move(first_pos)

    while True:
        time.sleep(taio_constant.DELAY_TIME_LOAD_PAGE)
        log_info()
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, taio_constant.BUTTON_DOWNLOAD)))
        download_button.click()
        time.sleep(taio_constant.SLEEP)
        # delete_pdf_files(download_directory)
        enable_move(worker)
        time.sleep(taio_constant.DELAY_TIME_LOAD_PAGE)


def main():
    # processes = []
    for _ in range(2):
        p = multiprocessing.Process(target=process_page, args=(_, 2))
        # processes.append(p)
        p.start()
        time.sleep(taio_constant.SLEEP)

    # for p in processes:
    #     p.join()


if __name__ == '__main__':
    main()
