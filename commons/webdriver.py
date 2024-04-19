import platform

from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions


class DisplayWebdriver:
    def __init__(self, proxy=None):
        self.is_linux = platform.system() == "Linux"

        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=600,400")
        self.kwargs = {"options": options}
        if proxy:
            self.kwargs["seleniumwire_options"] = {"proxy": proxy}

    def __enter__(self) -> Chrome:
        if self.is_linux:
            from pyvirtualdisplay import Display

            self.display = Display(backend="xvfb")
            self.display.start()

        self.webdriver = Chrome(**self.kwargs)
        return self.webdriver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.webdriver.close()
        self.webdriver.quit()
        if self.is_linux:
            self.display.stop()
