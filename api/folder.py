import os

class Folder:
    def __init__(self, root:str="/notes/"):
        self.root = root

    def ls(self, path: str):
        return os.scandir(self.root+path)
    
    def mkdir(self, path:str):
        return os.mkdir(self.root+path)

    def touch(self, path:str):
        return os.system(f'touch {self.root}{path}')

    def cat(self, path:str):
        return os.system(f'cat {self.root}{path}')
    
    def write(self, path: str, text: str):
        return os.system(f'echo "{text}" > {self.root}{path}')

    def rm(self, path:str):
        return os.system(f'rm -rf {self.root}{path}')
