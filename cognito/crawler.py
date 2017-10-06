from .browser import Browser
from time import sleep
from selenium.webdriver.common.keys import Keys
import json
import re
import requests

cognito_url = 'https://www.cognitoforms.com/'


class CognitoCrawler:
    def __init__(self, _dir):
        self.browser = Browser()
        self.dir = _dir

    def login(self, username, password):
        browser = self.browser
        browser.get(cognito_url + 'login')
        browser.iframe()
        account_elem = browser.find_one('#EmailAddress')
        account_elem.send_keys(username)
        password_elem = browser.find_one('#Password')
        password_elem.send_keys(password)

        login_btn = browser.find_one('button[type="submit"]')
        login_btn.send_keys('\n')
        sleep(2)

    def run(self):
        browser = self.browser
        browser.get(
            cognito_url +
            'forms/leetcodefullstacksoftwareengineer/entries/1-all-entries'
        )
        candidates = self.get_candidates()
        self.store_candidates(candidates)

    def go_to_list(self):
        self.browser.no_iframe().iframe().iframe('#c-entrylist')

    def got_to_details(self):
        self.browser.no_iframe().iframe().iframe('#c-entrydetails')

    def get_candidates(self):
        browser = self.browser

        self.go_to_list()
        canvas = browser.find_one('.slick-viewport')
        sleep(5)
        browser.offset_click(canvas, 0, 132)
        cur_elem = browser.active_elem()

        candidates = {}

        i = 0
        while i < 2:
            i += 1
            self.go_to_list()
            cur_elem.send_keys(Keys.DOWN)
            self.got_to_details()
            entry_id = browser.find_one(
                '.c-entry-id-summary > div > span').text
            if entry_id in candidates:
                break

            name = browser.find_one('.c-name > .c-editor').text
            email = browser.find_one('.c-email > .c-editor').text
            resume_url = browser.find_one('.c-file a').get_attribute('href')
            candidates[entry_id] = {
                'id': entry_id,
                'name': name,
                'email': email,
                'resume_url': resume_url
            }
            print(entry_id, name, email, resume_url)

        return sorted(candidates.values(), key=lambda c: c['id'])

    def download(self, url, _dir='/tmp', prefix=''):
        res = requests.get(url)
        if res.status_code == 200:
            fname = re.findall("filename=(.+)",
                               res.headers['content-disposition'])[0]
            # it might be "xxx.pdf" or xxx.pdf
            fname = fname.replace('"', '')
            with open('%s/%s%s' % (_dir, prefix, fname), 'w') as f:
                f.write(res.content)
                return '%s%s' % (prefix, fname)
        return ''

    def store_candidates(self, candidates):
        for candidate in candidates:
            resume = self.download(
                candidate['resume_url'],
                _dir=self.dir,
                prefix=candidate['id'] + '-')

            candidate.pop('resume_url')
            candidate['resume'] = resume

        out = json.dumps(candidates, ensure_ascii=False)
        with open('%s/canidates.json' % self.dir, 'w') as f:
            f.write(out)
