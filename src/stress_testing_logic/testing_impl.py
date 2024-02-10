import random
import subprocess
import time
from contextlib import asynccontextmanager
from threading import Lock
import docker
from docker.models.containers import Container

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
    #    TODO capturing of container's id on creating, put it into the array
    docker_client = docker.client.from_env()

    for idx in range(CONTAINERS_MAX):
        print("{} container started ...".format(idx))
        containers.append(docker_client.containers.run(image="stress_container",
                                                       detach=True,
                                                       auto_remove=True,
                                                       remove=True,
                                                       name=f'cont{idx}',
                                                       tty=True))

        CONTAINERS_NOW += 1
    mutexes = [Lock() for _ in range(CONTAINERS_MAX)]

    yield  # instructions after the yield will be executed on shutdown

    for container in containers:
        print(f"Destroying {container}")
        container.kill()


def cp_code_into_container(container, room: room_schemas.Room):
    data = [("bru.cpp", room.bruteforce_src),
            ("opt.cpp", room.tested_src),
            ("gen.cpp", room.test_gen_src),
            ("che.cpp", room.checker_src)]

    for piece in data:
        file_path, content = piece
        cmd = ['sh', '-c', f'echo "{content}" > {file_path}']
        exec_id = container.exec_run(cmd, user='root')


def run_testing(container) -> tuple[int, bytes]:
    """
        Initiates testing pipeline script inside the container
    :param container:
    :return: tuple (int, bytes)
    """
    cmd = ['sh', '-c', f'bash testing_pipeline.sh']
    return container.exec_run(cmd)


def test_code(room: room_schemas.Room) -> schemas.TestingOutput:
    """
        This function runs the code for some room object, by neither building an image, nor starting a
        container, instead, it finds an available container (that is currently not busy with testing),
        copies files inside, runs, and then deletes the files.
        :param room: room, the entry retrieved from the db for a particular id
        :return: testing verdict
    """

    idx_container = random.randint(0, CONTAINERS_MAX - 1)
    mutex = mutexes[idx_container]

    report: str
    elapsed: str
    if mutex.acquire(True):
        try:
            print("Acquired the mutex, container {} is running".format(idx_container))
            W_DIR = "/usr/test_env"
            container = containers[idx_container]

            cp_code_into_container(container, room)

            start_t = time.time()
            result = run_testing(container)
            end_t = time.time()

            report = str(result[1])
            elapsed = str(end_t - start_t)
        finally:
            mutex.release()

    return schemas.TestingOutput(
        elapsed_time=elapsed,
        output=report
    )
