import assemblyTable
import parser

class CodeWriter:
    def __init__(self,commands,filename):
        self.arithmetic_ops = ['add', 'sub', 'and', 'or', 'not', 'neg', 'eq', 'gt', 'lt']
        self.compare_ops = ['eq', 'gt', 'lt']
        self.LATT = ['local','argument','this','that']
        self.label_ops = ['label','goto','if-goto']
        self.function_ops = ['function','call','return']
        self.commands = commands
        self.code = []
        self.compare_counter = 1
        self.func_counter = 1
        self.file = filename
        self.label_counter = 1

    def isMemory(self,eles):
        if (eles[0] == "push" or eles[0] == "pop"):
            return True
        
    def isArithmetic(self,eles):
        if (eles[0] in self.arithmetic_ops):
            return True
        
    def isLATT(self,eles):
        if (eles[1] in self.LATT):
            return True
        
    def isCompare(self,eles):
        if (eles[0] in self.compare_ops):
            return True
        
    def isLabel(self,eles):
        if (eles[0] in self.label_ops):
            return True
        
    def isFunction(self,eles):
        if (eles[0] in self.function_ops):
            return True
        
    def translateLATT(self,eles):
        if(eles[1] =="local"):
            key = eles[0]+' '+'segment'+' i'
            assembly_code = assemblyTable.map[key].replace('segmentPointer','1')
            assembly_code = assembly_code.replace('i',eles[2])
        if(eles[1] =="argument"):
            key = eles[0]+' '+'segment'+' i'
            assembly_code = assemblyTable.map[key].replace('segmentPointer','2')
            assembly_code = assembly_code.replace('i',eles[2])
        if(eles[1] =="this"):
            key = eles[0]+' '+'segment'+' i'
            assembly_code = assemblyTable.map[key].replace('segmentPointer','3')
            assembly_code = assembly_code.replace('i',eles[2])
        if(eles[1] =="that"):
            key = eles[0]+' '+'segment'+' i'
            assembly_code = assemblyTable.map[key].replace('segmentPointer','4')
            assembly_code = assembly_code.replace('i',eles[2])
        return assembly_code

    def translateOthers(self,eles):
        if eles[1] == "pointer":
            key = f"{eles[0]} pointer {eles[2]}"
            assembly_code = assemblyTable.map[key]
        elif eles[1] == "static":
            key = eles[0]+' '+'static'+' i'
            assembly_code = assemblyTable.map[key].replace('Foo',self.file.split('.')[0]).replace('i',eles[2])
        else:
            key = eles[0]+' '+eles[1]+' i'                              
            assembly_code = assemblyTable.map[key].replace('i',eles[2])
        return assembly_code

    def translateArithmetic(self,eles):
        key = eles[0]
        assembly_code = assemblyTable.map[key]
        if (key in self.compare_ops):
            assembly_code = assembly_code.replace('{}',str(self.compare_counter))
            self.compare_counter += 1
        return assembly_code

    def translateLabel(self,eles):
        key = eles[0]+' '+'label_name'
        assembly_code = assemblyTable.map[key].replace('label_name',eles[1]).replace('{}',str(self.label_counter))
        self.label_counter += 1
        return assembly_code
    
    def translateFunction(self,eles):
        unique_id = self.file.split('.')[0]  + str(self.func_counter)
        if(eles[0] == "call"):
            key = eles[0]+' '+'function_name'+' nArgs'
            assembly_code = assemblyTable.map[key].replace('function_name',eles[1]).replace('nArgs',eles[2])
            assembly_code = assembly_code.replace('{}',unique_id)
        elif(eles[0] == "function"):
            key = eles[0]+' '+'function_name'+' nVars'
            assembly_code = assemblyTable.map[key].replace('function_name',eles[1]).replace('nVars',eles[2])    
            assembly_code = assembly_code.replace('{}',unique_id)
        elif(eles[0] == "return"):
            key = eles[0]
            assembly_code = assemblyTable.map[key]
            assembly_code = assembly_code.replace('{}',unique_id)
        self.func_counter += 1
        return assembly_code

    def translate(self):
        for command in self.commands:
            assembly_code = ""
            self.code.append("// " + command + "\n")
            eles = command.split(' ',2)
            if (self.isArithmetic(eles)):
                assembly_code = self.translateArithmetic(eles)
            elif(self.isMemory(eles)):
                if (self.isLATT(eles)):
                    assembly_code = self.translateLATT(eles)
                else:
                    assembly_code = self.translateOthers(eles)
            elif(self.isLabel(eles)):
                assembly_code = self.translateLabel(eles)
            elif(self.isFunction(eles)):
                assembly_code = self.translateFunction(eles)
            assembly_code = assembly_code.replace('@SP','@0')
            assembly_code = assembly_code.replace('@LCL','@1')
            assembly_code = assembly_code.replace('@ARG','@2')
            assembly_code = assembly_code.replace('@THIS','@3')
            assembly_code = assembly_code.replace('@THAT','@4')
            self.code.append(assembly_code)

    def inintialize(self):
        self.code.append("@256 \nD=A \n@0 \nM=D \n")
        self.code.append("@returnAddress_Sysinit \nD=A \n@0 \nA=M \nM=D \n@0 \nM=M+1 \n@1 \nD=M \n@0 \nA=M \nM=D \n@0 \nM=M+1 \n@2 \nD=M \n@0 \nA=M \nM=D \n@0 \nM=M+1 \n@3 \nD=M \n@0 \nA=M \nM=D \n@0 \nM=M+1 \n@4 \nD=M \n@0 \nA=M \nM=D \n@0 \nM=M+1 \n@5 \nD=A \n@0 \nD=D+A \n@0 \nD=M-D \n@2 \nM=D \n@0 \nD=M \n@1 \nM=D \n@Sys.init \n0;JMP \n(returnAddress_Sysinit) \n")
        
    
            
            