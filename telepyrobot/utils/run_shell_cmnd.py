import asyncio
from typing import List


async def run_command(shell_command: List) -> (str, str):
    process = await asyncio.create_subprocess_exec(
        *shell_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return t_response, e_response
