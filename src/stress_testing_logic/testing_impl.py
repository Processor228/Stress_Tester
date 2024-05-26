import json
import random
import subprocess
import time
from contextlib import asynccontextmanager
from asyncio import Lock
import docker
from docker.models.containers import Container
import asyncio

from fastapi import FastAPI

import src.room_manage_logic.schemas as room_schemas
import src.stress_testing_logic.schemas as schemas

CONTAINERS_NOW = 0
CONTAINERS_MAX = 5
mutexes: list[Lock]
containers = []  # can't find type of Container Object
docker_client: docker.client.DockerClient


def phony_implementation(room: room_schemas.Room) -> schemas.TestingOutput:
    return schemas.TestingOutput(
        elapsed_time=0.0,
        output="Phony implementation"
    )


@asynccontextmanager
async def prepare_containers(app: FastAPI):
    global CONTAINERS_NOW, CONTAINERS_MAX, mutexes, docker_client
    docker_client = docker.client.from_env()

    for idx in range(CONTAINERS_MAX):
        print("{} container started ...".format(idx))
        containers.append(docker_client.containers.run(image="stress_container",
                                                       detach=True,
                                                       auto_remove=True,
                                                       remove=True,
                                                       name=f'cont{idx}',
                                                       tty=True))

    mutexes = [Lock() for _ in range(CONTAINERS_MAX)]

    yield  # instructions after the yield will be executed on shutdown

    for container in containers:
        print(f"Destroying {container}")
        container.kill()


def cp_code_into_container(container, room: room_schemas.Room):
    data = [(f"brute.{room.bruteforce_lang}", room.bruteforce_src),
            (f"tested.{room.tested_lang}", room.tested_src),
            (f"gener.{room.test_gen_lang}", room.test_gen_src),
            (f"che.{room.checker_lang}", room.checker_src)]

    for piece in data:
        file_path, content = piece
        cmd = ['sh', '-c', f'echo {json.dumps(content)} > {file_path}']
        exec_id = container.exec_run(cmd, user='root')


# I want to run that as a task... such task that will block current function execution and let other
# functions run.

def run_testing(container, brtfrs_ext, tested_ext, genrtr_ext) -> tuple[int, bytes]:
    """
        Initiates testing pipeline script inside the container
    :param genrtr_ext:
    :param brtfrs_ext:
    :param tested_ext:
    :param container:
    :return: tuple (int, bytes) - the return code of the program and it's stdout, in bytes.
    """
    cmd = ['sh', '-c',
           f'python3 testing_pipeline.py -b brute.{brtfrs_ext} -o tested.{tested_ext} -g gener.{genrtr_ext}']

    return container.exec_run(cmd)


async def test_code(room: room_schemas.Room) -> schemas.TestingOutput:
    """
        This function runs the code for some room object, by neither building an image, nor starting a
        container, instead, it finds an available container (that is currently not busy with testing),
        copies files inside, runs, and then deletes the files.
        :param room: room, the entry retrieved from the db for a particular id
        :return: testing verdict
    """
    global CONTAINERS_MAX, CONTAINERS_NOW
    idx_container = (CONTAINERS_NOW + 1) % CONTAINERS_MAX
    CONTAINERS_NOW += 1
    CONTAINERS_NOW %= CONTAINERS_MAX

    mutex = mutexes[idx_container]

    report: str
    elapsed: str

    await mutex.acquire()
    try:
        W_DIR = "/usr/test_env"
        container = containers[idx_container]

        cp_code_into_container(container, room)

        start_t = time.time()
        testing_coro = asyncio.to_thread(run_testing,
                                         container=container,
                                         brtfrs_ext=room.bruteforce_lang,
                                         tested_ext=room.tested_lang,
                                         genrtr_ext=room.test_gen_lang)

        result = await asyncio.create_task(testing_coro)

        end_t = time.time()

        report = result[1].decode("utf-8")
        elapsed = str(end_t - start_t)
    finally:
        mutex.release()

    return schemas.TestingOutput(
        elapsed_time=elapsed,
        output=report
    )
