import sys
import os

import docker
import curses

from docker_helper import DockerHelper
from print_log import print_to_screen


class ClusterController:
    def __init__(self):
        self.stdscr = None
        self.process_dict = {}
        self.env_setup = None

    @staticmethod
    def docker_menu(stdscr):
        stdscr.clear()
        stdscr.refresh()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        menu_items = [
            "stop cluster",
            "upgrade cluster",
            "start cluster",
            "cluster status",
            "connectivity test",
            "exit session",
        ]
        selected_option = 0

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            for idx, item in enumerate(menu_items):
                x = width // 2 - len(item) // 2
                y = height // 2 - len(menu_items) // 2 + idx
                if idx == selected_option:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, item)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, item)
            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(menu_items)
            elif key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(menu_items)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if selected_option == len(menu_items) - 1:
                    break
                else:
                    stdscr.clear()
                    env_setup = DockerHelper(stdscr)
                    if menu_items[selected_option] == "stop cluster":
                        env_setup.stop_all_containers()

                    elif menu_items[selected_option] == "upgrade cluster":
                        env_setup.docker_pull_image('mongo')
                        env_setup.docker_pull_image(["network_vista_nginx", "network_vista_core"])

                    elif menu_items[selected_option] == "start cluster":
                        env_setup.start_cluster()

                    elif menu_items[selected_option] == "cluster status":
                        env_setup.list_all_running_containers()

                    elif menu_items[selected_option] == "connectivity test":
                        env_setup.connectivity_tests()

                    stdscr.refresh()
                    stdscr.getch()


def check_docker_installed():
    try:
        client = docker.from_env()
        client.ping()
        return True
    except docker.errors.DockerException:
        return False


if __name__ == "__main__":
    try:
        if not check_docker_installed():
            print_to_screen("docker not installed or running", log_level='error')
            sys.exit(1)

        if not os.path.isfile("system.yml"):
            print_to_screen("system.yml file missing, please run setup.py", log_level='error')
            sys.exit(1)

        cluster_controller = ClusterController()
        curses.wrapper(cluster_controller.docker_menu)
    except KeyboardInterrupt:
        sys.exit(1)
