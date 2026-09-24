from playwright.sync_api import TimeoutError


def accept_cookies(page):

    try:

        print("Waiting for OneTrust cookie banner...")

        page.wait_for_selector(
            "#onetrust-accept-btn-handler",
            timeout=5000
        )

        button = page.locator(
            "#onetrust-accept-btn-handler"
        )

        if button.is_visible():

            print("Cookie banner found.")

            button.click()

            page.wait_for_timeout(2000)

            print("Cookies accepted.")

            return True

    except TimeoutError:

        print("OneTrust banner not found.")

    except Exception as e:

        print("Cookie Error:", e)

    return False