## nuberrypi-info

NuBerryPi-info is utily to display statistics on running NuBerryPi.
There are several modes of operation:

> nuberrypi-info

will display general info.

> nuberrypi-info -a or nuberrypi-info --all

will display **all** information.

(Avoid using this output for public showing as it contains some private information.)

> nuberrypi-info --public

will show general information but will hide private data (ip, balance, serial number)
This is great for showing on forums, etc.

> nuberrypi-info -s or nuberrypi-info --system

will display only system diagnostics.

Example output:

    NuBerryPi system info:
    {
    "average load": [
        0.45, 
        0.46, 
        0.48
    ], 
    "kernel release": "3.14.6-3-GRSEC", 
    "nuberrypi": "0.22", 
    "system_temperature": 45.464, 
    "uptime": "22:23:25.540000"
    }

> nuberrypi-info -p or nuberrypi-info --nu

is equal to "nud getinfo"

> nuberrypi-info -o or nuberrypi-info --output

will dump data to stdout. You can use this to pipe data to some other program.

> nuberrypi-info --health

will run diagnostic on blockchain status. It uses peerchain.co as reference.
It is worth to run this once in a while to check if you are on the right chain.
If all is True, you are safe.

Example output:

    last_block_hash_matches:True
    merkle_root_matches:True
    block_count_matches:True
    previous_block_hash_matches:True

