import socket

def send_to_vmd(command):
    with socket.create_connection(("localhost", 5555)) as sock:
        sock.sendall(command.encode('utf-8') + b'\n')
        response = sock.recv(1024)
        print("Response:", response.decode('utf-8'))



commands = [

# Create representation for hydrophobic residues
    'mol addrep top',  # Add representation slot. (its the first one, to the id is 0)
    'mol modselect 0 top "resname ALA VAL LEU ILE MET PHE TRP PRO"',
    'mol modstyle 0 top Licorice',
    'mol modcolor 0 top ColorID 4',  # Yellow
    'mol modmaterial 0 top Goodsell',

    # Create representation for hydrophilic residues
    'mol addrep top',  # Add representation slot (id is 1)
    'mol modselect 1 top "resname ARG ASN ASP GLN GLU HIS LYS SER THR TYR CYS"',
    'mol modstyle 1 top Licorice',
    'mol modcolor 1 top ColorID 11',  # Purple
    'mol modmaterial 1 top Goodsell',

    # Add cartoon representation for the backbone
    'mol addrep top',  # Add representation slot (id is 2)
    'mol modselect 2 top "all"',  # Select all atoms for the cartoon
    'mol modstyle 2 top NewCartoon',
    'mol modcolor 2 top ColorID 2',  # Grey
    'mol modmaterial 2 top Goodsell'


]

for command in commands:
    send_to_vmd(command)