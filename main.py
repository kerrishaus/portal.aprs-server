#!/usr/bin/env python

import asyncio
from websockets.asyncio.server import serve

def runDirewolf(text, voice):
    program = subprocess.Popen(
        [
            "ffplay",
            "-hide_banner",
            "-loglevel", "error",
            "-f", "s16le",
            "-ar", str(voice.config.sample_rate),
            "-nodisp",
            "-infbuf",
            "-autoexit",
            "-af", f"volume={flags.voiceVolume}",
            # can't use atempo because it exits too early and cuts off the last phonem.
            # instead, we use piper's length_scale to change voice speed.
            "-i", "pipe:"
        ],
        stdout=sys.stdout,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE
    )
    
    for byteData in voice.synthesize_stream_raw(text):
        program.stdin.write(byteData)
    
    program.stdin.close()
    program.wait()

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765) as server:
        await server.serve_forever()

asyncio.run(main())
