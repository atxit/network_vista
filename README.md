# Network Vista (beta 0.9)

Introducing Network Vista, a comprehensive platform designed to streamline network data collection and ensure compliance. The Network Vista platform offers a holistic view of your network.

* Define Database Structures: Easily set up database tables tailored to your network's needs.
* Track change: Effortlessly monitor and record modifications within your tables, providing clear insights into what changed and when.
* Automate Data Population: Specify 'show' commands to automatically populate tables with relevant data.
* Utilise Advanced Parsing: Leverage SSH for secure device communication and employ NTC Templates for efficient data parsing or utilise the inbuilt 'build your own Parser' module (PPT).
* Integrate Custom Meraki Platform Parsers: Seamlessly incorporate bespoke parsers for Cisco Meraki devices, ensuring accurate data collection and analysis.
* Track Configuration Changes: Maintain a comprehensive record of changes within any table, facilitating effective change management.
* Implement Custom Tests: Create user-defined tests within tables to ensure compliance and monitor network performance.
* Support Configuration Auditing: Conduct thorough configuration audits for both SSH-enabled devices and Cisco Meraki platforms, enhancing network security and compliance.
* API Support for All user defined tables: Access all table data via robust API integration, enabling seamless integration with other systems and enhancing automation capabilities.
* Support LDAP Integration: Integrate with Lightweight Directory Access Protocol (LDAP) servers to centralize authentication and streamline user management.
* Implement Role-Based Access Control (RBAC): Define and enforce user roles and permissions to ensure secure and appropriate access to Network Vista resources.

With Network Vista, gain unparalleled insights into your network's data, ensuring both efficiency and compliance.

### Prerequisites

Please ensure that you have the following prerequisites and dependencies in place

* Python 3.10 (or higher): The project is built on Python, and it requires version 3.10 or higher to run successfully.
* Docker: Docker is required as part of this installation. 
* Git: Git is required to clone this repository.

### Installation Instructions

Note: these installation Instructions has only been tested against Linux Based platforms. 

Clone this repository
```bash
git clone https://github.com/atxit/network_vista.git
```

Go to the project folder
```bash
cd network_vista
```

Run setup.sh, this will:

* create a Python virtual environment in the root of the project.
* activate the virtual environment
* install all packages which are required to run this project

```bash
. setup.sh
```

Run python setup.py file, this will:

* generate system default passwords, which is used by Network Vista. These are found in the system.yml file (found in the root of the project)
* create a default location for the Mongo Databases (~/data/db).
* test connectivity to the docker hub.
* pull the Mongo Docker image.
* enable a Mongo password on each database
* generate default SSL certs which are stored in ~/network_vista_certs/ and used by the NGINX container. 


System passwords are found in the system.yml file, these are generated during the setup process and are unique to each deployment.
The Network Vista Root password is found within system.yml. 
If you wish to change the root password, simply update the root password and save the file. If the cluster is operationally, please restart it. 

If you wish to change the system generated SSL certs:

* shutdown the cluster.
* remove the existing certs.
* replace the SSL certs. 
* rename the new public cert and private key using the following: network_vista_private_key.pem & network_vista_public_cert.pem
* restart the cluster.

```bash
python3 setup.py
```

Run python cluster_controller.py, this will start the controller UI. Within the controller UI, you can:

* start the cluster. 
* stop the cluster.
* check the status of the cluster.
* import the Network Vista core images or update the existing images.
* test connectivity to the Docker Hub.

```bash
python3 cluster_controller.py
```

1) Pull Core Images

Note: During the first installation, the cluster controller will pull the Network Vista core image. As these core images are fairly large, please be patient.

![readmeImages/img10.png](readmeImages/img10.png)

2) Check the Cluster Status, all containers should be display down.

![readmeImages/img11.png](readmeImages/img11.png)

3) Start the Cluster

![readmeImages/img0.png](readmeImages/img0.png)

![readmeImages/img1.png](readmeImages/img1.png)

4) Check Cluster Status, all containers should be active. 

![readmeImages/img2.png](readmeImages/img2.png)

![readmeImages/img3.png](readmeImages/img3.png)

To stop the cluster, please select the Stop Cluster option. 

Click https://127.0.0.1 to access Network Vista.

### Support with using Network Vista

For support on how to use Network Vista, please check out my YouTube Channel https://www.youtube.com/channel/UCBLGibrwjedh2GW4nrF8bzQon or 
review the "how to" guides which are found within the howTo directory, located within this repository
