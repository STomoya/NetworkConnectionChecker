
import logging
import time
import socket

import requests

try:
    from line_token import LINE_TOKEN
except ImportError:
    LINE_TOKEN = None

class NetworkChecker:
    '''
    Network Connection Status Checker class

    checks if the network is connectable to the Internet

    args
        connect_interval : Int [sec] required
            interval between each try
        play : Int [] required
            a specific status (i.e. True, False) must continue for 'play' times to switch
        send_message : Bool [] (True)
            if True, and there is a file named line_token.py with the variable 'LINE_TOKEN'
            this class will send a message using LINE Notify (https://notify-bot.line.me/ja/)
        host : String [] ('8.8.8.8')
            the IP adress of the host.
            default is '8.8.8.8' (Google Public DNS)
        port : Int [] (53)
            the port to try connect on.
            default is 53 (TCP)
        timeout : Int [sec] (1)
            timeout of the connection
    '''
    def __init__(self,
            connect_interval,
            play,
            send_message=True,
            host='8.8.8.8',
            port=53,
            timeout=1
        ):

        self.connect_interval = connect_interval
        self.play = play
        self.send_message = send_message

        self.host = host
        self.port = port
        self.timeout = timeout

        self.stat_queue = []
        self.current_stat = True

        formatter = '%(levelname)s : %(asctime)s : %(message)s'
        logging.basicConfig(format=formatter)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def is_connectable(self):
        '''
        Check if the port of the host is reachable and return status
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)

        try:
            s.connect((self.host, self.port))
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            return True
        except socket.error as se:
            s.close()
            return False

    def send_line_message(self):
        '''
        send message by LINE Notify
        ignored when no 'line_token.py' with the 'LINE_TOKEN' variable
        '''
        message = 'The network is now connectable'

        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": "Bearer " + LINE_TOKEN}
        payload = {"message": message}
        requests.post(url, headers=headers, data=payload)

    def run(self):
        '''
        main flow

        infinit loop and check if the network is connectable each 'conncet_interval' seconds
        '''

        while True:

            # save status (queue.put())
            self.stat_queue.append(self.is_connectable())
            recent_logs = self.stat_queue[-self.play:]
            value_set = list(set(recent_logs))

            if len(value_set) == 1:                                             # when same status for 'play' times in a row
                if not value_set[0] == self.current_stat:                           # if the status differs
                    self.current_stat = value_set[0]
                    self.logger.info('status switched to {}'.format('True' if self.current_stat else 'False'))
                    if self.current_stat and LINE_TOKEN and self.send_message:          # send message if connection is turned on
                        self.send_line_message()

            # erase first element (queue.get())
            if len(self.stat_queue) >= self.play:
                self.stat_queue = self.stat_queue[1:]

            # sleep for 'connect_interval' seconds
            time.sleep(self.connect_interval)


if __name__ == "__main__":
    NetworkChecker(
        connect_interval=20,
        play=5,
        send_message=True,
        host='8.8.8.8',
        port=53,
        timeout=2
    ).run()