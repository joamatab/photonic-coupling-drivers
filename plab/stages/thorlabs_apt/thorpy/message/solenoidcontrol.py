from ._base import Message


##### Solenoid Control Messages #####
class MGMSG_MOT_GET_SOL_CYCLEPARAMS(Message):
    id = 0x4C5
    is_long_cmd = True
    parameters = [
        ("chan_ident", "H"),
        ("on_time", "I"),
        ("off_time", "I"),
        ("num_cycles", "I"),
    ]


class MGMSG_MOT_GET_SOL_INTERLOCKMODE(Message):
    id = 0x4C8
    parameters = [("chan_ident", "B"), ("mode", "B")]


class MGMSG_MOT_GET_SOL_OPERATINGMODE(Message):
    id = 0x4C2
    parameters = [("chan_ident", "B"), ("mode", "B")]


class MGMSG_MOT_GET_SOL_STATE(Message):
    id = 0x4C8
    parameters = [("chan_ident", "B"), ("state", "B")]


class MGMSG_MOT_REQ_SOL_CYCLEPARAMS(Message):
    id = 0x4C4
    parameters = [("chan_ident", "B"), (None, "B")]


class MGMSG_MOT_REQ_SOL_INTERLOCKMODE(Message):
    id = 0x4C7
    parameters = [("chan_ident", "B"), (None, "B")]


class MGMSG_MOT_REQ_SOL_OPERATINGMODE(Message):
    id = 0x4C1
    parameters = [("chan_ident", "B"), (None, "B")]


class MGMSG_MOT_REQ_SOL_STATE(Message):
    id = 0x4C7
    parameters = [("chan_ident", "B"), (None, "B")]


class MGMSG_MOT_SET_SOL_CYCLEPARAMS(Message):
    id = 0x4C3
    is_long_cmd = True
    parameters = [
        ("chan_ident", "H"),
        ("on_time", "I"),
        ("off_time", "I"),
        ("num_cycles", "I"),
    ]


class MGMSG_MOT_SET_SOL_INTERLOCKMODE(Message):
    id = 0x4C6
    parameters = [("chan_ident", "B"), ("mode", "B")]


class MGMSG_MOT_SET_SOL_OPERATINGMODE(Message):
    id = 0x4C0
    parameters = [("chan_ident", "B"), ("mode", "B")]


class MGMSG_MOT_SET_SOL_STATE(Message):
    id = 0x4C6
    parameters = [("chan_ident", "B"), ("state", "B")]
