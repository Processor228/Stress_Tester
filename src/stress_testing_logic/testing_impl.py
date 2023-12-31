import schemas
import src.room_manage_logic.schemas as room_schemas


def test_code(room: room_schemas.Room) -> schemas.TestingOutput:
    """
    This function runs the code for some room object
    :param room: room, the entry retrieved from the db for a particular id
    :return: testing verdict
    """
    return schemas.TestingOutput(elapsed_time=1.13,
                                 output="not yet implemented, sorry {} room can't be run".format(room.id)
                                 )
