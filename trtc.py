from myhdl import *
import random


class Color:
    green = 0
    yellow = 1
    red = 2

colors = ["green", "yellow", "red"]
pkt_size= []
result = []


def trtc_test():
    pir = 1000
    cir = 700
    pbs = 1400
    cbs = 1100
    tp = Signal(pbs)
    tc = Signal(cbs)
    color = Signal(0)
    clk_meter = Signal(bool(0))
    clk_update = Signal(bool(0))
    size = Signal(random.randint(64, 1518))
    # trtc_inst = trtc(size, tp, tc, color, clk_meter)

    @always(delay(100))
    def clk_update_gen():
        clk_update.next = not clk_update
        print "clk_update_gen %d" % clk_update.next

    @always(delay(10))
    def clk_meter_gen():
        clk_meter.next = not clk_meter
        print "clk_meter_gen %d" % clk_meter.next

    @always(clk_update.posedge)
    def update_tp():
        print "update_tp"
        if (tp + pir) > pbs:
            tp.next = pbs
        else:
            tp.next += pir
        print "tp: %d" % tp.next

    @always(clk_update.posedge)
    def update_tc():
        print "update_tc"
        if (tc + cir) > cbs:
            tc.next = cbs
        else:
            tc.next += cir
        print "tc: %d" % tc.next

    @always(clk_meter.negedge)
    def stimulus():
        print "stimulus"
        size.next = random.randint(64 - 12, 555 - 12)
        print "size: %d" % size.next
        pkt_size.append(size.next)

    @always(clk_meter.posedge)
    def meter():
        print "=enter meter======"
        print "size: %d" % size
        print "tp: %d" % tp
        print "tc: %d" % tc
        if (tp - size) < 0:
            color.next = 2
        elif (tc - size) < 0:
            tp.next = tp - size
            color.next = 1
        else:
            tp.next = (tp - size)
            tc.next = (tc - size)
            color.next = 0

        print "=exit trtc======="
        print "tp: %d" % tp.next
        print "tc: %d" % tc.next
        print "color: %s" % colors[color.next]
        result.append(colors[color.next])

    return clk_update_gen, clk_meter_gen,  update_tp, update_tc, \
        stimulus, meter


def simulate(timesteps):
    testb = traceSignals(trtc_test)
    sim = Simulation(testb)
    sim.run(timesteps)


def main():
    simulate(500)
    print "config:"
    print "\tpir = 1000"
    print "\tcir = 700"
    print "\tpbs = 1400"
    print "\tcbs = 1100"
    print "result:"
    for _result, _pkt_size in zip(result, pkt_size):
        print "\tpkt size: " + str(_pkt_size) + "\tcolor: " + _result


if __name__ == '__main__':
    main()
