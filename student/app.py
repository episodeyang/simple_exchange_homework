#!/usr/bin/env python3

import threading
import exchange
import liquidity
import long
import socketserver

# disable the TCP Port timeout.
socketserver.TCPServer.allow_reuse_address = True

def main():
    HOST_LONG, PORT_LONG = "localhost", 9999
    HOST_LIQUIDITY, PORT_LIQUIDITY = "localhost", 9998
    exchg = socketserver.TCPServer((HOST_LONG, PORT_LONG), exchange.ExchangeSend)
    exchg_thread = threading.Thread(target=exchg.serve_forever)
    exchg_thread.start()

    # TODO: Create a TCP Connection for SIR LIQUIDITY calling the exchange's ExchangeReceiver, call the variable sirliq
    # TODO Create a thread for the TCPServer you called sirliq and call the serve_forever command as your target, call the variable liq_thread
    # TODO: Call start function for liq_thread
    # TODO: Create a variable call mrlong that calls the Long class
    # TODO: Create a variable receiving that create a thread whose target calls variable's mrlong's receive function
    # TODO: Call start function for receiving variable

    sirliq = socketserver.TCPServer((HOST_LIQUIDITY, PORT_LIQUIDITY), exchange.ExchangeReceiver)
    liq_thread = threading.Thread(target=sirliq.serve_forever)
    liq_thread.start()

    mrlong = long.Long()
    mrlong_sending = threading.Thread(target=mrlong.send)
    mrlong_receiving = threading.Thread(target=mrlong.receive)
    mrlong_sending.start()
    mrlong_receiving.start()

    liq = liquidity.Liquidity()
    liq_sending = threading.Thread(target=liq.send)
    liq_receive = threading.Thread(target=liq.receive)
    liq_sending.start()
    liq_receive.start()


if __name__ == "__main__":
    main()
