from playwright.sync_api import sync_playwright

from utils import normalize_url
from cookie_handler import accept_cookies
from ga4_validator import validate_ga4_requests
from logger import write_log


def open_website(
    url,
    expected_measurement_id
):
    """
    Opens a website, accepts cookies,
    captures GA4 requests and validates
    the Measurement ID.
    """

    url = normalize_url(url)

    write_log(f"Opening Website : {url}")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        ga4_requests = []

        # ----------------------------------------
        # Capture all network requests
        # ----------------------------------------

        def capture_request(request):

            request_url = request.url

            # Uncomment this only while debugging
            # write_log(request_url)

            if "/g/collect" in request_url:

                write_log(
                    f"GA4 Request Captured : {request_url}"
                )

                ga4_requests.append(request_url)

        page.on(
            "request",
            capture_request
        )

        try:

            # ----------------------------------------
            # Open Website
            # ----------------------------------------

            page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )

            write_log("Website Loaded Successfully")

            # ----------------------------------------
            # Accept Cookies
            # ----------------------------------------

            write_log("Checking Cookie Banner...")

            cookies_accepted = accept_cookies(page)

            if cookies_accepted:

                write_log("Cookies Accepted")

            else:

                write_log("Cookie Banner Not Found")

            # ----------------------------------------
            # Wait for GA4 request
            # ----------------------------------------

            page.wait_for_timeout(5000)

            write_log(
                f"Captured {len(ga4_requests)} GA4 Requests"
            )

            # ----------------------------------------
            # Validate GA4
            # ----------------------------------------

            result = validate_ga4_requests(
                ga4_requests,
                expected_measurement_id
            )

            result["cookies_accepted"] = cookies_accepted

            write_log(
                f"Audit Result : {result['status']}"
            )

            if result["found_measurement_id"]:

                write_log(
                    f"Measurement ID Found : {result['found_measurement_id']}"
                )

            return result

        except Exception as e:

            write_log(f"ERROR : {str(e)}")

            return {
                "status": "FAIL",
                "reason": str(e),
                "found_measurement_id": "",
                "cookies_accepted": False
            }

        finally:

            browser.close()

            write_log("Browser Closed\n")