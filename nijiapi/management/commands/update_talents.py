import json

from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from talents.models import Talent


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
        # ウィンドウサイズを大きくしておかないとPC専用の要素が取得できない
        driver.set_window_size(1920, 1080)

        # slug を元に個別ページへアクセスし、情報を取得する
        base_url = 'https://www.nijisanji.jp/talents/l/'
        talents = Talent.objects.all().order_by('id')
        for talent in talents:
            url = f'{base_url}{talent.slug}'
            print('-----------------------------')
            print(f'url: {url}')
            driver.get(url)
            driver.implicitly_wait(1)

            name = driver.find_element(By.CLASS_NAME, 'talents-detail_liverName__l_bfT').text
            name_ruby = driver.find_element(By.CLASS_NAME, 'talents-detail_liverRuby__WNv_o').text
            name_en = driver.find_element(By.CLASS_NAME, 'talents-detail_liverEnName__k9908').text
            description = driver.find_element(By.CLASS_NAME, 'talents-detail_liverDescription__N3pxj').text

            # 誕生日/ファンネーム
            content_rows = driver.find_elements(By.CLASS_NAME, 'talents-detail_row__PrEYp')
            if len(content_rows) > 0:
                content_rows_texts = [row.find_element(By.CLASS_NAME, 'talents-detail_content__epVfd').text for row in content_rows]
                birthday = content_rows_texts[0]
                fan_name = content_rows_texts[1]

            # アカウント
            sns_account_a_tags = driver.find_elements(By.CLASS_NAME, 'sns-link_snsLink__AbkSN')
            youtube_id = ''
            x_id = ''
            twitch_id = ''
            funclub_id = ''
            for a_tag in sns_account_a_tags:
                url = a_tag.get_attribute('href')
                if 'youtube.com' in url:
                    youtube_id = url.split('/')[-1]
                elif 'twitter.com' in url:
                    x_id = url.split('/')[-1]
                elif 'x.com' in url:
                    x_id = url.split('/')[-1]
                elif 'twitch.tv' in url:
                    twitch_id = url.split('/')[-1]
                elif 'fanclub.nijisanji.jp' in url:
                    funclub_id = url.split('/')[-1]

            talent.name = name
            talent.name_ruby = name_ruby
            talent.name_en = name_en
            talent.description = description
            talent.birthday = birthday
            talent.fan_name = fan_name
            talent.youtube_id = youtube_id
            talent.x_id = x_id
            talent.twitch_id = twitch_id
            talent.funclub_id = funclub_id
            talent.save()

        driver.quit()
