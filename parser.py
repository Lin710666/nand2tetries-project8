#CLASS
class Parser:
    def __init__(self, file):
        self.file = file
        self.commands = []
    
    def get_code(self):
        with open(self.file, 'r') as f:
            for line in f:
                # 移除注释
                line = line.split('//')[0]
                # 移除换行符和空白
                line = line.strip()
                # 跳过空行
                if line:
                    self.commands.append(line)
        return self.commands


           
        


            



        
