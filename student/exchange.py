import socketserver
import threading
import time
import select
from termcolor import cprint, colored as c

"""
This code is literally from Piazza, it just needs a few modification to send and recieve correctly
"""
SR_BYTES = 1024
POLL_TIMEOUT = 0.0000

current_price = None
side_to_send = None

# For some more assistance, please look at this link
# https://www.technovelty.org/python/python-socketserver-class.html

# this is a module level global.
mutex_lock = threading.Lock()


class ExchangeReceiver(socketserver.BaseRequestHandler):
    """This Class Will interface with Sir Liquidity
         from Sir Liquidity: ['BUY', 'SELL']
         to Mr Long via threading event: prices
    """

    def handle(self):
        while True:
            global current_price
            global side_to_send
            global mutex_lock
            # TODO: You will have to implement a select like in the URL example
            # To check whether we need to recv or send data.
            # if we are receiving data it will be price data.
            # if we are sending data it will be the side data.
            # recall that you will have to cast from str to float for your price
            try:
                if side_to_send is not None:
                    cprint(c('Exchange ', 'grey') + '=> ' + c('Sir Liquidity', "green"))
                    self.request.send(side_to_send.encode())
                    side_to_send = None
                elif current_price is None:
                    # make sure timeout=0, so that it is not blocking
                    ready_to_read, ready_to_write, in_error = select.select([self.request], [], [], POLL_TIMEOUT)
                    if len(ready_to_read) == 1 and ready_to_read[0] == self.request:
                        current_price = float(self.request.recv(SR_BYTES).decode())
                        cprint(c('Exchange', 'grey') + ' got price from ' + c('Sir Liquidity ', 'green') + c("{}".format(current_price), 'grey'))
                    if len(ready_to_write) == 1 and ready_to_write[0] == self.request:
                        cprint('ready to write', 'red')

            except Exception as error:
                cprint("Issue with Exchange Receive Error:{}".format(error), 'red')
                break
            finally:
                pass


class ExchangeSend(socketserver.BaseRequestHandler):
    """This Class Will interface with Mr Long
         from Mr Long: ['BUY', 'SELL']
         to Sir Liquidity via threading event: prices
    """

    def handle(self):
        while True:
            global current_price
            global side_to_send
            global mutex_lock
            # TODO: You will have to implement a select like in the URL example
            # To check whether we need to recv or send data
            # Here you will do the opposite, receiving data will be the side
            # sending data will be the price
            # recall that you will have to cast from str to float for your price

            try:
                if current_price is not None:
                    cprint(c('Exchange ', 'grey') + '=> ' + c('Mr Long', "yellow"))
                    self.request.send(str(current_price).encode())
                    current_price = None
                elif side_to_send is None:
                    ready_to_read, ready_to_write, in_error = select.select([self.request], [], [], POLL_TIMEOUT)
                    if len(ready_to_read) == 1 and ready_to_read[0] == self.request:
                        side_to_send = self.request.recv(SR_BYTES).decode()
                        cprint('getting stuff from ' + c('Mr Long', 'yellow') + '. Side to send: {}'.format(side_to_send), 'grey')

            except Exception as error:
                cprint("Issue with Exchange Send Error:{}".format(error), 'red')
                break
            finally:
                pass
