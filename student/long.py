import os
import threading
import socket
import numpy as np
from termcolor import cprint, colored as c

"""
Part of this code is literally from the slides
"""

HOST, PORT = "localhost", 9999
balance = 0.0


class Long():
    def __init__(self):
        self.lock = threading.Lock()
        self.__balance = 0.0
        self.__current_price = None
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((HOST, PORT))
        self.__prev_ma = 0.0
        self.__increase = 0
        self.__ma_list = []
        self.__is_buy = False
        self.__ma_period = 10

    def send(self):
        try:
            # TODO: UPDATE the balance equation here, if buy then -1 else 1 * the self.__current_price
            # TODO: THEN send current side
            if self.__current_price is None:
                pass
            else:
                with self.lock:
                    side = 'BUY' if self.__is_buy else 'SELL'
                    self.__sock.send(side.encode())
                    self.__balance += (-1 if self.__is_buy else 1) * self.__current_price
                    cprint(c('Mr Long', 'yellow') + ' sent side ' + c('{}'.format(side), 'grey'))

                    if not self.__is_buy:
                        cprint(c('Mr Long', 'yellow') + ' current balance: ' + c("{}".format(self.__balance), 'blue'))
                    # else:
                    #     cprint(c('Mr Long', 'yellow') + ' current balance: ' + c("{}".format(self.__balance), 'cyan'))

        except Exception as error:
            print("Issue with Mr. Long Error:{}".format(error))

    def _buy(self):
        self.__is_buy = True
        self.send()

    def _sell(self):
        self.__is_buy = False
        self.send()

    def receive(self):
        while True:
            try:
                # TODO: GRAB PRICE FROM THE SOCKET and save in variable price
                # TODO: convert string price to float and pass in the variable price and self.__ma_period
                price = float(self.__sock.recv(1024).decode())
                cprint(c('Mr Long', 'yellow') + ' got price ' + c('{}'.format(price), 'grey'))
                # TODO: to the moving_average function, make sure to assign a variable to the moving average that is returned

                self.__ma_list.append(price)
                ma = self.moving_average(self.__ma_list, self.__ma_period)
                if self.__is_buy and self.__current_price is not None and price < self.__current_price:
                    # TODO: call send function and send a sell
                    # TODO: make sure to sent self.__is_buy to False
                    self.__current_price = price
                    self._sell()
                elif not self.__is_buy:
                    # TODO: the moving average variable you have pass it in with the price to check_increase
                    self.check_increase(ma, price)

            except Exception as error:
                print("LONG Receive Error: {0}".format(error))
                break
        print("LONG BALANCE: {}".format(balance))

    def moving_average(self, ne, n):
        ma = None
        # TODO: create the moving average function
        length = len(ne)
        if length < n:
            pass
        else:
            ma = np.sum(ne[-10:], dtype=float) / n
        return ma

    def check_increase(self, ma, price):
        global balance
        if ma:
            # TODO: write code that check if there is an increase in the ma average
            # TODO:self.__prev_ma hold the previous moving average, so you can compare to the moving average
            # TODO:current moving average is store in the variable ma
            # TODO:if there is an increase then have self.__increase increase by 1
            # TODO:Then set the prev_ma variable to be ma
            # TODO:else if there is a decrease reset self.__increase variable to 0 and set prev_ma to ma
            if self.__prev_ma < ma:
                self.__increase += 1
            else:
                self.__increase = 0
                self.__prev_ma = ma
            # This is finished for you here
            if self.__increase == 3:
                self.__prev_ma = 0.0
                self.__increase = 0
                self.__current_price = price
                self._buy()
