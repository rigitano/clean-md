# Delete all current representations
set num_reps [molinfo top get numreps]
for {set i 0} {$i < $num_reps} {incr i} {
    mol delrep 0 top
}







#UNSELECTED IS GRAY

# See protein as licorice
mol selection {all}
mol representation Licorice
mol color ColorID 2 ;# grey
mol material Transparent
mol addrep top

# Add a cartoon representation for the backbone
mol selection {protein}
mol representation NewCartoon
mol color ColorID 2 ;# grey
mol material Transparent
mol addrep top



#SELECTED IS RED

# Beta strands (Extended beta)
mol color ColorID 1 ;# red
mol representation Licorice
mol selection {(resname PRO CYS) or (name CA) or (element S) or (index 1 2 3)}
mol material Opaque
mol addrep top





