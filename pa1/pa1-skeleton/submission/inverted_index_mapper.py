class InvertedIndexMapper(InvertedIndex):
    def __getitem__(self, key):
        return self._get_postings_list(key)
    
    def _get_postings_list(self, term):
        """Gets a postings list (of docIds) for `term`.
        
        This function should not iterate through the index file.
        I.e., it should only have to read the bytes from the index file
        corresponding to the postings list for the requested term.
        """
        ### Begin your code
        start_pos, len_posting,nbytes = self.postings_dict[term]
#         print(term,nbytes)
        posting_uncode = []
        with open(self.index_file_path,"rb+") as f:
            f.seek(start_pos)
            posting_uncode = f.read(nbytes)
#             print(posting_uncode)
        posting_list = self.postings_encoding.decode(posting_uncode)
#         print(posting_list)
        return posting_list
            
        ### End your code