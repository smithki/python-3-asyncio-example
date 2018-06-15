# Server application

import asyncio
import time

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

start_time = time.time()
total_requests = 0
requests_last_second = 0
first_count = True

async def count_requests():
  global total_requests
  global requests_last_second
  global start_time
  global first_count
  while True:
    await asyncio.sleep(1)
    time_elapsed = time.time() - start_time
    if not first_count:
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE + ERASE_LINE, end = "")
    print("Total requests:               {0}".format(total_requests))
    print("Total requests last second:   {0}".format(requests_last_second))
    print("Average requests per second:  {0}".format(round(total_requests / time_elapsed, 2)))
    requests_last_second = 0
    if first_count:
      first_count = False

def handle_request(connection):
  global total_requests
  global requests_last_second
  buffer = connection.recv(4096)
  if len(buffer) > 0:
    total_requests += 1
    requests_last_second += 1

async def start_server():
  import socket
  ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ws.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  print("Socket created")

  try:
    ws.bind(("localhost", 8888))
    print("Socket bind complete")
  except socket.error as msg:
    import sys
    print("Socket binding failed. Error : " + str(sys.exc_info()))
    sys.exit()

  # Listen on the socket
  ws.listen(10)
  print("Socket listening\n")

  # Accept the client
  connection, address = ws.accept()
  ip, port = str(address[0]), str(address[1])
  print("Client connected from " + ip + ":" + port, end = "\n\n")


  while True:
    await asyncio.sleep(0)
    handle_request(connection)

# Execute async functions
asyncio.ensure_future(count_requests())
asyncio.ensure_future(start_server())

loop = asyncio.get_event_loop()
loop.run_forever()
