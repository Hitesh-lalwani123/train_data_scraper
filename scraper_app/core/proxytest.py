from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_proxy(proxy):
    print(f"\nTesting proxy: {proxy}")

    options = Options()
    options.add_argument("--headless=new")  # Headless mode (no visible window)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--proxy-server=http://{proxy}")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://httpbin.org/ip")

        # Wait for IP response to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )

        ip_text = driver.find_element(By.TAG_NAME, "pre").text
        print(f"Proxy {proxy} worked. Detected IP:\n{ip_text}")

        driver.quit()

    except Exception as e:
        print(f"Proxy {proxy} failed: {e}")

# Example proxy (replace with yours)
proxy_to_test = "118.68.64.134:16000"
test_proxy(proxy_to_test)
