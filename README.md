# Python3/ayncio Code Exercise

This is an example using Python3 and asyncio to do the following:

1. Run a service that tracks of how many WebSocket requests per second it is receiving.
2. Run a client that can throttle the number of WebSocket messages per second it sends concurrently.

This could also be implemented using the popular [Requests](http://docs.python-requests.org/en/master/) library.

## Running the example

1. Open a terminal to the working directory
2. Run `python3 server.py`
3. Run `python3 client.py`
