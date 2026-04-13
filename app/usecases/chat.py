from typing import List, Dict
from app.core.errors import NotFoundError
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.schemas.chat import MessageOut


class ChatUseCase:
    def __init__(
        self,
        chat_repo: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ):
        self._chat_repo = chat_repo
        self._openrouter_client = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        # Сохраняем сообщение пользователя
        await self._chat_repo.add_message(user_id, "user", prompt)

        # Формируем контекст
        messages: List[Dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})

        # Загружаем историю
        if max_history > 0:
            history = await self._chat_repo.get_recent_by_user(user_id, max_history)
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})

        # Добавляем текущий промпт (он уже сохранён, но в истории он будет последним)
        # Для избежания дублирования, можно добавить только если его нет в истории.
        # Но поскольку мы сохранили промпт, а затем загрузили историю с лимитом,
        # возможно, он уже есть. Упростим: добавим промпт отдельно в конец.
        # Лучше: после сохранения, при формировании контекста, мы можем не включать его,
        # если он уже есть в истории (но он будет включён, т.к. мы загрузили последние сообщения).
        # Чтобы не дублировать, просто не добавляем отдельно, т.к. история уже содержит его.
        # Однако, если max_history=0, то история не загружается, тогда нужно добавить вручную.
        if max_history == 0:
            messages.append({"role": "user", "content": prompt})

        # Вызываем OpenRouter
        answer = await self._openrouter_client.ask(messages, temperature=temperature)

        # Сохраняем ответ ассистента
        await self._chat_repo.add_message(user_id, "assistant", answer)

        return answer

    async def get_history(self, user_id: int, limit: int = 50) -> List[MessageOut]:
        messages = await self._chat_repo.get_recent_by_user(user_id, limit)
        return [MessageOut.model_validate(m) for m in messages]

    async def clear_history(self, user_id: int) -> None:
        await self._chat_repo.clear_history(user_id)