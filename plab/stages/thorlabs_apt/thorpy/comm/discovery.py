def discover_stages():
    import usb
    from .port import Port
    from serial.tools.list_ports import comports
    import platform

    serial_ports = [
        (x[0], x[1], dict(y.split("=", 1) for y in x[2].split(" ") if "=" in y))
        for x in comports()
    ]

    for dev in usb.core.find(find_all=True, custom_match=lambda x: x.bDeviceClass != 9):
        try:
            # FIXME: this avoids an error related to https://github.com/walac/pyusb/issues/139
            # FIXME: this could maybe be solved in a better way?
            dev._langids = (1033,)
            # KDC101 3-port is recognized as FTDI in newer kernels
            if dev.manufacturer not in ["Thorlabs", "FTDI"]:
                continue
        except usb.core.USBError:
            continue

        if platform.system() == "Linux":
            port_candidates = [
                x[0] for x in serial_ports if x[2].get("SER", None) == dev.serial_number
            ]
        else:
            raise NotImplementedError(
                "Implement for platform.system()=={0}".format(platform.system())
            )

        assert len(port_candidates) == 1

        port = port_candidates[0]

        p = Port.create(port, dev.serial_number)
        yield from p.get_stages().values()


if __name__ == "__main__":
    print(list(discover_stages()))


# iManufacturer           1 Thorlabs
#    iProduct                2 APT DC Motor Controller
#    iSerial                 3 83856536
