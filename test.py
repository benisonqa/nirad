# mylist = ['H/W path            Device      Class       Description', '=======================================================', '                                system      VirtualBox', '/0                              bus         VirtualBox', '/0/0                            memory      128KiB BIOS', '/0/1                            memory      5GiB System memory', '/0/2                            processor   Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz', '/0/100                          bridge      440FX - 82441FX PMC [Natoma]', '/0/100/1                        bridge      82371SB PIIX3 ISA [Natoma/Triton II]', '/0/100/1.1          scsi1       storage     82371AB/EB/MB PIIX4 IDE', '/0/100/1.1/0.0.0    /dev/cdrom  disk        CD-ROM', '/0/100/1.1/0.0.0/0  /dev/cdrom  disk        ', '/0/100/2                        display     SVGA II Adapter', '/0/100/3            enp0s3      network     82540EM Gigabit Ethernet Controller', '/0/100/4                        generic     VirtualBox Guest Service', "/0/100/5                        multimedia  82801AA AC'97 Audio Controller", '/0/100/6                        bus         KeyLargo/Intrepid USB', '/0/100/6/1          usb2        bus         OHCI PCI host controller', '/0/100/7                        bridge      82371AB/EB/MB PIIX4 ACPI', '/0/100/b                        bus         82801FB/FBM/FR/FW/FRW (ICH6 Family) USB2 EHCI Controller', '/0/100/b/1          usb1        bus         EHCI Host Controller', '/0/100/d            scsi2       storage     82801HM/HEM (ICH8M/ICH8M-E) SATA Controller [AHCI mode]', '/0/100/d/0.0.0      /dev/sda    disk        26GB VBOX HARDDISK', '/0/100/d/0.0.0/1                volume      1GiB Linux filesystem partition', '/0/100/d/0.0.0/2    /dev/sda2   volume      7725MiB Linux LVM Physical Volume partition', '/0/100/d/0.0.0/3    /dev/sda3   volume      16GiB Linux LVM Physical Volume partition', '/0/3                            input       PnP device PNP0303', '/0/4                            input       PnP device PNP0f03', '/1                  virbr0-nic  network     Ethernet interface', '/2                  virbr0      network     Ethernet interface', '/3                  docker0     network     Ethernet interface']

# for data in mylist:
#     print(data)



class Node:
    def __init__(self, data):
        self.data = data
        self.next = None



