# Personalised Theory Docker Image Template

This repository provides a complete template for creating a Docker image that serve personalised theory questions for computer-based examinations. 

## Overview

This Docker image template is designed to integrate with our computer-based exam platform. When deployed, your Docker image will serve theory questions through a simple REST API  at the `/` endpoint. The exam platform will fetch the `/` endpoint to obtain the questions for students and the corresponding solutions for lecturers for marking purposes.

### Key Features

- 📝 **Flexible Question Generation**: Support for both static and dynamic question content
- 🐳 **Docker Ready**: Pre-configured Dockerfile for easy deployment
- ⚡ **FastAPI Backend**: High-performance, modern Python web framework
- 🔧 **Simple Customization**: Simple template structure for easy modification
- 📊 **Exam Platform Integration**: Compatible with the new computer-based exam system

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.12+** (for local development and testing)
- **Git**: [Install Git](https://git-scm.com/downloads)

### Quick Start Guide

1. **Create a new repository from this template**

    1. Open the template repository page:
    https://github.com/UCD-FCCI/Personalised-Theory-Docker-Image

    2. Click "**Use this template**" button at the top right → choose an owner, give the new repository a name, set visibility (**should be Private due to exam security**), then click "**Create repository from template**".

    3. Clone the new repository locally:
    ```bash
    # HTTPS
    git clone https://github.com/YOUR_USERNAME/NEW_REPO_NAME.git

    cd NEW_REPO_NAME
    ```

    > [!NOTE]
    > - Replace YOUR_USERNAME and NEW_REPO_NAME with appropriate values.
    > - After creating the repository, customize app.py and other files as described below.

2. **Customize Your Questions**
   - Edit `app.py` to implement your question logic (see [Customization Guide](#customization-guide))
   - Test your implementation locally (see [Local Testing](#local-testing))

3. **Build Your Docker Image**
   ```bash
   docker build -t <name-of-the-Docker-image> .
   # example: docker build -t fat16-time .
   ```

4. **Test the Container**
   ```bash
   docker run -p 8080:8080 <name-of-the-Docker-image>
   # example: docker run -p 8080:8080 fat16-time
   ```

5. **Access Your API**
   - Open http://localhost:8080 in your browser. You should see a JSON with the two keys `question` and `solution` is returned.

## Project Structure

```
Personalised-Theory-Docker-Image/
├── app.py              # Main application file (customize this)
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
└── README.md          # This documentation
```

## Customization Guide

### Basic Customization

The main customization happens in the `app.py` file. You need to modify the `main()` function to implement your question and solution creation logic.

**Template Structure:**
```python
@app.get("/")
async def main() -> dict[str, Any]:
    return {
        "question": "YOUR QUESTION HERE",
        "solution": "YOUR SOLUTION HERE",
    }
```

### Implementation Examples

#### Example 1: Static Question
For a fixed question that is consistent for all students:

```python
@app.get("/")
async def main() -> dict[str, Any]:
    return {
        "question": "Explain the difference between TCP and UDP protocols in network communication.",
        "solution": "TCP is connection-oriented and reliable with error checking, while UDP is connectionless and faster but less reliable.",
    }
```

#### Example 2: Dynamic Questions
For randomized questions:

```python
import random

@app.get("/")
async def main() -> dict[str, Any]:
    questions = [
        {
            "question": "Explain the role of cryptographic hash functions (e.g., SHA-256) in digital forensics and how they are used during evidence acquisition.",
            "solution": "Hash functions produce a fixed-size fingerprint of data used to verify integrity. Investigators compute and record hashes of storage media and files before and after acquisition to prove no changes occurred. Include algorithm, hash value, and timestamp; use hashes to correlate artifacts and detect tampering."
        },
        {
            "question": "Describe the chain of custody for digital evidence and list the minimum information that must be recorded to preserve admissibility.",
            "solution": "Chain of custody documents every person who handled the evidence and every transfer, with dates/times, reason for transfer, and storage location. Minimum records: evidence identifier, description, collector name, date/time of collection, transfer records (from/to with signatures), storage location, and any actions performed (imaging, analysis) to maintain integrity and reproducibility."
        }
    ]
    
    selected = random.choice(questions)
    return selected
```

#### Example 3: Parameterized Questions
For questions with variable parameters:

```python
import random

@app.get("/")
async def main() -> dict[str, Any]:
    # Generate a random 32-bit value and prepare byte sequences
    value = random.randint(1, 0xFFFFFFFF)
    be_hex = f"{value:08X}"  # big-endian hex digits, MSB first
    bytes_be = [be_hex[i:i+2] for i in range(0, 8, 2)]
    bytes_le = list(reversed(bytes_be))  # little-endian byte order (LSB first)

    endian = random.choice(["big-endian", "little-endian"])
    displayed_hex = "0x" + ("".join(bytes_be) if endian == "big-endian" else "".join(bytes_le))

    # The correct decimal interpretation always comes from the big-endian ordering
    interpreted_decimal = int("0x" + "".join(bytes_be), 16)

    question = f"""
    In a computer forensics investigation you inspect a memory or disk hexdump and find the following 32-bit hexadecimal value represented in {endian} byte order:

    {displayed_hex}

    Tasks:
    1. Convert this hexadecimal value to its decimal representation.
    2. Explain the conversion steps, including how endianness affects interpretation.
    """

    solution = f"""
    Solution:

    Displayed value ({endian}): {displayed_hex}

    Step-by-step explanation:
    - Break the hex into bytes: {', '.join(bytes_le if endian == 'little-endian' else bytes_be)}.
    - If the bytes are little-endian, reverse the byte sequence to get big-endian (human-readable) order: 0x{''.join(bytes_be)}.
    - Convert the big-endian hex to decimal: {interpreted_decimal}.
    """
    
    return {
        "question": question.strip(),
        "solution": solution.strip(),
    }
```

### Advanced Customization

#### Adding Dependencies
If your question generation requires additional Python packages relevant to computer forensics:

1. Add the packages to requirements.txt:
```
fastapi
uvicorn[standard]
<your-additional-package>
```

2. Import and use them in `app.py` (minimal examples):
```python
import <your-additional-package>

from typing import Any

from fastapi import FastAPI

app = FastAPI()

...
```

#### Adding Multiple Endpoints
You can add additional endpoints to help you test the correctness of your question and solution creation logic.

```python
@app.get("/parse")
async def parse_hexdump(hexdump_table: str) -> str:
    # Hexdump parsing logic to obtain some fields
    pass
```

```python
@app.get("/validate")
async def validate_conversion(dec_value: int, provided_hex_str: str) -> bool:
    # Validate a dec-to-hex conversion
    pass
```

> [!NOTE]
> The computer-based exam platform only fetches the `/` endpoint to obtain the questions and solutions. It won't fetch any other endpoints.

#### Including Files or Data
To include data files or templates:

1. Create a `data/` directory in your project
2. Add files to the `data/` directory
3. Update the `Dockerfile` to copy these files:
   ```dockerfile
   COPY data/ ./data/
   ```
4. Access files in your Python code:
   ```python
   # given a list of pre-defined questions is at `data/questions.json`.
   import json
   
   with open('data/questions.json', 'r') as f:
       questions_data = json.load(f)
   ```

## Local Testing

### Method 1: Direct Python Execution
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app:app --host 0.0.0.0 --port 8080

# Test the endpoint
curl http://localhost:8080/
```

### Method 2: Docker Testing
```bash
# Build the image
docker build -t my-theory-questions .

# Run the container
docker run -p 8080:8080 my-theory-questions

# Test the endpoint
curl http://localhost:8080/
```


## API Specification

### Endpoint: `GET /`

**Response Format:**
```json
{
  "question": "string - The question text to display to students",
  "solution": "string - The solution for lecturer reference (not shown to students)"
}
```

**Response Requirements:**
- Both `question` and `solution` fields are required
- Content should be plain text or Markdown formatted
- Questions should be self-contained and clear
- Solutions should provide comprehensive marking guidance

## Best Practices
> [!NOTE]
> The following best practices are optional and for your reference only.

### Question Design
- ✅ **Clear and Concise**: Write questions that are unambiguous
- ✅ **Self-Contained**: Include all necessary context within the question
- ✅ **Consistent Structure**: Maintain consistent question structure
- ✅ **Markdown Format**: The question should be in markdown format

### Solution Design  
- ✅ **Comprehensive**: Include complete solutions with explanations
- ✅ **Marking Criteria**: Provide clear marking guidelines since we'll integrate LLMs to help accelerate your marking process
- ✅ **Common Mistakes**: Note common student errors to watch for

### Technical Best Practices
- ✅ **Error Handling**: Include proper error handling in your code
- ✅ **Logging**: Add logging for debugging purposes
- ✅ **Security**: Don't include sensitive information in the image
- ✅ **Testing**: Thoroughly test your questions before deployment

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError" when running locally**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: "Port already in use" when testing Docker**
```bash
# Solution: Use a different port for the host machine
# This example changes the host port to 8081, 
# while keep the container's internal port to 8080.
docker run -p 8081:8080 my-theory-questions
```

**Issue: Docker build fails**
```bash
# Solution: Check Dockerfile syntax and ensure all files exist
docker build --no-cache -t my-theory-questions .
```

**Issue: Questions not displaying correctly**
- Verify the JSON response format
- Check that both `question` and `solution` keys exist
- Test the endpoint with curl or browser

### Getting Help

1. **Check the Logs**: Use `docker logs <container-id>` to see application logs
2. **Validate JSON**: Ensure your responses are valid JSON format

## Technical Issues

This template is maintained as part of the computer-based examination platform. For technical support or feature requests, please create an [ISSUE](https://github.com/UCD-FCCI/Personalised-Theory-Docker-Image/issues).

### Version History
- **v1.0**: Initial template release with FastAPI and Docker support