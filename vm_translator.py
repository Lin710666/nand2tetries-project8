import parser
import codeWriter
import assemblyTable
import sys
import os

def output(input,filename,initialzed):
    parser1 = parser.Parser(input)
    commands = parser1.get_code()

    codewriter = codeWriter.CodeWriter(commands,filename)
    if not initialzed:
        codewriter.inintialize()
        initialzed = True
    codewriter.translate()
    code = codewriter.code
    return code

def main():
    args = sys.argv
    initialzed = False
    code = []
    
    if os.path.isfile(args[1]):
        # 处理单个文件
        output_file = args[1].split('.')[0]+'.asm'
        code = output(args[1], args[1], initialzed)
        initialzed = True  # 标记已初始化
    elif os.path.isdir(args[1]):
        # 处理目录时只初始化一次
        output_file = args[1]+'.asm'
        init_cw = codeWriter.CodeWriter([], "")
        init_cw.inintialize()
        code.extend(init_cw.code)
        initialzed = True
        
        for file in os.listdir(args[1]):
            if file.endswith(".vm"):
                sub_code = output(os.path.join(args[1],file),file,initialzed)
                code.extend(sub_code)
                
            
#得到输出文件
    file = open(output_file, 'w')
    for line in code:
        file.write(line)
    file.close()

if __name__ == '__main__':
    main()

    
