import assemble
import string


GENERAL_REGISTERS = [
    'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi'
]


ALL_REGISTERS = GENERAL_REGISTERS + [
    'esp', 'eip', 'ebp'
]


class GadgetSearch(object):
    def __init__(self, dump_path, start_addr):
        """
        Construct the GadgetSearch object.

        Input:
            dump_path: The path to the memory dump file created with GDB.
            start_addr: The starting memory address of this dump.
        """

        #self.dump_path = dump_path
        #self.start_addr = start_addr

        self.dump = open(dump_path, "rb").read ()
        self.start_addr = start_addr

        #self.dump.seek(start_addr)
        #raise NotImplementedError()

    def get_format_count(self, gadget_format):
        """
        Get how many different register placeholders are in the pattern.
        
        Examples:
            self.get_format_count('POP ebx')
            => 0
            self.get_format_count('POP {0}')
            => 1
            self.get_format_count('XOR {0}, {0}; ADD {0}, {1}')
            => 2
        """
        # Hint: Use the string.Formatter().parse method:
        #   import string
        #   print string.Formatter().parse(gadget_format)

        iter = string.Formatter().parse(gadget_format)
        mylist = []
        for x in iter:
            for i in x:
                if i!=None and i.isdigit() and not(int(i) in mylist):
                    mylist.append(int(i))

        return len(mylist)

        #raise NotImplementedError()

    def xuniqueCombinations(self, items, n):
        if n==0: yield []
        else:
            for i in xrange(len(items)):
                for cc in self.xuniqueCombinations(items[i:],n-1):
                    yield [items[i]]+cc
                    yield cc + [items[i]]

    def get_register_combos(self, nregs, registers):
        """
        Return all the combinations of `registers` with `nregs` registers in
        each combination. Duplicates ARE allowed!

        Example:
            self.get_register_combos(2, ('eax', 'ebx'))
            => [['eax', 'eax'],
                ['eax', 'ebx'],
                ['ebx', 'eax'],
                ['ebx', 'ebx']]
        """

        
        res = []
        for x in self.xuniqueCombinations(registers,nregs):
            res.append(x)

        unique = []
        [unique.append(item) for item in res if item not in unique]    
        return unique







    def format_all_gadgets(self, gadget_format, registers):
        """
        Format all the possible gadgets for this format with the given
        registers.

        Example:
            self.format_all_gadgets("POP {0}; ADD {0}, {1}", ('eax', 'ecx'))
            => ['POP eax; ADD eax, eax',
                'POP eax; ADD eax, ecx',
                'POP ecx; ADD ecx, eax',
                'POP ecx; ADD ecx, ecx']
        """
        # Hints:
        # 1. Use the format function:
        #    'Hi {0}! I am {1}, you are {0}'.format('Luke', 'Vader')
        #    => 'Hi Luke! I am Vader, you are Luke'
        # 2. You can use an array instead of specifying each argument. Use the
        #    internet, the force is strong with StackOverflow.
        nregs = self.get_format_count(gadget_format)
        all_combinations = self.get_register_combos(nregs, registers)
        res = []
        for i in range(0, len(all_combinations)):
            string = gadget_format.format(*all_combinations[i])
            res.append (string)

        return res
        #raise NotImplementedError()

    def find_all(self, gadget):
        """
        Return all the addresses of the gadget inside the memory dump.

        Example:
            self.find_all('POP eax')
            => < all ABSOLUTE addresses in memory of 'POP eax; RET' >
        """
        # Notes:
        # 1. Addresses are ABSOLUTE (for example, 0x08403214), NOT RELATIVE to the
        #    beginning of the file (for example, 12).
        # 2. Don't forget to add the 'RET'

        data_to_search = assemble.assemble_data (gadget + ';RET')

        dump = self.dump
        start = self.start_addr

        addresses = []

        offset = 0
        while offset < len(dump):
            #offset = dump[i:].find (data_to_search)
            offset = dump.find (data_to_search, offset)

            address = '%08x' % (start + offset)
            if (offset == -1):
                break
            if (not (address in addresses)):
                addresses.append(address)
            offset += len (data_to_search)
            #print '{0}, {1}'.format(offset, len(dump))

        #self.dump.close()
        return addresses

        #raise NotImplementedError()

    def find(self, gadget, condition=None):
        """
        Return the first result of find_all. If condition is specified, only
        consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(addr for addr in self.find_all(gadget) if condition(addr))
        except StopIteration:
            raise ValueError("Couldn't find matching address for " + gadget)

    def find_all_formats(self, gadget_format, registers=GENERAL_REGISTERS):
        """
        Similar to find_all - but return all the addresses of all
        possible gadgets that can be created with this format and registers.
        Every elemnt in the result will be a tuple of the gadget string and
        the address in which it appears.

        Example:
            self.find_all_formats('POP {0}; POP {1}')
            => [('POP eax; POP ebx', address1),
                ('POP ecx; POP esi', address2),
                ...]
        """
        gadgets = self.format_all_gadgets(gadget_format, registers)
        res = []

        for i in  range (0, len(gadgets)):
            address = self.find_all (gadgets[i])
            for j in range(0, len(address)):
                pair = [gadgets[i], address[j]]
                res.append (tuple(pair))
        return res
        #raise NotImplementedError()

    def find_format(self, gadget_format, registers=GENERAL_REGISTERS, condition=None):
        """
        Return the first result of find_all_formats. If condition is specified,
        only consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(
                addr for addr in self.find_all_formats(gadget_format, registers)
                if condition(addr))
        except StopIteration:
            raise ValueError(
                "Couldn't find matching address for " + gadget_format)
