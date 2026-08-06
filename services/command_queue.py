import asyncio
import uuid
from datetime import datetime
from pydantic import BaseModel


class Command(BaseModel):
    id: str = ""
    type: str
    args: dict = {}
    device_id: str = ""
    status: str = "pending"
    created_at: str = ""

    def __init__(self, **data):
        if not data.get("id"):
            data["id"] = f"cmd_{uuid.uuid4().hex[:8]}"
        if not data.get("created_at"):
            data["created_at"] = datetime.utcnow().isoformat()
        super().__init__(**data)


class CommandResult(BaseModel):
    id: str
    status: str
    message: str
    data: dict = {}


class DeviceState:
    def __init__(self):
        self._queues: dict[str, asyncio.Queue] = {}
        self._results: dict[str, CommandResult] = {}
        self._devices: dict[str, dict] = {}

    def register_device(self, device_id: str, device_info: dict):
        if device_id in self._devices:
            self._devices[device_id].update(device_info)
        else:
            self._devices[device_id] = device_info
        if device_id not in self._queues:
            self._queues[device_id] = asyncio.Queue()

    def get_queue(self, device_id: str) -> asyncio.Queue:
        if device_id not in self._queues:
            self._queues[device_id] = asyncio.Queue()
        return self._queues[device_id]

    async def enqueue_command(self, device_id: str, command: Command):
        queue = self.get_queue(device_id)
        await queue.put(command)

    async def wait_for_command(self, device_id: str, timeout: int = 30) -> Command | None:
        queue = self.get_queue(device_id)
        try:
            return await asyncio.wait_for(queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def store_result(self, result: CommandResult):
        self._results[result.id] = result

    def get_result(self, command_id: str) -> CommandResult | None:
        return self._results.pop(command_id, None)

    def get_devices(self) -> dict[str, dict]:
        return self._devices


device_manager = DeviceState()
