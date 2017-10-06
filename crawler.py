from cognito import CognitoCrawler
from secret import USERNAME, PASSWDORD
import os


cur_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = '%s/data' % cur_dir

if __name__ == '__main__':
    cognito_crawler = CognitoCrawler(data_dir)
    cognito_crawler.login(USERNAME, PASSWDORD)
    cognito_crawler.run()
