import protector
import argparse
import asyncio
import websockets


def check_protector():
    hash_string = protector.get_hash_str()
    skey_initial = protector.get_session_key()
    protector1 = protector.Session_protector(hash_string)
    protector2 = protector.Session_protector(hash_string)
    #stage 0
    skey1 = protector1.next_session_key(skey_initial)
    skey2 = protector2.next_session_key(skey_initial)
    assert skey1 == skey2
    #stage 1 - each protector use it's own skey and compare with another's side
    skey3 = protector1.next_session_key(skey1)
    skey4 = protector2.next_session_key(skey2)
    assert skey3 == skey4
    #stage 2
    skey5 = protector1.next_session_key(skey3)
    skey6 = protector2.next_session_key(skey4)
    assert skey5 == skey6
    print (skey1, skey2, skey3, skey4, skey5, skey6)


def parse_args():
    parser = argparse.ArgumentParser(description="Protected chat")
    parser.add_argument("ip_port", type=str, help="IP address & port for client mode, port only for server mode")
    parser.add_argument("-n", type=int, default=100, help="Number of simultaneous connections")

    options = parser.parse_args()
    options = vars(options)

    ip_port = options['ip_port']
    connections = options['n']
    connections = int(connections)

    ip = None
    port = None

    try:
        if ':' in ip_port:
            ip_port = ip_port.split(':')
            ip = int(ip_port[0])
            port = int(ip_port[1])
            connections = None
        else:
            port = int(ip_port)
    except Exception as e:
        print(e)

    return (ip, port, connections)


async def helloServer(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")


def server():
    start_server = websockets.serve(helloServer, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


async def helloClient():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


def client():
    asyncio.get_event_loop().run_until_complete(helloClient())


if __name__ == "__main__":
    #check_protector()
    (ip, port, connections) = parse_args()
    print(ip)
    print(port)
    print(connections)

    if ip:
        print("Client Mode")
        client()
    else:
        print("Server Mode")
        server()

    # print("Starting wsgiref server")
    # with make_server('', 8000, file_server) as httpd:
    #     print("Serving on port 8000...")
    #     try:
    #         httpd.serve_forever()
    #     except KeyboardInterrupt:
    #         print("Stop serving")
    #     except Exception as e:
    #         print(str(e))
