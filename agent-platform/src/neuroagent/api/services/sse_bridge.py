"""Thread-safe bridge between a sync worker thread and an SSE async generator.

The agent/evaluator run synchronously inside ``loop.run_in_executor``. Calling
``asyncio.Queue.put_nowait`` directly from that worker thread is not
thread-safe — the queue may wake waiters on the wrong thread or corrupt its
internal state. This bridge marshals every put through
``loop.call_soon_threadsafe`` so the queue is only ever touched on the event
loop thread.

It also handles client disconnects: once :meth:`mark_disconnected` is set
(automatically when the async consumer is closed early), the worker's events
are discarded instead of buffered, so an abandoned run cannot grow the queue
without bound. The worker itself keeps running to completion — cancelling it
requires orchestrator cooperation, which we deliberately do not attempt.
"""

from __future__ import annotations

import asyncio
import logging
import threading
from typing import AsyncIterator

logger = logging.getLogger(__name__)

DEFAULT_MAXSIZE = 2048


class SSEBridge:
    """Bounded, thread-safe handoff of event dicts to the event loop.

    Must be constructed on the event loop thread (it captures the running
    loop). The worker thread calls :meth:`put_from_thread` with each event and
    finally with ``None`` as the completion sentinel; the async side iterates
    :meth:`events`.
    """

    def __init__(self, maxsize: int = DEFAULT_MAXSIZE) -> None:
        self._queue: asyncio.Queue[dict | None] = asyncio.Queue(maxsize=maxsize)
        self._loop = asyncio.get_running_loop()
        self._disconnected = threading.Event()

    @property
    def client_disconnected(self) -> bool:
        return self._disconnected.is_set()

    def mark_disconnected(self) -> None:
        """Stop buffering worker events (client is gone)."""
        self._disconnected.set()

    def put_from_thread(self, event: dict | None) -> None:
        """Enqueue an event from the worker thread; never blocks the loop.

        After a disconnect, non-sentinel events are silently discarded. If the
        queue is full, the event is dropped with a warning; the sentinel is
        never dropped (the oldest queued event is evicted instead).
        """
        if self._disconnected.is_set() and event is not None:
            return
        try:
            self._loop.call_soon_threadsafe(self._put_on_loop, event)
        except RuntimeError:
            # Event loop already closed (server shutdown) — nothing to deliver.
            pass

    def _put_on_loop(self, event: dict | None) -> None:
        """Runs on the event loop thread, where put_nowait is safe."""
        try:
            self._queue.put_nowait(event)
        except asyncio.QueueFull:
            if event is None:
                # Never lose the completion sentinel: evict the oldest event.
                try:
                    self._queue.get_nowait()
                except asyncio.QueueEmpty:  # pragma: no cover — full implies non-empty
                    pass
                self._queue.put_nowait(event)
            else:
                logger.warning(
                    "SSE bridge queue full — dropping %r event",
                    event.get("type", "unknown"),
                )

    async def events(self) -> AsyncIterator[dict]:
        """Yield events until the sentinel arrives.

        If the consumer is closed early (SSE client disconnected), the bridge
        is marked disconnected so the worker stops buffering.
        """
        completed = False
        try:
            while True:
                event = await self._queue.get()
                if event is None:
                    break
                yield event
            completed = True
        finally:
            if not completed:
                self.mark_disconnected()
