# See protein as licorice
mol selection "protein"
mol representation Licorice
mol color Type ;# by atom type
mol material Goodsell
mol addrep top

# Add a cartoon representation for the backbone
mol selection "protein"
mol representation NewCartoon
mol color ColorID 2 ;# grey
mol material Goodsell
mol addrep top

# Visualize molecules within hydrogen bond range of the protein

mol selection "not protein within 3.5 of protein"
mol representation Licorice
mol color Name
mol material Opaque
mol addrep top

# Visualize hydrogen bonds using Hbonds drawing method
mol selection "protein"
mol representation Hbonds
mol color ColorID 27 ;# magenta
mol material Opaque
mol addrep top