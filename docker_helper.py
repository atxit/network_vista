import argparse
import sys
import os
import time
from pathlib import Path
import platform
from datetime import datetime, timedelta
from requests import get
import requests

import yaml
import docker
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

from pymongo import MongoClient
from pymongo.errors import OperationFailure
import subprocess

from print_log import print_to_screen


def confirm_system_cfg_file():
    return os.path.isfile("system.yml")


def read_system_file():
    with open("system.yml", "r") as file_handler:
        return yaml.safe_load(file_handler)


def is_macbook_with_apple_processor():
    if platform.system() == "Darwin":
        try:
            result = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], text=True)
            if "Apple" in result:
                return True
        except Exception as e:
            print(f"Error detecting processor: {e}")
    return False


class DockerHelper:
    def __init__(self, stdscr=None):
        self.args = None
        self.stdscr = stdscr
        self.line_id = 0
        if confirm_system_cfg_file():
            system_vars = read_system_file()["system"]
            self.cluster_api_key = system_vars["CLUSTER_API_KEY"]
            self.mongo_pw = system_vars["MONGO_PW"]
            self.root_pw = system_vars["ROOT_PW"]
            self.vault_key = system_vars["VAULT_KEY"]
        else:
            print("system configuration file missing, terminating...")
            sys.exit(1)

        if is_macbook_with_apple_processor():
            self.hub_core_image = "networkvista/network_vista_core_apple:latest"
            self.hub_nginx_image = "networkvista/network_vista_nginx_apple:latest"
            self.local_core_image = "network_vista_core_apple:latest"
            self.local_nginx_image = "network_vista_nginx_apple:latest"
        else:
            self.hub_core_image = "networkvista/network_vista_core:latest"
            self.hub_nginx_image = "networkvista/network_vista_nginx:latest"
            self.local_core_image = "network_vista_core:latest"
            self.local_nginx_image = "network_vista_nginx:latest"

    def parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", action="store_true", help="init, setup")
        parser.add_argument(
            "-d", action="store_true", help="remove all user admins from Dbs"
        )
        parser.add_argument("-m", action="store_true", help="starts Mongo Db")
        parser.add_argument("-x", action="store_true", help="generate certs")
        parser.add_argument("-s", default=None, help="starts a non-mongo container")
        parser.add_argument("-c", action="store_true", help="Clear all dangling images")
        parser.add_argument("-t", default=None, help="terminates container by name")
        parser.add_argument("-start", action="store_true", help="Start the cluster")
        self.args = parser.parse_args(sys.argv[1:])

        if self.args.x:
            self.generate_self_signed_cert()
            sys.exit()

        if self.args.s is not None:
            if self.args.s == "nginx":
                self.start_nginx()
            else:
                self.start_core_container(container_name=self.args.s)
            sys.exit()

        if self.args.c:
            self.prune_images()
            sys.exit()

        if self.args.t is not None:
            self.stop_container_by_name(self.args.t)
            sys.exit()

        if self.args.start is True:
            self.start_cluster()

        if self.args.i:
            self.create_dbs()
            self.add_restricted_account_to_dbs()

        if self.args.d:
            self.remove_restricted_account_from_dbs()

        if self.args.m:
            self.start_mongo_container(secure=True)

    def create_mongo_dbs(self):
        self.create_mongo_folder()
        container = self.start_mongo_container()
        client = MongoClient("mongodb://localhost:27017/")
        for db_id in ["static", "aSide", "bSide"]:
            db = client[db_id]
            collection = db["temp"]
            collection.insert_one({"key": "value"})
            collection.drop()
        client.close()
        print_to_screen("stopping Mongo DB")
        container.stop()
        print_to_screen("stopped Mongo DB")
        print_to_screen("removing Mongo DB container")
        container.remove()
        print_to_screen("removed Mongo DB container")

    def add_restricted_account_to_dbs(self):
        print_to_screen("adding restricted account to Mongo DB")
        self.create_mongo_folder()
        print_to_screen("starting Mongo DB")
        container = self.start_mongo_container()
        print_to_screen("started Mongo DB")
        client = MongoClient("mongodb://localhost:27017/")
        for db_id in ["static", "aSide", "bSide"]:
            print_to_screen(f"adding admin to {db_id}")
            db = client[db_id]
            try:
                db.command(
                    "createUser",
                    "admin",
                    pwd=self.mongo_pw,
                    roles=["readWrite"],
                )
                print_to_screen(f"added admin to {db_id}")
            except Exception:
                print_to_screen(f"removing admin, then re-adding {db_id}")
                try:
                    db.command("dropUser", "admin")
                except OperationFailure:
                    print_to_screen(f"user not present in {db_id}, skipped")
                db.command(
                    "createUser",
                    "admin",
                    pwd=self.mongo_pw,
                    roles=["readWrite"],
                )
                print_to_screen(f"added admin to {db_id}")

        client.close()
        print_to_screen("stopping Mongo DB")
        container.stop()
        print_to_screen("stopped Mongo DB")
        print_to_screen("removing Mongo DB container")
        container.remove()
        print_to_screen("removed Mongo DB container")

    def remove_restricted_account_from_dbs(self):
        print("removing restricted access from DBs")
        container = self.start_mongo_container()
        client = MongoClient("mongodb://localhost:27017/")
        for db_id in ["static", "aSide", "bSide"]:
            db = client[db_id]
            try:
                db.command("dropUser", "admin")
            except OperationFailure:
                print(f"user not present in {db_id}, skipped")
            print(f"removed {db_id} from DBs")
        client.close()
        container.stop()
        container.remove()

    def start_mongo_container(self, secure=False):
        container_name = "mongodb"
        image_name = "mongo:latest"
        port_mapping = {"27017": "27017"}
        volumes = {self.mongo_file_path(): {"bind": "/data/db", "mode": "rw"}}
        client = docker.from_env()

        self.stop_container_by_name(container_name)
        self.create_docker_network()

        if secure:
            container = client.containers.run(
                image=image_name,
                name=container_name,
                detach=True,
                ports=port_mapping,
                environment={
                    "MONGO_INITDB_ROOT_USERNAME": "admin",
                    "MONGO_INITDB_ROOT_PASSWORD": self.mongo_pw,
                },
                volumes=volumes,
                network="docker_network",
                command="mongod --auth",
            )
        else:
            container = client.containers.run(
                image=image_name,
                name=container_name,
                detach=True,
                ports=port_mapping,
                volumes=volumes,
            )
        #

        return container

    def start_nginx(self):
        self.print_stdscr("starting container: NGINX")
        self.stop_container_by_name(container_name="network_vista_nginx")
        client = docker.from_env()
        try:
            container = client.containers.run(
                image=self.local_nginx_image,
                name="network_vista_nginx",
                detach=True,
                ports={"443": "443"},
                volumes={
                    os.path.abspath(
                        os.path.join(os.path.expanduser("~"), "network_vista_certs")
                    ): {"bind": "/network_vista_certs", "mode": "rw"}
                },
                network="docker_network",
                command="systemctl start nginx",
            )
        except docker.errors.NotFound as msg:
            try:
                container = client.containers.run(
                    image=self.hub_nginx_image,
                    name="network_vista_nginx",
                    detach=True,
                    ports={"443": "443"},
                    volumes={
                        os.path.abspath(
                            os.path.join(os.path.expanduser("~"), "network_vista_certs")
                        ): {"bind": "/network_vista_certs", "mode": "rw"}
                    },
                    network="docker_network",
                    command="systemctl start nginx",
                )
            except:
                print("could not located network_vista_nginx:latest")
                sys.exit(1)
            self.print_stdscr("container NGINX has started")
            self.print_stdscr("Completed, push Enter to close")
        return container

    def start_core_container(self, container_name):
        self.print_stdscr(f"starting container: {container_name}")
        self.stop_container_by_name(container_name=container_name)
        client = docker.from_env()
        if container_name == "frontend":
            command = "./dist/boot -b frontend"
        elif container_name == "backend":
            command = "./dist/boot -b backend"
        elif container_name == "collector":
            command = "./dist/boot -b collector"
        else:
            self.print_stdscr("container name not matched")
            sys.exit(1)

        env_dict = {
            "DOCKER_ENABLED": True,
            "CLUSTER_API_KEY": self.cluster_api_key,
            "ROOT_PW": self.root_pw,
            "VAULT_KEY": self.vault_key,
            "MONGO_PW": self.mongo_pw,
        }
        try:
            _ = client.containers.run(
                image=self.local_core_image,
                name=container_name,
                detach=True,
                network="docker_network",
                command=command,
                environment=env_dict,
            )
            self.print_stdscr(f"container {container_name} has now started")
        except docker.errors.NotFound as msg:
            try:
                _ = client.containers.run(
                    image=self.hub_core_image,
                    name=container_name,
                    detach=True,
                    network="docker_network",
                    command=command,
                    environment=env_dict,
                )
            except Exception:
                self.print_stdscr(f"could not start container {container_name}")

    def prune_containers(self):
        client = docker.from_env()
        pruned_containers = client.containers.prune()
        if pruned_containers["ContainersDeleted"]:
            for container_id in pruned_containers["ContainersDeleted"]:
                self.print_stdscr(f"pruned container : {container_id}")

    def prune_images(self):
        client = docker.from_env()
        prune_results = client.images.prune()
        if (
            "ImagesDeleted" in prune_results
            and prune_results["ImagesDeleted"] is not None
        ):
            self.print_stdscr("pruned dangling images...")
        self.print_stdscr("push Enter to exit")

    def generate_self_signed_cert(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        subject = x509.Name(
            [
                x509.NameAttribute(x509.NameOID.COMMON_NAME, "network_vista.local"),
            ]
        )

        validity_period = timedelta(days=9000)
        not_before = datetime.utcnow()
        not_after = not_before + validity_period

        certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(subject)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(not_before)
            .not_valid_after(not_after)
            .sign(private_key, hashes.SHA256(), default_backend())
        )

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        certificate_pem = certificate.public_bytes(encoding=serialization.Encoding.PEM)
        self.write_cert_and_key(private_key_pem, certificate_pem)

    def start_cluster(self):
        self.prune_containers()
        self.stop_container_by_name("mongodb")
        self.start_mongo_container(secure=True)
        for container_name in ["frontend", "backend", "collector"]:
            self.start_core_container(container_name)
        self.stop_container_by_name("nginx")
        self.start_nginx()
        self.print_stdscr(f"completed, push Enter to exit")

    def print_stdscr(self, to_print):
        if isinstance(to_print, str):
            to_print = to_print.split("\n")

        if self.stdscr is not None:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            start_row = (height // 2) - (len(to_print) // 2)

            for idx, line in enumerate(to_print):
                x_pos = (width // 2) - (len(line) // 2)
                y_pos = start_row + idx
                self.stdscr.addstr(y_pos, x_pos, line)

            self.stdscr.refresh()
        else:
            for line in to_print:
                print_to_screen(line)

    def docker_pull_image(self, image_name):
        self.print_stdscr(
            "### NOTE: Please be patient, some images are fairly large ###"
        )
        time.sleep(2)
        if isinstance(image_name, str):
            image_name = image_name.split()

        for image in image_name:
            if image == 'network_vista_core':
                image_id = self.hub_core_image
            elif image == 'network_vista_nginx':
                image_id = self.hub_nginx_image
            else:
                image_id = image

            client = docker.APIClient()
            try:
                response = client.pull(image_id, stream=True, decode=True)

                total_layers = 0
                downloaded_layers = 0
                progress_tracker = {}
                print_to_screen(f"Pulling image: {image_id}")

                for event in response:
                    status = event.get("status")
                    layer_id = event.get("id")
                    progress = event.get("progressDetail")
                    if status == "Downloading" and progress:
                        current = progress.get("current", 0)
                        total = progress.get("total", 1)
                        progress_tracker[layer_id] = (current, total)

                    elif status == "Extracting":
                        if layer_id not in progress_tracker:
                            downloaded_layers += 1
                            total_layers += 1

                    elif status == "Pull complete":
                        if layer_id not in progress_tracker:
                            total_layers += 1
                        downloaded_layers += 1
                        progress_tracker[layer_id] = (1, 1)

                    if total_layers > 0:
                        overall_progress = (downloaded_layers / total_layers) * 100
                        self.print_stdscr(f"Progress: {overall_progress:.2f}%")
                    try:
                        self.print_stdscr(f"Status: {status} | Layer: {layer_id} | Progress: {progress}")
                    except Exception:
                        pass
            except docker.errors.NotFound:
                self.print_stdscr(f'{image_id} not found')
                time.sleep(4)
        self.prune_images()

    def create_docker_network(self):
        network_name = "docker_network"
        client = docker.from_env()
        networks = client.networks.list()
        network_exists = any(network.name == network_name for network in networks)
        if not network_exists:
            try:
                network = client.networks.create(network_name)
                self.print_stdscr(
                    f"Network '{network_name}' was successfully created using Id: {network.id}"
                )
            except docker.errors.APIError as e:
                self.print_stdscr(f"Error creating network: {e}")

    def connectivity_tests(self):
        docker_url = False
        try:
            response = get("https://registry-1.docker.io/v2/", timeout=2)
            if response.status_code == 401:
                docker_url = True
        except requests.RequestException:
            self.print_stdscr(
                [
                    f"An error occurred while accessing the Docker registry",
                    "please Enter to exit",
                ]
            )
        self.print_stdscr(
            [
                f"Docker connectivity test results: {'successful' if docker_url else 'unsuccessful'}",
                'press Enter to exit'
            ]
        )

    def stop_all_containers(self):
        client = docker.from_env()
        all_containers = client.containers.list()
        if len(all_containers) > 0:
            self.print_stdscr("shutdown of containers begins, please wait...")
        else:
            self.print_stdscr(f"All containers currently stopped, nothing to do")
        for container in all_containers:
            if container.name in (
                "network_vista_nginx",
                "collector",
                "backend",
                "frontend",
                "mongodb",
            ):
                self.print_stdscr(
                    f'stopping container "{container.name}", container is {container.status}'
                )
                container.stop()
                container.remove()
                self.print_stdscr(f"removed container {container.name}")

        self.print_stdscr(f"completed, push Enter to exit")

    @staticmethod
    def create_mongo_folder():
        expanded_directory_path = os.path.expanduser("~/data/db")
        if not os.path.exists(expanded_directory_path):
            os.makedirs(expanded_directory_path)
            print_to_screen(f"Directory '{expanded_directory_path}' created.")
        else:
            print_to_screen(f"Directory '{expanded_directory_path}' already exists.")

    def list_all_running_containers(self):
        client = docker.from_env()
        running_containers = client.containers.list()
        expected_containers_dict = {
            "network_vista_nginx": False,
            "collector": False,
            "backend": False,
            "frontend": False,
            "mongodb": False,
        }
        for expected_containers in expected_containers_dict:
            for container in running_containers:
                if expected_containers == container.name:
                    expected_containers_dict[expected_containers] = True
        result = []
        for container_name, active in expected_containers_dict.items():
            result.append(f'{container_name} is {"active" if active else "down"}')

        result.append('completed, press enter to exit')
        self.print_stdscr(result)

    def write_cert_and_key(self, private_key_pem, certificate_pem):
        private_key = str(
            Path(self.define_cert_folder(), "network_vista_private_key.pem")
        )
        public_cert = str(
            Path(self.define_cert_folder(), "network_vista_public_cert.pem")
        )

        self.create_cert_folder()

        if not os.path.isfile(private_key):
            with open(private_key, "wb") as key_file:
                key_file.write(private_key_pem)
            self.print_stdscr(
                [
                    f"wrote private key to {private_key}",
                    f"wrote public key to {public_cert}"
                ]
            )

        if not os.path.isfile(public_cert):
            with open(public_cert, "wb") as cert_file:
                cert_file.write(certificate_pem)
            self.print_stdscr(
                [
                    f"wrote private key to {private_key}",
                    f"wrote public key to {public_cert}",
                ]
            )

    @staticmethod
    def stop_container_by_name(container_name):
        client = docker.from_env()
        all_containers = client.containers.list()
        for container_obj in [x for x in all_containers if x.name == container_name]:
            container_obj.stop()
            container_obj.remove()

    @staticmethod
    def define_cert_folder():
        return os.path.abspath(
            os.path.join(os.path.expanduser("~"), "network_vista_certs")
        )

    @staticmethod
    def mongo_file_path():
        return os.path.abspath(os.path.join(os.path.expanduser("~"), "data/db"))

    def create_cert_folder(self):
        os.makedirs(self.define_cert_folder(), exist_ok=True)


if __name__ == "__main__":
    docker_helper = DockerHelper()
    docker_helper.parse()
