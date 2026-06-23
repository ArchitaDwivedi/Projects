from command import Command
from exceptions import InvalidCommandError


class Parser:

    def __init__(self, string) -> None:
        self.string = string

    def command_split(self):

        split_list = self.string.split()

        typ = split_list[0].upper()

        if typ == "PUT":

            if len(split_list) == 3:
                return (
                    typ,
                    split_list[1].upper(),
                    split_list[2].upper(),
                    None
                )

            elif len(split_list) == 5:

                if split_list[3].upper() != "EX":
                    raise ValueError(
                        "Expected EX"
                    )

                return (
                    typ,
                    split_list[1].upper(),
                    split_list[2].upper(),
                    int(split_list[4])
                )

            raise ValueError(
                "Invalid PUT syntax"
            )

        if typ in ("GET", "DELETE"):

            if len(split_list) != 2:
                raise ValueError(
                    f"{typ} requires exactly 1 argument"
                )

            return (
                typ,
                split_list[1].upper(),
                None,
                None
            )

        raise ValueError(
            "Invalid command"
        )

    def validation(self, typ, key, value, ttl=None):

        # Incorrect combination
        '''
            Rules:
                1. WITH PUT- MUST HAVE A AND B
                2. WITH GET - ONLY A
                3. WITH DELETE - ONLY A
        '''

        if typ not in ('SAVE', 'LOAD') and not key:
            raise ValueError(f'No key given for {typ}')

        if typ == 'PUT' and not value:
            raise ValueError('No value given for PUT')

    def build_cmd_object(
        self,
        typ,
        key,
        value,
        ttl
    ):

        return Command(
            operation=typ,
            key=key,
            value=value,
            ttl=ttl
        )
