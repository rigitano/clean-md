# Define hydrophobic and hydrophilic residues
set hydrophobic_residues "ALA VAL LEU ILE MET PHE TRP PRO"
set hydrophilic_residues "ARG ASN ASP GLN GLU HIS LYS SER THR TYR CYS"

# Create representations for hydrophobic residues
set sel_hydrophobic [atomselect top "resname $hydrophobic_residues"]
mol selection "resname $hydrophobic_residues"
mol representation Licorice
mol color ColorID 4 ;# yellow
mol material Goodsell
mol addrep top

# Create representations for hydrophilic residues
set sel_hydrophilic [atomselect top "resname $hydrophilic_residues"]
mol selection "resname $hydrophilic_residues"
mol representation Licorice
mol color ColorID 11 ;# purple
mol material Goodsell
mol addrep top

# Update VMD display
$sel_hydrophobic delete
$sel_hydrophilic delete


# Add a cartoon representation to show the backbone
mol representation NewCartoon
mol color ColorID 2 ;# grey
mol material Goodsell
mol addrep top