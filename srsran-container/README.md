The configurations and the container in this repository can be used to launch a virtual RAN with srsRAN. Currently, three containers are used for the RU, DU and CU. A test UE is defined in the DU configuration file, which can be used to verify the functionality of the setup.

## Running

The RAN can be brought up by starting up each of the containers separately. The configurations for all of the containers are provided in the `/configs`-folder, which can be mounted to each of the containers in order to use the appropriate configuration file.

The command to run each of the containers is: 

`docker run  --rm -v ./configs:/configs --network host --privileged ekelhala/srsran-container <component binary> -c /configs<corresponding config>`

The binaries for the components are `srsdu` for DU, `srscu` for CU and `ru_emulator` for RU. Config files are `cu.yaml` for CU, `du.yaml` for DU and `ru.yaml` for RU.

The recommended order when bringing the RAN up is **CU -> RU -> DU**
