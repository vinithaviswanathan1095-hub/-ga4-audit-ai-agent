def validate_ga4_requests(
    ga4_requests,
    expected_measurement_id
):
    """
    Validates whether the expected GA4 Measurement ID
    is present in the captured GA4 requests.
    """

    found_measurement_id = ""

    for request in ga4_requests:

        # Check only GA4 collect requests
        if "/g/collect" not in request:
            continue

        # Extract Measurement ID from the request URL
        if "tid=" in request:

            start = request.find("tid=") + 4

            end = request.find("&", start)

            if end == -1:
                end = len(request)

            found_measurement_id = request[start:end]

            # Compare with expected Measurement ID
            if found_measurement_id == expected_measurement_id:

                return {
                    "status": "PASS",
                    "reason": "Correct Measurement ID found",
                    "found_measurement_id": found_measurement_id
                }

    # No matching Measurement ID found
    if found_measurement_id:

        return {
            "status": "FAIL",
            "reason": "Incorrect Measurement ID found",
            "found_measurement_id": found_measurement_id
        }

    return {
        "status": "FAIL",
        "reason": "No GA4 request found",
        "found_measurement_id": ""
    }