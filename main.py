from network import NetworkLayer
from receiver import ReceiverProcess
from sender import SenderProcess, RDTSender
import sys
import random


def stress_test(number_of_tests):
    count = 0
    for i in range(number_of_tests):
        msg = "TEST"
        rel = random.uniform(0.1, 1)
        SenderProcess.set_outgoing_data(msg)

        network_serv = NetworkLayer(reliability=rel, delay=0, pkt_corrupt=True, ack_corrupt=True)

        rdt_sender = RDTSender(network_serv)
        rdt_sender.rdt_send(SenderProcess.get_outgoing_data())
        if("".join(ReceiverProcess.get_buffer()) != msg):
            print("=======> " ,ReceiverProcess.get_buffer())
            count += 1
        ReceiverProcess.get_buffer().clear()
    print(count)


if __name__ == '__main__':
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    print(args)
    msg = args['msg']
    prob_to_deliver = float(args['rel'])
    delay = int(args['delay'])
    debug = bool(int(args['debug']))
    corrupt_pkt = True
    corrupt_ack = True
    if debug:
        corrupt_pkt = bool(int(args['pkt']))
        corrupt_ack = bool(int(args['ack']))

    SenderProcess.set_outgoing_data(msg)

    print(f'Sender is sending:{SenderProcess.get_outgoing_data()}')

    network_serv = NetworkLayer(reliability=prob_to_deliver, delay=delay, pkt_corrupt=corrupt_pkt,
                                ack_corrupt=corrupt_ack)

    rdt_sender = RDTSender(network_serv)
    rdt_sender.rdt_send(SenderProcess.get_outgoing_data())

    print(f'Receiver received: {ReceiverProcess.get_buffer()}')

