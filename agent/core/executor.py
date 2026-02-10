"""
Command Executor
Executes commands received from HQ
"""

class CommandExecutor:
    """Executes allowed commands"""
    
    def __init__(self):
        self.allowed_commands = set()
    
    def execute(self, command):
        """Execute a command safely"""
        pass
    
    def is_allowed(self, command_type):
        """Check if command type is allowed"""
        pass
