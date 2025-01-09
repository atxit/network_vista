import os
import random
import string
import sys

import yaml
import docker

from docker_helper import DockerHelper
from print_log import print_to_screen


def generate_random_number_string():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=30))


def generate_random_string():
    return "".join(random.choices(string.ascii_letters, k=10))


def write_system_cfg_file():
    if not os.path.isfile("system.yml"):
        with open("system.yml", "w") as file:
            setup_dict = {
                "system": {
                    "VAULT_KEY": generate_random_number_string(),
                    "CLUSTER_API_KEY": generate_random_number_string(),
                    "MONGO_PW": generate_random_number_string(),
                    "ROOT_PW": generate_random_string(),
                }
            }
            yaml.dump(setup_dict, file, default_flow_style=False)
            print_to_screen("wrote system file to repo root")
    else:
        print_to_screen("system file detected, skipped")


def remove_existing_db_deployment():
    docker_helper = DockerHelper()
    if os.path.isdir(docker_helper.mongo_file_path()):
        wait_until = True
        while wait_until:
            resp = input("existing Mongo path found, remove? [Y/n]: ")
            if resp == "Y":
                os.system(f"rm -rf {docker_helper.mongo_file_path()}")
                wait_until = False
            elif resp == "n":
                wait_until = False


def add_restricted_account():
    docker_helper = DockerHelper()
    docker_helper.create_mongo_dbs()
    docker_helper.add_restricted_account_to_dbs()
    print_to_screen(
        "Mongo DB is currently down, use cluster controller to start",
        log_level="warning",
    )


def add_system_certs():
    docker_helper = DockerHelper()
    docker_helper.generate_self_signed_cert()


def check_docker_installed():
    try:
        client = docker.from_env()
        client.ping()
        return True
    except docker.errors.DockerException:
        return False


def connectivity_tests():
    docker_helper = DockerHelper()
    docker_helper.connectivity_tests()


if __name__ == "__main__":
    if not check_docker_installed():
        print_to_screen("docker not installed or running", log_level="error")
        sys.exit(1)

    write_system_cfg_file()
    remove_existing_db_deployment()
    connectivity_tests()
    add_restricted_account()
    add_system_certs()

    print_to_screen("setup is complete, start cluster by using the cluster controller")
