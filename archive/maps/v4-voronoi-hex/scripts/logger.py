class Logger():
    def __init__(self):
        self.verbose = False
        self.log_indent = 0
    
    def setVerbose(self, v):
        self.verbose = v
    
    def log(self, msg):
        if self.verbose:
            print(f"{'  ' * self.log_indent}{msg}")

    def indent(self, n=1):
        self.log_indent += n
    
    def outdent(self, n=1):
        self.log_indent -= n
    
