#delete all current representations
set num_reps [molinfo top get numreps]
for {set i 0} {$i < $num_reps} {incr i} {
    mol delrep 0 top
}
    


# Add a cartoon representation for the backbone
mol selection "all"
mol representation NewCartoon

mol selection "extended_beta"
mol color ColorID 1 ;# Red
mol material Opaque
mol addrep top

mol selection "bridge_beta" #Single hydrogen-bonded beta-strand pairs
mol color ColorID 4 ;# yellow
mol material Opaque
mol addrep top

#now, colores for each type of scructure
mol selection "alpha_helix"
mol color ColorID 0 ;# Blue
mol material Opaque
mol addrep top

mol selection "helix_3_10"
mol color ColorID 10 ;# cyan
mol material Opaque
mol addrep top

mol selection "pi_helix"
mol color ColorID 11 ;# purple
mol material Opaque
mol addrep top

mol selection "coil" # Unstructured random regions
mol color ColorID 8 ;# white
mol material Opaque
mol addrep top

mol selection "turn" # change direction by a well defined pattern of h bonds
mol color ColorID 17 ;# pale yellow
mol material Opaque
mol addrep top


#now highlight some important aminoacids

# Prolines
mol representation Licorice
mol selection "resname PRO"
mol color ColorID 7 ;# green
mol material Opaque
mol addrep top

# Cysteines
mol representation Licorice
mol selection "resname CYS"
mol color ColorID 3 ;# orange
mol material Opaque
mol addrep top