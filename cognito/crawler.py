from .browser import Browser
from time import sleep
from selenium.webdriver.common.keys import Keys
import json
import os
import time


cognito_url = 'https://www.cognitoforms.com/'


class CognitoCrawler:
    def __init__(self, _dir):
        self.dir = _dir
        self.browser = Browser(_dir)

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
        self.download_resumes(candidates)

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
        print('Extract candidates\' info...')
        while True:
            self.got_to_details()
            entry_id = browser.find_one(
                '.c-entry-id-summary > div > span').text
            if entry_id in candidates:
                break

            name = browser.find_one('.c-name > .c-editor').text
            email = browser.find_one('.c-email > .c-editor').text
            resume_url = browser.find_one(
                '.c-file .c-fileupload-download a').get_attribute('href')
            resume_name = browser.find_one(
                '.c-file .c-fileupload-file a > div').text

            print(entry_id, name, email, resume_name)
            # self.download(resume_url, entry_id, resume_name)

            candidates[entry_id] = {
                'id': entry_id,
                'name': name,
                'email': email,
                'resume_name': resume_name,
                'resume_url': resume_url,
            }
            self.go_to_list()
            cur_elem.send_keys(Keys.DOWN)

        return sorted(candidates.values(), key=lambda c: c['id'])

    def store_candidates(self, candidates):
        # store data before download
        out = json.dumps(candidates)
        with open('%s/canidates.json' % self.dir, 'w') as f:
            f.write(out)

    def load_candidates(self):
        with open('%s/canidates.json' % self.dir) as f:
            candidates = json.loads(f.read())
            return candidates
        return []

    def download(self, url, entry_id, fname):
        # fix dot appear first
        if fname[0] == '.':
            fname = fname[1:]

        ori_name = self.dir + '/' + fname
        new_name = self.dir + '/' + entry_id + '-' + fname

        if os.path.exists(new_name):
            return
        print(entry_id, fname)
        self.browser.get(url)
        counter = 0
        while not os.path.exists(ori_name):
            if counter == 5:
                # fix multiple space problem
                for name in os.listdir(self.dir):
                    if ' '.join(name.split()) == fname:
                        ori_name = self.dir + '/' + name
                        break
            time.sleep(1)
            counter += 1

        os.rename(ori_name, new_name)

    def download_resumes(self, candidates=None):
        print('Download started...')
        if not candidates:
            candidates = self.load_candidates()
        for candidate in candidates:
            self.download(candidate['resume_url'],
                          candidate['id'],
                          candidate['resume_name'])
        print('Download ended')
