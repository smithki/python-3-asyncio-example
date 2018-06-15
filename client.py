# Client application

import socket
import asyncio
import concurrent.futures
import numbers
import threading
import queue

def prompt_for_throttle():
  while True:
    throttle = input("How many requests should be sent per second, concurrently?\n")
    q.put(int(throttle))

# async def send_requests():
#   while True:
#     if not q.empty():
#       req_per_sec = q.get()
#     await asyncio.sleep(1 / req_per_sec)
#     ws.send("hello world".encode("utf8"))

async def send_requests():
  req_per_sec = 0

  while True:
    if not q.empty():
      req_per_sec = q.get()
    await asyncio.sleep(1)
    if req_per_sec > 0:
      with concurrent.futures.ThreadPoolExecutor(max_workers=req_per_sec) as executor:
        futures = [
          loop.run_in_executor(
            executor,
            ws.send,
            "hello world".encode('utf8')
          )
          for i in range(req_per_sec)
        ]

# Connect to the socket server
ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ws.connect(("localhost", 8888))

# Queue for sending user input between threads
q = queue.Queue()

# Thread for capturing user input
threading.Thread(target = prompt_for_throttle).start()

# Start sending requests
asyncio.ensure_future(send_requests())

# Execute the async event loop
loop = asyncio.get_event_loop()
loop.run_forever()
