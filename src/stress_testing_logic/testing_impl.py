import src.stress_testing_logic.schemas as schemas
import src.room_manage_logic.schemas as room_schemas

import subprocess


CONTAINERS_NOW = 0
CONTAINERS_MAX = 5


def phony_implementation(room: room_schemas.Room) -> schemas.TestingOutput:
    return schemas.TestingOutput(
            elapsed_time=0.0,
            output="Phony implementation"
        )


def test_code(room: room_schemas.Room) -> schemas.TestingOutput:
    """
    This function runs the code for some room object
    :param room: room, the entry retrieved from the db for a particular id
    :return: testing verdict
    """
    stress_output: str

    if CONTAINERS_NOW >= CONTAINERS_MAX:
        return schemas.TestingOutput(
            elapsed_time=0.0,
            output="Wait"
        )

    # this is c++ testing implementation
    subprocess.run(["mkdir", "test_dir/stress{}".format(CONTAINERS_NOW)])

    with open("test_dir/stress{}/bruteforce_src.cpp".format(CONTAINERS_NOW), "w") as wr:
        wr.write(room.bruteforce_src)
    with open("test_dir/stress{}/test_gen_src.cpp".format(CONTAINERS_NOW), "w") as wr:
        wr.write(room.test_gen_src)
    with open("test_dir/stress{}/tested_src.cpp".format(CONTAINERS_NOW), "w") as wr:
        wr.write(room.tested_src)

    subprocess.run("cat test_script.sh > test_dir/stress{}/test.sh".format(CONTAINERS_NOW), shell=True)
    subprocess.run("cat test_Dockerfile > test_dir/stress{}/Dockerfile".format(CONTAINERS_NOW), shell=True)

    # --------------( building the image )------------------ #
    subprocess.run(
        ["docker", "build", "-t", "stress_{}".format(CONTAINERS_NOW), "test_dir/stress{}".format(CONTAINERS_NOW)])

    # ------------ ( starting the container ) --------------- #
    container_id = str(subprocess.check_output(
        ["docker", "run", "-t", "-d", "stress_{}:latest".format(CONTAINERS_NOW)]))[2:-3]
    print(container_id)

    # ------------ ( invoking testing procedure ) ---------- #
    stress_output = subprocess.check_output(["docker", "exec", container_id, "bash", "test.sh"]).decode("utf-8")
    subprocess.run(["docker", "kill", container_id])

    return schemas.TestingOutput(
        elapsed_time=1.13,
        output="not yet implemented, sorry {} room can't be run".format(room.id)
        )
