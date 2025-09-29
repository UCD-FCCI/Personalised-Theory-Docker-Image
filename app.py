"""
Personalised Theory Docker Image Template

This FastAPI application serves as a template for creating personalized theory
question services that can be deployed as Docker containers.

Template Usage:
1. Modify the main() function to implement your question generation logic
2. Update the returned question and solution content
3. Add any additional functions or endpoints as needed
4. Build and deploy using the provided Dockerfile

This Docker image will be integrated into our new computer-based exam platform.
The platform expects a simple REST API for fetching theory questions and solutions.
"""

from typing import Any

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main() -> dict[str, Any]:
    """
    Main endpoint for the personalized theory question API.

    This endpoint serves as the primary interface for delivering theory questions
    and their solutions. The platform will fetch this endpoint to obtain the question and solution
    when each student reads this question for the first time.

    The question returned from this endpoint will be displayed to the student alongside
    a general instruction of the question. The solution returned from this endpoint
    will be used to facilitate the lecturer to mark the student's answer.

    *THE SOLUTION IS NOT DISPLAYED TO THE STUDENT.*

    Implementation Options:
    - Generate a unique question for each request (dynamic content)
    - Return the same question consistently for all requests (static content)

    Returns:
        dict[str, Any]: A dictionary with two required keys:
            - "question": str - The theory question text to display
            - "solution": str - The corresponding solution
    """
    return {
        "question": "THE GENERATED QUESTION",
        "solution": "THE GENERATED SOLUTION",
    }
