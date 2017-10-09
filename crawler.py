import argparse
import os

from cognito import CognitoCrawler
from secret import USERNAME, PASSWDORD


cur_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = '%s/data' % cur_dir


def usage():
    return '''
        python crawler.py
        python crawler.py --dowanlod_only
    '''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cognito Forms Crawler',
                                     usage=usage())

    parser.add_argument('--dowanlod_only', action='store_true', default=False)
    args = parser.parse_args()

    cognito_crawler = CognitoCrawler(data_dir)
    cognito_crawler.login(USERNAME, PASSWDORD)
    if args.dowanlod_only:
        cognito_crawler.download_resumes()
    else:
        cognito_crawler.run()
