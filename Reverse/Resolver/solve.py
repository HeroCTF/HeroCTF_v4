def ROR(x, n, bits=32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))


def ROL(x, n, bits=32):
    return ROR(x, bits - n, bits)


def compute_checksum(function_name):
    sum = 0
    for c in function_name:
        c = ord(c)
        sum = ROL(sum, 0xE)
        if c < 0x61:
           sum += c
        else:
            sum += (c - 0x20)
    return sum
 
result = {}

def main():
    export_table = open('kernel32_exports.txt', 'r')

    for line in export_table:
        function = line.split()[0]
        if function in ["GetDateFormatWWorker", "IsWow64GuestMachineSupported", "SetThreadPreferredUILanguages"]:
            hash = hex(compute_checksum(function))
            result[function] = hash
    export_table.close()
    
    print(f"[+] Result: {result}")
    print("[+] Flag: Hero{" + f"{result['GetDateFormatWWorker']}:{result['IsWow64GuestMachineSupported']}:{result['SetThreadPreferredUILanguages']}" + "}")


if __name__ == '__main__':
    main()
