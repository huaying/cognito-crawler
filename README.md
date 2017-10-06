# cognito-crawler
Download resume file and candidate info from Cognito Forms with webdriver

## Setup
1. The chromedrive only works for Mac. You need to download the correct version of chromedrive based on your os.
2. Install library: `pip install -r requirements.txt`
3. `cp secret.py.dist secret.py` and put username and password in the file `secret.py`

## Usage
`python crawler.py`

Then it will download all the resume file into `data/` and create a file `candidates.json` which includes candidates' name / email / resume_name.

