from __future__ import annotations

import asyncio
import logging
import os
import signal
from datetime import datetime
from typing import Optional, Set


PORT = int(os.environ.get("PORT", "4444"))
MAX_SESSIONS = int(os.environ.get("MAX_SESSIONS", "20"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )


class BashaServer:
    def __init__(self, host: str = "0.0.0.0", port: int = PORT):
        self.host = host
        self.port = port
        self.server: Optional[asyncio.base_events.Server] = None
        self.active_sessions: Set[asyncio.Task] = set()

    async def start(self):
        self.server = await asyncio.start_server(
            self._handle_client, self.host, self.port
        )
        addrs = ", ".join(str(sock.getsockname()) for sock in self.server.sockets or [])
        logging.info(f"listening on {addrs}")
        async with self.server:
            await self.server.serve_forever()

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        peer = writer.get_extra_info("peername")
        ip_port = f"{peer[0]}:{peer[1]}" if peer else "unknown"
        logging.info(f"connection from {ip_port}")

        # Backpressure on max sessions
        if len(self.active_sessions) >= MAX_SESSIONS:
            try:
                writer.write(b"basha is busy right now. try again later.\n")
                await writer.drain()
            finally:
                writer.close()
                await writer.wait_closed()
            logging.warning("refused connection: max sessions reached")
            return

        task = asyncio.create_task(self._run_script_session(reader, writer, ip_port))
        self.active_sessions.add(task)
        task.add_done_callback(self.active_sessions.discard)

    async def _run_script_session(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, ip_port: str
    ):
        start = datetime.now()
        proc = None
        try:
            # Launch the legacy BASHA/script.py as a subprocess
            script_path = os.path.join(os.path.dirname(__file__), ".", "script.py")
            proc = await asyncio.create_subprocess_exec(
                "python3",
                script_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            async def tcp_to_proc():
                try:
                    while True:
                        data = await reader.read(1024)
                        if not data:
                            break
                        # Forward Ctrl+C (0x03) as SIGINT to the child so its handler runs
                        if b"\x03" in data and proc is not None:
                            proc.send_signal(signal.SIGINT)
                            # Remove the byte before forwarding remaining input
                            data = data.replace(b"\x03", b"")
                            if not data:
                                continue
                        if proc and proc.stdin:
                            proc.stdin.write(data)
                            await proc.stdin.drain()
                except Exception:
                    pass
                finally:
                    # EOF to child stdin
                    if proc and proc.stdin:
                        try:
                            proc.stdin.close()
                        except Exception:
                            pass

            async def proc_to_tcp():
                try:
                    assert proc is not None and proc.stdout is not None
                    while True:
                        chunk = await proc.stdout.read(1024)
                        if not chunk:
                            break
                        writer.write(chunk)
                        await writer.drain()
                except Exception:
                    pass

            t1 = asyncio.create_task(tcp_to_proc())
            t2 = asyncio.create_task(proc_to_tcp())
            await asyncio.wait({t1, t2}, return_when=asyncio.FIRST_COMPLETED)

            # Ensure process exits
            if proc and proc.returncode is None:
                try:
                    proc.terminate()
                except ProcessLookupError:
                    pass
                try:
                    await asyncio.wait_for(proc.wait(), timeout=2)
                except asyncio.TimeoutError:
                    try:
                        proc.kill()
                    except ProcessLookupError:
                        pass
                    await proc.wait()
        except Exception as e:
            logging.exception(f"session error ({ip_port}): {e}")
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            dur = (datetime.now() - start).total_seconds()
            logging.info(f"session end {ip_port} duration={dur:.1f}s")


async def main():
    setup_logging()
    srv = BashaServer()
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda s=sig: asyncio.create_task(_shutdown(loop, s))
        )
    await srv.start()


async def _shutdown(loop: asyncio.AbstractEventLoop, sig: signal.Signals):
    logging.info(f"received signal {sig.name}, shutting down...")
    tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task()]
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
