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
        url = 'https://www.nijisanji.jp/talents/'
        driver.get(url)

        # __NEXT_DATA__ に含まれる JSON を取得
        next_data = driver.find_element(By.ID, '__NEXT_DATA__').get_attribute('innerHTML')
        data = json.loads(next_data)
        all_livers = data['props']['pageProps']['allLivers']

        """
        all_livers は 2024/02 時点で以下のような構造になっているので、slug が分かれば個別のタレントページにアクセスできる
        - id                : 内部IDと思われる
        - slug              : タレントごとのページにアクセスするための識別子
        - name              : タレント名
        - enName            : タレント名（英語表記）
        - profile
          - affiliation     : 所属事務所(にじさんじ)
          - debutat         : デビュー日時(ISO 8601形式)
        - images
          - head
            - url           : タレントの画像URL
          - width           : 画像の幅
          - height          : 画像の高さ
        - socialLinks
          - fanclub         : ファンクラブURL
          - subscribeCount  : チャンネル登録者数
          - orderbyRuby     : 不明
          - orderbyEnName   : 不明
        """

        # debutAt の昇順でソート
        all_livers = sorted(all_livers, key=lambda x: x['profile']['debutAt'])

        # Talent モデルにデータを保存していく
        # ただし、既に存在している場合は更新する
        for liver in all_livers:
            name = liver['name'] if liver.get('name') else ''
            name_en = liver['enName'] if liver.get('enName') else ''
            slug = liver['slug'] if liver.get('slug') else ''
            affiliation = liver['profile'].get('affiliation', '')
            debut_at = liver['profile'].get('debutAt', None)
            fanclub_url = liver['socialLinks'].get('fanclub', '')

            # タレントを検索し、一致する場合は更新、それ以外の場合は新規作成
            talent, created = Talent.objects.update_or_create(
                name=name,
                defaults={
                    'name_en': name_en,
                    'slug': slug,
                    'affiliation': affiliation[0],
                    'debut_at': debut_at,
                    'fanclub_url': fanclub_url
                }
            )

            if created:
                print(f'{talent.name} を新規作成しました')
            else:
                print(f'{talent.name} を更新しました')

            talent.save()

        driver.quit()
