from cuid2 import Cuid



class CUID2:
    def __init__(self, length: int, prefix: str = None):
        self.cuid = Cuid(length=length)
        """
            length: the length of the cuid itself
            len(prefix): the length of the added prefix
            and + 1 for the '-' char
        """
        self.length: int = length + len(prefix) + 1
        self.prefix: str = prefix

    """
        generate: this will generate a cuid,
        e.g.
        prefix-efw1yxqitcwv9544jbqg4jjd
    """
    def generate(self) -> str:
        return f"{self.prefix}-{self.cuid.generate()}"


CUID_USER: CUID2 = CUID2(length=35, prefix="user")
CUID_ROOM: CUID2 = CUID2(length=25, prefix="room")
CUID_TAG: CUID2 = CUID2(length=30, prefix="tag")
CUID_ATTENDANCE: CUID2 = CUID2(length=25, prefix="att")
CUID_ATTENDEE: CUID2 = CUID2(length=15, prefix="at")
