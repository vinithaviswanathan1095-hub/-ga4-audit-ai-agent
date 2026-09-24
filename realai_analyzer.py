import json

from openai import OpenAI

from config import OPENAI_API_KEY

from logger import write_log


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def analyze_all_results(results):

    """
    Uses AI to analyze the complete audit.
    """

    audit_json = json.dumps(
        results,
        indent=2
    )

    prompt = f"""
You are a Senior Google Analytics Implementation Consultant.

Below is the result of a GA4 Audit.

{audit_json}

Please generate a report in the following format.

# Executive Summary

Overall health of all websites.

# Passed Websites

List websites that passed.

# Failed Websites

List failed websites.

# Common Issues

Identify patterns.

# Recommendations

Provide actionable recommendations.

Keep the report under 500 words.
"""

    try:

        write_log(
            "Generating AI Report..."
        )

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content": "You are an expert GA4 Consultant."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.2

        )

        write_log(
            "AI Report Generated"
        )

        return response.choices[0].message.content

    except Exception as e:

        write_log(
            str(e)
        )

        return f"AI Error : {e}"