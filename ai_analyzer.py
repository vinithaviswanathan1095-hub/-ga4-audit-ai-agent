from logger import write_log


def analyze_all_results(results):
    """
    Generate an AI-style audit report without calling OpenAI.
    This is a mock implementation for development and testing.
    """

    write_log("Generating AI Audit Report...")

    total_sites = len(results)

    passed_sites = [
        site for site in results
        if site["status"] == "PASS"
    ]

    failed_sites = [
        site for site in results
        if site["status"] == "FAIL"
    ]

    pass_count = len(passed_sites)
    fail_count = len(failed_sites)

    pass_rate = round((pass_count / total_sites) * 100, 2) if total_sites > 0 else 0

    report = f"""
# 🤖 GA4 Audit AI Report

## Executive Summary

- Total Websites Audited : **{total_sites}**
- Passed : **{pass_count}**
- Failed : **{fail_count}**
- Success Rate : **{pass_rate}%**

---

## Passed Websites

"""

    if passed_sites:

        for site in passed_sites:

            report += (
                f"- {site['site']} "
                f"(Measurement ID: {site['found_measurement_id']})\n"
            )

    else:

        report += "No websites passed the audit.\n"

    report += "\n---\n\n## Failed Websites\n\n"

    if failed_sites:

        for site in failed_sites:

            report += (
                f"### {site['site']}\n"
                f"- Expected Measurement ID : {site['expected_measurement_id']}\n"
                f"- Found Measurement ID : {site['found_measurement_id'] or 'Not Found'}\n"
                f"- Reason : {site['reason']}\n\n"
            )

    else:

        report += "No failed websites.\n"

    report += """
---

## Common Recommendations

"""

    if fail_count == 0:

        report += """
- All audited websites appear to have a valid GA4 implementation.
- Continue monitoring deployments after GTM or website releases.
- Periodically verify Measurement IDs across environments.
"""

    else:

        report += """
- Verify the GA4 Measurement ID configured in Google Tag Manager.
- Ensure the correct GTM container is published.
- Verify that GA4 tags fire after cookie consent.
- Check whether Consent Mode is blocking analytics requests.
- Review browser console errors if no GA4 requests are detected.
"""

    write_log("AI Audit Report Generated Successfully")

    return report