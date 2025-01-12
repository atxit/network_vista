# Network Vista Setup Instructions

# Network Vista Overview

Your original statement provides a clear overview of Network Vista. To enhance clarity and readability, consider the following revision:

Network Vista is a network data collection and compliance platform. Users can:

* Collect Data: Gather information from network devices.
* Parse and Structure: Organize the collected data into a structured database.
* Query and Test: Execute queries and create tests against the stored data to ensure compliance and analyze network performance.

# Prerequisites

Please ensure that you have the following prerequisites and dependencies in place

* Python 3.10 (or higher): The project is built on Python, and it requires version 3.10 or higher to run successfully.
* Docker: Docker is required as part of this installation. 
* Git: Git is required to clone this repository.

# Installation Instructions

Note: these installation Instructions has only been tested against Linux Based platforms. 

Clone the repo
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


Install poetry project dependencies. 
```bash
poetry install
```
set python path (if needed)

to verify 
```bash
echo $PYTHONPATH
```
if nothing is returned, set using:
```bash
. set_python_path.sh
```

Ensure MongoDB is up and running.

```bash
make start
```

Click http://127.0.0.1:5020/acitfserver to access the project's web interface.

Once you have access, checkout my YouTube video https://youtu.be/82LW_qfmCuA on how to navigate the project or review the "how to" guides found within the howTo directory (located within this repository)




