import getpass
from . import camelot_stream_hdfc, camelot_stream_au, camelot_stream_kotak, camelot_lattice_axis, camelot_lattice_idbi, camelot_lattice_canara, camelot_lattice_iob

def choose_bank(file, bank_name, password):
    """banks = ["HDFC Bank", "AU Small Finance Bank", "Kotak Bank", "Axis Bank", "IDBI Bank", "Canara Bank", "Indian Overseas Bank"]
    
    print("Please choose a bank:")
    for i, bank in enumerate(banks, start=1):
        print(f"{i}. {bank}")
    
    choice = int(input("Enter the number corresponding to your bank: "))
    
    if 1 <= choice <= len(banks):
        selected_bank = banks[choice - 1]
        print(f"You selected: {selected_bank}")
    else:
        print("Invalid choice. Please try again.")"""

    if bank_name == 'hdfc':
        camelot_stream_hdfc.parse_pdf(file, password)
    elif bank_name == 'AU Bank':
        camelot_stream_au.parse_pdf(file, password)
    elif bank_name == 'Kotak Bank':
        camelot_stream_kotak.parse_pdf(file, password)
    elif bank_name == 'Axis Bank':
        camelot_lattice_axis.parse_pdf(file, password)
    elif bank_name == 'IDBI Bank':
        camelot_lattice_idbi.parse_pdf(file, password)
    elif bank_name == 'Canara Bank':
        camelot_lattice_canara.parse_pdf(file, password)
    elif bank_name == 'Indian Overseas Bank':
        camelot_lattice_iob.parse_pdf(file, password)
    else:
        pass
