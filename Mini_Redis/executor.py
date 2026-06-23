class Executor:

    def __init__(self, storage):
        self.storage = storage

    def execute(self, command, log=True):

        if command.operation == "PUT":

            self.storage.put(
                command.key,
                command.value,
                ttl=command.ttl,
                log=log
            )

        elif command.operation == 'GET':
            return self.storage.get(command.key)

        elif command.operation == 'DELETE':
            self.storage.delete(
                command.key,
                log=log
            )

        elif command.operation == 'SAVE':
            self.storage.save()

        elif command.operation == 'LOAD':
            self.storage.load()
