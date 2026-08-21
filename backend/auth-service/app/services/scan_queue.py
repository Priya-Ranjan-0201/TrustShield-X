import uuid
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ScanQueueTask:
    def __init__(
        self,
        task_id: str,
        scan_id: uuid.UUID,
        scan_type: str,
        priority: int = 5,
        payload: Optional[Dict[str, Any]] = None,
    ):
        self.task_id = task_id
        self.scan_id = scan_id
        self.scan_type = scan_type
        self.priority = priority
        self.payload = payload or {}
        self.status = "QUEUED"
        self.retries = 0


class BaseScanQueue(ABC):
    @abstractmethod
    async def enqueue(
        self, scan_id: uuid.UUID, scan_type: str, priority: int = 5, payload: Optional[Dict[str, Any]] = None
    ) -> str:
        pass

    @abstractmethod
    async def dequeue() -> Optional[ScanQueueTask]:
        pass

    @abstractmethod
    async def get_task_status(self, task_id: str) -> Optional[str]:
        pass

    @abstractmethod
    async def cancel_task(self, task_id: str) -> bool:
        pass


class MemoryScanQueue(BaseScanQueue):
    def __init__(self):
        self._queue: asyncio.Queue[ScanQueueTask] = asyncio.Queue()
        self._tasks: Dict[str, ScanQueueTask] = {}

    async def enqueue(
        self, scan_id: uuid.UUID, scan_type: str, priority: int = 5, payload: Optional[Dict[str, Any]] = None
    ) -> str:
        task_id = f"task-{uuid.uuid4()}"
        task = ScanQueueTask(
            task_id=task_id,
            scan_id=scan_id,
            scan_type=scan_type,
            priority=priority,
            payload=payload,
        )
        self._tasks[task_id] = task
        await self._queue.put(task)
        return task_id

    async def dequeue() -> Optional[ScanQueueTask]:
        try:
            task = self._queue.get_nowait()
            task.status = "PROCESSING"
            return task
        except asyncio.QueueEmpty:
            return None

    async def get_task_status(self, task_id: str) -> Optional[str]:
        task = self._tasks.get(task_id)
        return task.status if task else None

    async def cancel_task(self, task_id: str) -> bool:
        task = self._tasks.get(task_id)
        if task and task.status == "QUEUED":
            task.status = "CANCELLED"
            return True
        return False
