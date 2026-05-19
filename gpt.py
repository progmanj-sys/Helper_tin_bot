from openai import AsyncOpenAI

class ChatGptService:
    def __init__(self, token):

        self.client = AsyncOpenAI(
            api_key=token,
            base_url="https://api.mistral.ai/v1"
        )
        self.message_list = []

    async def send_message_list(self) -> str:
        # Використовуємо модель Mistral
        completion = await self.client.chat.completions.create(
            model="mistral-small-latest",
            messages=self.message_list
        )

        message = completion.choices[0].message

        self.message_list.append({"role": "assistant", "content": message.content})
        return message.content

    def set_prompt(self, prompt_text: str) -> None:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})

    async def add_message(self, message_text: str) -> str:
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()

    async def send_question(self, prompt_text: str, message_text: str) -> str:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()