
import os
import time
import requests

from typing import List, Optional, ClassVar
from dotenv import load_dotenv

from pydantic import Field
from langchain_core.language_models import LLM
from langchain_core.prompts import PromptTemplate


# --------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv(override=False)


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            "Please check your .env file."
        )

    return value


# --------------------------------------------------
# 2. CUSTOM LLM CLASS
# --------------------------------------------------

class CustomLLM(LLM):

    model: str

    endpoint_url: str

    api_key: str = Field(
        exclude=True,
        repr=False
    )

    temperature: float = 0.5
    top_p: float = 0.9
    max_tokens: int = 1000

    timeout: int = 60
    max_retries: int = 2

    # HTTP errors that may be temporary
    RETRYABLE_STATUS_CODES: ClassVar[set[int]] = {
    500, 502, 503, 408, 504, 429
    }


    # --------------------------------------------------
    # 3. GENERATE LLM RESPONSE
    # --------------------------------------------------

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs
    ) -> str:

        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens
        }

        if stop:
            payload["stop"] = stop

        print("\n========== API REQUEST ==========")
        print("API URL:", self.endpoint_url)
        print("Model:", self.model)
        print("Prompt Length:", len(prompt))

        # --------------------------------------------------
        # 4. RETRY MECHANISM
        # --------------------------------------------------

        for attempt in range(self.max_retries + 1):

            try:

                response = requests.post(
                    self.endpoint_url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )

                print("\n========== API DEBUG ==========")
                print("Attempt:", attempt + 1)
                print("Status Code:", response.status_code)

                # ------------------------------------------
                # SUCCESS RESPONSE
                # ------------------------------------------

                if response.ok:

                    try:
                        data = response.json()

                    except ValueError:
                        raise RuntimeError(
                            "LLM API returned an invalid JSON response."
                        )

                    choices = data.get("choices")

                    if not choices:
                        raise RuntimeError(
                            f"LLM API returned no choices: {data}"
                        )

                    message = choices[0].get("message", {})
                    content = message.get("content")

                    if not content:
                        raise RuntimeError(
                            "LLM API returned an empty response."
                        )

                    # Support string and text-block responses
                    if isinstance(content, str):
                        result = content

                    elif isinstance(content, list):
                        result = "\n".join(
                            item.get("text", "")
                            for item in content
                            if isinstance(item, dict)
                        )

                    else:
                        raise RuntimeError(
                            "Unexpected LLM response format."
                        )

                    if not result.strip():
                        raise RuntimeError(
                            "LLM generated an empty response."
                        )

                    print("\n========== API SUCCESS ==========")
                    print("Response generated successfully.")

                    return result

                # ------------------------------------------
                # ERROR RESPONSE
                # ------------------------------------------

                error_details = response.text[:2000]

                print("Server Response:", error_details)

                # Do not retry permanent request errors
                if response.status_code not in self.RETRYABLE_STATUS_CODES:

                    raise RuntimeError(
                        f"LLM API request failed with "
                        f"HTTP {response.status_code}: {error_details}"
                    )

                # Retry temporary HTTP errors
                if attempt < self.max_retries:

                    retry_after = response.headers.get("Retry-After")

                    try:
                        delay = float(retry_after) if retry_after else 2 ** attempt
                    except ValueError:
                        delay = 2 ** attempt

                    delay = min(delay, 30)

                    print(
                        f"Temporary API error. "
                        f"Retrying in {delay} seconds..."
                    )

                    time.sleep(delay)

                    continue

                raise RuntimeError(
                    f"LLM API failed after "
                    f"{self.max_retries + 1} attempts. "
                    f"HTTP {response.status_code}: {error_details}"
                )

            # ----------------------------------------------
            # CONNECTION AND TIMEOUT ERRORS
            # ----------------------------------------------

            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError
            ) as error:

                print("Connection Error:", str(error))

                if attempt < self.max_retries:

                    delay = 2 ** attempt

                    print(
                        f"Retrying connection in {delay} seconds..."
                    )

                    time.sleep(delay)

                    continue

                raise RuntimeError(
                    f"LLM API connection failed after "
                    f"{self.max_retries + 1} attempts: {error}"
                )

            except requests.exceptions.RequestException as error:

                raise RuntimeError(
                    f"LLM API request error: {error}"
                ) from error

        raise RuntimeError("LLM request failed unexpectedly.")

    # --------------------------------------------------
    # 5. LANGCHAIN IDENTIFICATION
    # --------------------------------------------------

    @property
    def _llm_type(self) -> str:
        return "custom-llm"


# --------------------------------------------------
# 6. INITIALIZE LLM
# --------------------------------------------------

llm = CustomLLM(
    model=get_required_env("MODEL_NAME"),
    endpoint_url=get_required_env("API_URL"),
    api_key=get_required_env("API_KEY"),
    temperature=0.5,
    top_p=0.9,
    max_tokens=1000,
    timeout=60,
    max_retries=2
)


# --------------------------------------------------
# 7. TEST PROMPT
# --------------------------------------------------

prompt = PromptTemplate.from_template(
    "You are a helpful AI assistant. "
    "Reply to: {text}"
)


# --------------------------------------------------
# 8. STANDALONE TEST
# --------------------------------------------------

if __name__ == "__main__":

    user_input = prompt.format(
        text="What is Quantum Computing?"
    )

    try:

        response = llm.invoke(user_input)

        print("\n========== LLM RESPONSE ==========")
        print(response)

    except Exception as error:

        print("\n========== LLM ERROR ==========")
        print(str(error))
