$(document).ready(function() {

  chain_input_options = {
    tags: true,
    placeholder: "Type in chain IDs from PDB...",
    maximumInputLength: 1,
    tokenSeparators: [',', ' ']
  }

  $('#first_pdb_chains').select2(chain_input_options);
  $('#second_pdb_chains').select2(chain_input_options);

});
