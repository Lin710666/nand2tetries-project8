map = {
    #内存分配指令
    "push segment i": "@segmentPointer \nD=M \n@i \nD=D+A \n@addr \nM=D \nA=M \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n",
    "pop segment i": "@segmentPointer \nD=M \n@i \nD=D+A \n@addr \nM=D \n@SP \nM=M-1 \n@SP \nA=M \nD=M \n@addr \nA=M \nM=D \n",

    "push constant i": "@i \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n",

    "pop static i": "@SP \nAM=M-1 \nD=M \n@Foo.i \nM=D \n",
    "push static i": "@Foo.i \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n",

    "push temp i": "@5 \nD=A \n@i \nD=D+A \n@addr \nM=D \nA=M \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n",
    "pop temp i": "@5 \nD=A \n@i \nD=D+A \n@addr \nM=D \n@SP \nM=M-1 \n@SP \nA=M \nD=M \n@addr \nA=M \nM=D \n",

    "push pointer 0": "@THIS \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n",
    "push pointer 1": "@THAT \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n",
    "pop pointer 0": "@SP \nM=M-1 \n@SP \nA=M \nD=M \n@THIS \nM=D \n",
    "pop pointer 1": "@SP \nM=M-1 \n@SP \nA=M \nD=M \n@THAT \nM=D \n",

    # 算术指令
    "add": "@SP \nAM=M-1 \nD=M \nA=A-1 \nM=M+D \n",
    "sub": "@SP \nAM=M-1 \nD=M \nA=A-1 \nM=M-D \n",
    "and": "@SP \nAM=M-1 \nD=M \nA=A-1 \nM=D&M \n",
    "or": "@SP \nAM=M-1 \nD=M \nA=A-1 \nM=D|M \n",
    
    
    "neg": "@SP \nA=M-1 \nM=-M \n",
    "not": "@SP \nA=M-1 \nM=!M \n",
    
    
    "eq": 
        "@SP \nAM=M-1 \nD=M \n@SP \nA=M-1 \nD=M-D \n@EQ_TRUE_{} \nD;JEQ \n@SP \nA=M-1 \nM=0 \n@EQ_END_{} \n0;JMP \n(EQ_TRUE_{}) \n@SP \nA=M-1 \nM=-1 \n(EQ_END_{}) \n"
    ,
    "gt": 
        "@SP \nAM=M-1 \nD=M \n@SP \nA=M-1 \nD=M-D \n@GT_TRUE_{} \nD;JGT \n@SP \nA=M-1 \nM=0 \n@GT_END_{} \n0;JMP \n(GT_TRUE_{}) \n@SP \nA=M-1 \nM=-1 \n(GT_END_{}) \n"
    ,
    "lt": 
        "@SP \nAM=M-1 \nD=M \n@SP \nA=M-1 \nD=M-D \n@LT_TRUE_{} \nD;JLT \n@SP \nA=M-1 \nM=0 \n@LT_END_{} \n0;JMP \n(LT_TRUE_{}) \n@SP \nA=M-1 \nM=-1 \n(LT_END_{}) \n"
    ,

    #分支指令
    "label label_name": "(label_name) \n",
    "goto label_name": "@label_name \n0;JMP \n",
    "if-goto label_name": "@SP \nAM=M-1 \nD=M \n@label_name \nD;JNE \n",

    #函数指令
    "call function_name nArgs": "@returnAddress_{} \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n@LCL \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n@ARG \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n@THIS \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n@THAT \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n@5 \nD=A \n@nArgs \nD=D+A \n@SP \nD=M-D \n@ARG \nM=D \n@SP \nD=M \n@LCL \nM=D \n@function_name \n0;JMP \n(returnAddress_{}) \n",
    "function function_name nVars": "(function_name) \n@nVars \nD=A \n@VarCounter_{} \nM=D \nD=M \n@LOOP_{} \nD;JGT \n@END_{} \n0;JMP \n(LOOP_{}) \n@0 \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1 \n@VarCounter_{} \nMD=M-1 \n@LOOP_{} \nD;JGT \n(END_{}) \n",
    "return": "@LCL \nD=M \n@endFrame_{} \nM=D \n@5 \nD=A \n@endFrame_{} \nA=M-D \nD=M \n@retAddr_{} \nM=D \n@SP \nAM=M-1 \nD=M \n@ARG \nA=M \nM=D \n@ARG \nD=M+1 \n@SP \nM=D \n@1 \nD=A \n@endFrame_{} \nA=M-D \nD=M \n@THAT \nM=D \n@2 \nD=A \n@endFrame_{} \nA=M-D \nD=M \n@THIS \nM=D \n@3 \nD=A \n@endFrame_{} \nA=M-D \nD=M \n@ARG \nM=D \n@4 \nD=A \n@endFrame_{} \nA=M-D \nD=M \n@LCL \nM=D \n@retAddr_{} \nA=M \n0;JMP \n",
}


