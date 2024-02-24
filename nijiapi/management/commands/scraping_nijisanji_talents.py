from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Command(BaseCommand):
    help = 'にじさんじのタレント一覧をスクレイピングして取得する'

    def handle(self, *args, **options):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        # FIXME: 本番環境では危険なので非推奨。対策を考える。
        chrome_options.add_argument("--no-sandbox")

        new_driver = ChromeDriverManager().install()
        service = Service(executable_path=new_driver)

        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.get('https://www.nijisanji.jp/talents?filter=nijisanji&orderKey=debut_at&order=asc')
        print(driver.title)
