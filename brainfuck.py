# A brainfuck to x86/Linux assembly compiler.

class CompilationError(Exception):
    '''Sigals a fatal error compiling the source.'''
    pass

class Compiler(object):
    def __init__(self):
        pass

    def compile(self, input, cells):
        '''Compile the input stream into an output string and return it.'''
        self.loops = []
        self.loop_number = 0
        self.inc_ptr_count = 0
        self.dec_ptr_count = 0
        code = ''

        for line in input:
            for c in line:
                if c in instructions:
                    code += self._emit_instruction(c)

        if len(self.loops) > 0:
            raise CompilationError('[ without corresponding ]')

        return boilerplate % {'cells': cells, 'code': code}

    def _emit_instruction(self, instr):
        '''Generate the code for a single instruction.'''
        if instr is '<':
            return dec_ptr
        elif instr is '>':
            return inc_ptr
        elif instr is '+':
            return inc_cell
        elif instr is '-':
            return dec_cell
        elif instr is ',':
            return in_byte
        elif instr is '.':
            return out_byte
        elif instr is '[':
            self.loop_number += 1
            self.loops.append(self.loop_number)
            return start_loop % {'loop_num': self.loop_number}
        elif instr is ']':
            if len(self.loops) > 0:
                num = self.loops.pop()
                return end_loop % {'loop_num': num}
            else:
                raise CompilationError('] without corresponding [')

# Valid brainfuck instructions.
instructions = ['<', '>', '+', '-', ',', '.', '[', ']']

# Assembly code templates for each instruction.
boilerplate = '''
.data
    .align 4
    cells: .space %(cells)d, 0
    char: .byte 0

.text
    .align 4

.globl _start
_start:
    movl $cells, %%eax
    movl $char, %%ecx
%(code)s
exit:
    movl $1, %%eax
    xorl %%ebx, %%ebx
    int $0x80

getbyte:
    pushl %%eax
    movl $3, %%eax
    xorl %%ebx, %%ebx
    movl $1, %%edx
    int $0x80
    movl 0(%%ecx), %%ebx
    popl %%eax
    movl %%ebx, 0(%%eax)
    ret

putbyte:
    push %%eax
    movl 0(%%eax), %%eax
    movl %%eax, 0(%%ecx)
    movl $4, %%eax
    movl $1, %%ebx
    movl $1, %%edx
    int $0x80
    pop %%eax
    ret
'''
# +
inc_ptr = '''
    incl %eax
'''
# -
dec_ptr = '''
    decl %eax
'''
# >
inc_cell = '''
    incb 0(%eax)
'''
# <
dec_cell = '''
    decb 0(%eax)
'''
# ,
in_byte = '''
    call getbyte
'''
# .
out_byte = '''
    call putbyte
'''
# [
start_loop = '''
loop_%(loop_num)d:
    cmpb $0, 0(%%eax)
    je end_loop_%(loop_num)d
'''
# ]
end_loop = '''
    jmp loop_%(loop_num)d
end_loop_%(loop_num)d:
'''
