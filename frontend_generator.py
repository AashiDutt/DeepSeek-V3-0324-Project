import requests
import json
import os

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

SYSTEM_PROMPT = """
Generate clean HTML with Tailwind CSS classes. Focus on:
1. Use appropriate Tailwind utility classes
2. Ensure text is centered
3. Use clear, visible colors
4. Make content readable

Example for "red button with white text":
<button class="bg-red-500 text-white px-4 py-2 rounded">Click me</button>

Prompt: "A gray box with the text "Hello World" centered inside"
Expected Output:
<div class="bg-gray-300 flex items-center justify-center p-6 rounded-lg">
    <p class="text-black text-xl">Hello World</p>
</div>
"""

def get_component_code(user_prompt: str) -> str:
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']

        # Remove markdown code block markers if present
        if "```" in content:
            content = content.split("```")[1].strip()

        return content.strip() or f"""
            <div class="bg-gray-300 flex items-center justify-center p-6 rounded-lg">
                <p class="text-black text-xl">{user_prompt}</p>
            </div>
        """
    else:
        raise Exception(f"DeepSeek API error {response.status_code}: {response.text}")
