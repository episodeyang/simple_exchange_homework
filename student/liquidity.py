import socket
import time
import threading
import numpy as np
from termcolor import cprint, colored as c

SENT_BYTES = 1024
INTERVAL = 0.05

"""
Part of this code is literally from the slides
"""
HOST, PORT = "localhost", 9998


class Liquidity:
    def __init__(self):
        self.lock = threading.Lock()
        # TODO: call the random seed of 12345 of numpy
        np.random.seed(12345)

        # TODO: create a variable called self.__list_prices that calls the np.random that Sebastien mentioned
        self.__list_prices = list(np.random.uniform(low=12.5, high=14.5, size=(500,)))

        self.__balance = 0.0
        self.__cp = 0.0
        # TODO: Create a socket connection called self.__sock
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: call connect for HOST and PORT
        self.__sock.connect((HOST, PORT))

    def send(self):
        try:
            # TODO: Create a for loop that iterates through the prices in self.__list_prices
            for price in self.__list_prices:
                # TODO: call the sendall function of self.__sock and send the price
                self.__sock.sendall(str(price).encode())
                cprint(c('Sir Liquidity', 'green') + ' sent price ' + c('{}'.format(price), 'grey'))

                # TODO sent self.__cp to the price you just sent to keep track of the current price
                self.__cp = price

                # TODO: call sleep for the time asked in the pdf of the assignment
                time.sleep(INTERVAL)
            pass
        except Exception as error:
            cprint(c("Issue with Sir Liquidity Error:{}".format(error), 'red'))

        cprint(c("Sent all prices, Closing........", 'green'))

    def _execute(self, buy):
        with self.lock:
            self.__balance += (-1 if buy else 1) * self.__cp
            if buy:
                cprint(c('Sir Liquidity', 'green') + ' current balance: ' + c('{}'.format(self.__balance), 'blue'))
            # else:
            #     cprint(c('Sir Liquidity', 'green') + ' current balance: ' + c("{}".format(self.__balance), 'cyan'))

    def receive(self):
        while True:
            try:
                received = self.__sock.recv(SENT_BYTES).decode().strip().lower()
                if received:
                    # TODO: If data is received, Keep track of the balance for Sir Liquidity here
                    # TODO: Then set receive to None
                    # TODO: print the current balance of sir liquidity
                    if received == 'buy':
                        self._execute(buy=False)
                    elif received == 'sell':
                        self._execute(buy=True)
                    pass

            except Exception as error:
                print("Receive Error: {0}".format(error))
                break
        print("FINAL LIQUIDITY BALANCE: {}".format(self.__balance))
