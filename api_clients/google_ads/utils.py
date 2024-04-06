import time
import json
import yaml
from urllib.parse import urlparse
from urllib.parse import parse_qs

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from google.api_core.exceptions import ResourceExhausted
from google.ads.googleads.client import GoogleAdsClient
from undetected_chromedriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from paths import GMAIL_CREDENTIALS, GOOGLE_CLOUD_CREDENTIALS, GOOGLE_ADS_CONFIG


def safe_google_request(request_function, sleep_time=5):

    def wrapper(*args, **kwargs):
        try:
            response = request_function(*args, **kwargs)
        except ResourceExhausted:
            time.sleep(sleep_time)
            response = request_function(*args, **kwargs)
        except RefreshError:
            from api_clients import GoogleAdsApiClient

            client = GoogleAdsApiClient()
            client.api_client = initialize_google_ads_client()
            response = request_function(*args, **kwargs)

        return response

    return wrapper


def initialize_google_ads_client() -> GoogleAdsClient:
    try:
        return GoogleAdsClient.load_from_storage(GOOGLE_ADS_CONFIG)
    except RefreshError:
        pass

    flow = InstalledAppFlow.from_client_secrets_file(
        GOOGLE_CLOUD_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/adwords"],
        redirect_uri="http://localhost",
    )
    url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
    )

    webdriver = Chrome()
    webdriver.get(url)

    _manually_login(webdriver)
    token = _parse_token(webdriver, flow)

    webdriver.quit()

    _refresh_config(token)

    return GoogleAdsClient.load_from_storage(GOOGLE_ADS_CONFIG)


def _parse_token(webdriver, flow):
    wait = WebDriverWait(webdriver, 10)

    wait.until(EC.url_contains("code="))

    url = webdriver.current_url
    query = urlparse(url).query
    code = parse_qs(query)["code"][0]
    return flow.fetch_token(code=code)


def _manually_login(webdriver):
    with open(GMAIL_CREDENTIALS) as file:
        credentials = json.load(file)

    wait = WebDriverWait(webdriver, 10)

    actions = ActionChains(webdriver)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
    actions.send_keys(credentials["email"]).perform()
    actions.send_keys(Keys.ENTER).perform()

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    actions.send_keys(credentials["password"]).perform()
    actions.send_keys(Keys.ENTER).perform()

    wrapper = wait.until(
        EC.presence_of_element_located((By.ID, "submit_approve_access"))
    )
    button = wrapper.find_element(By.TAG_NAME, "button")
    button.click()


def _refresh_config(token):
    with open(GOOGLE_ADS_CONFIG, "r+") as file:
        data = yaml.safe_load(file)
        data["refresh_token"] = token["access_token"]

        file.seek(0)
        yaml.dump(data, file)
        file.truncate()
