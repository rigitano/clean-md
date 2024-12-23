# ----------------------------------------------------------------------
# VMD Tcl Script: resinfo_categorize_corrected.tcl
#
# Purpose:
#   For each loaded molecule in VMD, categorize residues based on predefined
#   selection keywords (e.g., protein, water, ion, lipid, nucleic, sugar).
#   For each category, list unique residue names along with the number of
#   atoms in a representative residue and the total count of such residues.
#
# Usage:
#   In the VMD Tk Console, execute:
#     source /path/to/resinfo_categorize_corrected.tcl
#
# ----------------------------------------------------------------------

# Define the list of category keywords. These should correspond to VMD's
# selection keywords and are case-insensitive.

set categories {protein lipid lipids nucleic sugar water waters ion ions }

# Function to initialize a list in an array if it doesn't exist
proc ensure_list_exists {array_name key} {
    # Link the array in the caller's scope
    upvar 1 $array_name array_ref
    if {![info exists array_ref($key)]} {
        set array_ref($key) [list]
    }
}

# Function to count atoms and residues for a given resname
proc get_residue_info {molID rname} {
    # Select all atoms with the given resname
    set sel [atomselect $molID "resname $rname"]
    
    # Get unique residue IDs (resid) to determine the number of residues
    set resid_list [lsort -unique [$sel get resid]]
    set num_residues [llength $resid_list]
    
    # If no residues found, return zeros
    if {$num_residues == 0} {
        $sel delete
        return [list 0 0]
    }
    
    # Select the first residue to count the number of atoms
    set first_resid [lindex $resid_list 0]
    set sel_first [atomselect $molID "resid $first_resid and resname $rname"]
    set num_atoms [$sel_first num]
    
    # Clean up selections
    $sel delete
    $sel_first delete
    
    return [list $num_atoms $num_residues]
}

# Main script execution
proc categorize_residues {categories} {
    # Retrieve the list of loaded molecules
    set molList [molinfo list]
    
    if {[llength $molList] == 0} {
        puts "No molecules loaded in VMD."
        return
    }
    
    # Iterate through each molecule
    foreach molID $molList {
        # Retrieve basic molecule information
        set filename   [molinfo $molID get filename]
        set molname    [molinfo $molID get name]
        set numFrames  [molinfo $molID get numframes]
        set numAtoms   [molinfo $molID get numatoms]
        
        # Print molecule header
        puts "\n============================================================"
        puts "Molecule ID:       $molID"
        puts "Molecule Name:     $molname"
        puts "Filename:          $filename"
        puts "Number of frames:  $numFrames"
        puts "Number of atoms:   $numAtoms"
        puts ""
        
        # Initialize a list to track categorized resnames
        set categorized_resnames {}
        
        # Initialize the categoryMap array to store categorized residues
        array set categoryMap {}
        
        # Iterate through each category keyword
        foreach category $categories {
            # Perform atom selection using the category keyword
            set sel_str $category
            set sel [atomselect $molID $sel_str]
            
            # Check if the selection has any atoms
            if {[$sel num] == 0} {
                $sel delete
                continue
            }
            
            # Get unique resnames from the selection
            set resnames [lsort -unique [$sel get resname]]
            $sel delete
            
            # Iterate through each resname
            foreach rname $resnames {
                # Skip if already categorized
                if {[lsearch -exact $categorized_resnames $rname] != -1} {
                    continue
                }
                
                # Get residue information
                lassign [get_residue_info $molID $rname] num_atoms num_residues
                
                # Create the entry string (all information on one line)
                set entry "resname: $rname, qt atoms: $num_atoms, total: $num_residues"
                
                # Ensure the category list exists in categoryMap
                ensure_list_exists categoryMap $category
                
                # Append the entry to the category using lappend
                lappend categoryMap($category) $entry
                
                # Mark the resname as categorized
                lappend categorized_resnames $rname
            }
        }
        
        # Assign remaining resnames to "other"
        # First, get all unique resnames in the molecule
        set all_sel [atomselect $molID "all"]
        set all_resnames [lsort -unique [$all_sel get resname]]
        $all_sel delete
        
        # Determine resnames not yet categorized
        set other_resnames {}
        foreach rname $all_resnames {
            if {[lsearch -exact $categorized_resnames $rname] == -1} {
                lappend other_resnames $rname
            }
        }
        
        # Process "other" resnames
        foreach rname $other_resnames {
            set info [get_residue_info $molID $rname]
            lassign $info num_atoms num_residues
            set entry "resname: $rname, qt atoms: $num_atoms, total: $num_residues"
            
            # Ensure the "other" category exists
            ensure_list_exists categoryMap "other"
            
            # Append the entry to "other" using lappend
            lappend categoryMap(other) $entry
        }
        
        # Print categorized residues
        puts "Unique resnames grouped by selection Singlewords that I like:"
        foreach cat [lsort [array names categoryMap]] {
            puts " selection Singleword : $cat"
            foreach item $categoryMap($cat) {
                puts "    $item"
            }
        }
        puts "============================================================\n"
    }
    
    # After processing all molecules, print the categorized residue information
}

# Execute the categorization
categorize_residues $categories
