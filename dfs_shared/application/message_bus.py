from dfs_shared.domain import events
from dfs_shared.domain import commands


class MessageBus:
    def __init__(self, uow, command_handlers, event_handlers):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message):
        self.queue = [message]
        while len(self.queue) > 0:
            msg = self.queue.pop()
            if isinstance(msg, commands.Command):
                self.handle_command(msg)
            elif isinstance(msg, events.Event):
                self.handle_event(msg)
            self.queue.extend(self.uow.pull_events())
    
    def handle_command(self, command):
        handler = self.command_handlers.get(type(command))

        if not handler:
            raise ValueError(f"Handler for command '{command.__class__.__name__}' not found.")
        
        handler(command, self.uow)
    
    def handle_event(self, event):
        handlers = self.event_handlers.get(type(event), list())
        
        for handler in handlers:
            handler(event, self.uow)