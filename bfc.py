# Command-line interface for a brainfuck to x86/Linux assembly compiler.

import sys, getopt
import brainfuck

def usage():
    print 'Usage:', sys.argv[0], '[options] file'

def help():
    usage()
    print 'Options:'
    print '  -o --output SFILE  name the assembly-file output SFILE (default bf.s)'
    print '  -c --cells CELLS   number of memory cells (default 30000)'
    print '  -h --help          show this message and exit'

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ho:c:', ['help', 'output', 'cells'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    output = 'bf.s'
    cells = 30000
    for o, a in opts:
        if o in ('-o', '--output'):
            output = a
        if o in ('-c', '--cells'):
            try:
                cells = int(a)
            except ValueError:
                print 'Cells is not a number'
                sys.exit()
            if cells <= 0:
                print 'Cells must be greater than zero'
                sys.exit()
        elif o in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) != 1:
        usage()
        sys.exit()
    input = args[0]

    try:
        in_file = open(input, 'r')
        out_file = open(output, 'w')

        compiler = brainfuck.Compiler()
        output = compiler.compile(in_file, cells)
        out_file.write(output)

        in_file.close()
        out_file.close()
    except brainfuck.CompilationError, e:
        print 'Compilation failed:', str(e)
        sys.exit(1)
    except IOError, e:
        print str(e)
        sys.exit(2)

if __name__ == '__main__':
    main()
