class InvertedIndexWriter(InvertedIndex):
    """"""
    def __enter__(self):
        self.index_file = open(self.index_file_path, 'wb+')              
        return self

    def append(self, term, postings_list):
        """Appends the term and postings_list to end of the index file.
        
        This function does three things, 
        1. Encodes the postings_list using self.postings_encoding
        2. Stores metadata in the form of self.terms and self.postings_dict
           Note that self.postings_dict maps termID to a 3 tuple of 
           (start_position_in_index_file, 
           number_of_postings_in_list, 
           length_in_bytes_of_postings_list)
        3. Appends the bytestream to the index file on disk

        Hint: You might find it helpful to read the Python I/O docs
        (https://docs.python.org/3/tutorial/inputoutput.html) for
        information about appending to the end of a file.
        
        Parameters
        ----------
        term:
            term or termID is the unique identifier for the term
        postings_list: List[Int]
            List of docIDs where the term appears
        """
        ### Begin your code
        postings_list_encode = self.postings_encoding.encode(postings_list)
        if self.postings_dict.get(term) is None:
            self.terms.append(term)
    #         print(term,postings_list)
    #         print(len(postings_list_encode))
            self.postings_dict[term] = (self.index_file.tell(),len(postings_list),len(postings_list_encode))
        else:
            assert self.terms[-1]==term,"the term has been inserted"
            start_pos,l1,l2 = self.postings_dict[term]
            self.postings_dict[term] = (start_pos,l1+len(postings_list),l2+len(postings_list_encode))
        self.index_file.write(postings_list_encode)
        ### End your code