import pymem
import re

CSGO_EXE = 'csgo.exe'
CLIENT_DLL = 'client.dll'
BYTE_PATTERN = rb'\x33\xC0\x83\xFA.\xB9\x20'

def toggle_wireframe(pm, address, enable):
    try:
        new_value = 2 if enable else 1
        pm.write_uchar(address, new_value)
        print(f"Wireframe {'enabled' if enable else 'disabled'}.")
    except pymem.exception.MemoryReadError:
        print("Error reading memory.")
    except pymem.exception.MemoryWriteError:
        print("Error writing memory.")

def main():
    try:
        pm = pymem.Pymem(CSGO_EXE)
        client = pymem.process.module_from_name(pm.process_handle, CLIENT_DLL)

        client_module = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        match = re.search(BYTE_PATTERN, client_module)
        
        if not match:
            print("Byte pattern not found.")
            return
        
        address = client.lpBaseOfDll + match.start() + 4
        
        while True:
            user_input = input("Enter 'on' to enable wireframe, 'off' to disable, or 'exit' to quit: ").strip().lower()

            if user_input == 'off':
                toggle_wireframe(pm, address, True)
            elif user_input == 'on':
                toggle_wireframe(pm, address, False)
            elif user_input == 'exit':
                print("Exiting...")
                break
            else:
                print("Invalid input. Please enter 'on', 'off', or 'exit'.")

    except pymem.exception.ProcessNotFound:
        print(f'{CSGO_EXE} process not found')
    except pymem.exception.ProcessError:
        print(f'Error accessing process {CSGO_EXE}')
    except pymem.exception.ModuleNotFound:
        print(f'{CLIENT_DLL} module not found')
    except pymem.exception.MemoryReadError:
        print('Error reading memory')
    except pymem.exception.MemoryWriteError:
        print('Error writing memory')
    except AttributeError:
        print('Byte pattern not found')

if __name__ == "__main__":
    main()
