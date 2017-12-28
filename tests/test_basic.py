from comonitor import Monitor


def test_enumerate_serial_ports():
    assert isinstance(Monitor.enumerate_serial_ports(), list)
