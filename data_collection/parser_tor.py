import os
import socket
import requests
import time

import socks
from user_agent import generate_user_agent

import stem.process
from stem import Signal
from stem.control import Controller

# /home/andrey/PycharmProjects/SeekingAlpha_project/

current_time = lambda: int(round(time.time()))

class Network(object):
    def __init__(self):
        # путь к директории файлов браузера Tor. В данном случае, директория для OS X
        TOR_DIR = '/home/andrey/PycharmProjects/SeekingAlpha_project/Tor/tor-browser_ru/Browser/TorBrowser/Data/Tor/'
        PASS_HASH = '16:DEBBA657C88BA8D060A5FDD014BD42DB7B5B736C0C248422F37C46B930'
        IP_ADDRESS = '127.0.0.1'
        self.SOCKS_PORT = 9051

        self.tor_config = {
            'SocksPort': str(self.SOCKS_PORT),
            'ControlPort': str(self.SOCKS_PORT + 1),
            'HashedControlPassword': PASS_HASH,
            'GeoIPFile': os.path.join(TOR_DIR, 'geoip'),
            'GeoIPv6File': os.path.join(TOR_DIR, 'geoip6')
        }

        self.tor_path = os.path.join(TOR_DIR, 'tor')
        # Setup proxy
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, IP_ADDRESS, self.SOCKS_PORT)
        self.nonProxySocket = socket.socket
        self.proxySocket = socks.socksocket

    def switch_ip(self):
        self.controller.signal(Signal.NEWNYM)
        print("Switching IP. Waiting.")
        t = current_time()
        time.sleep(self.controller.get_newnym_wait())
        print("{0}s gone".format(current_time() - t))

    def print_bootstrap_lines(self, line):
        print(line)

    def init_tor(self, password='supersafe', log_handler=None):
        self.tor_process = None
        self.controller = None

        try:
            self.tor_process = stem.process.launch_tor_with_config(
                tor_cmd=self.tor_path,
                config=self.tor_config,
                init_msg_handler=log_handler
            )

            self.controller = Controller.from_port(port=self.SOCKS_PORT + 1)
            self.controller.authenticate(password)

        except:
            if self.tor_process is not None:
                self.tor_process.terminate()
            if self.controller is not None:
                self.controller.close()

            raise RuntimeError('Failed to initialize Tor')

        socket.socket = self.proxySocket

    def kill_tor(self):
        print('Killing Tor process')
        if self.tor_process is not None:
            self.tor_process.kill()

        if self.controller is not None:
            self.controller.close()



network = Network()
network.init_tor('supersafe', network.print_bootstrap_lines)

url = 'http://checkip.amazonaws.com/'
headers = {'User-Agent': generate_user_agent()}

req = requests.get(url, headers=headers)
print(req.content)
network.switch_ip()
req = requests.get(url, headers=headers)
print(req.content)

network.kill_tor()


