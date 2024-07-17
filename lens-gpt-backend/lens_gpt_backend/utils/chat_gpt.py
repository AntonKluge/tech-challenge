from openai import OpenAI

from lens_gpt_backend.config import CONFIG

client = OpenAI(api_key=CONFIG['OPENAI_API_KEY'])


def ask_chat_gpt(instruction: str, input_text: list[str]) -> str:
    messages = [{"role": "system", "content": instruction}] + [
        {"role": "user" if i % 2 == 0 else "assistant", "content": text} for i, text in enumerate(input_text)]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,  # type: ignore
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Parse the response to extract the producer and model
    response_text = response.choices[0].message.content
    if not response_text:
        raise ValueError("Response text is empty")
    return response_text.strip()
