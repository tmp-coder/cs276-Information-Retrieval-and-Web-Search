class InvertedIndexIterator(InvertedIndex):
    """"""
    def __enter__(self):
        """Adds an initialization_hook to the __enter__ function of super class
        """
        super().__enter__()
        self._initialization_hook()
        return self
    
#     def __init__(self,index_name, postings_encoding=None, directory=''):
#         super().__init__(index_name,postings_encoding,directory)
#         self.term_idx=0

    def _initialization_hook(self):
        """Use this function to initialize the iterator
        """
        ### Begin your code
        self.index_file = open(self.index_file_path,"rb+")
        self.term_idx = 0
        ### End your code

    def __iter__(self): 
        return self
    
    def __next__(self):
        """Returns the next (term, postings_list) pair in the index.
        
        Note: This function should only read a small amount of data from the 
        index file. In particular, you should not try to maintain the full 
        index file in memory.
        """
        ### Begin your code
        if self.term_idx >= len(self.terms):
            raise StopIteration
        term = self.terms[self.term_idx]
        start_pos,_,nbytes = self.postings_dict[term]
        if start_pos != self.index_file.tell():
            self.index_file.seek(start_pos)
        posting_list_undecode = self.index_file.read(nbytes)
        postings_list = self.postings_encoding.decode(posting_list_undecode)
        self.term_idx+=1
        return (term,postings_list)
        ### End your code

    def delete_from_disk(self):
        """Marks the index for deletion upon exit. Useful for temporary indices
        """
        self.delete_upon_exit = True

    def __exit__(self, exception_type, exception_value, traceback):
        """Delete the index file upon exiting the context along with the
        functions of the super class __exit__ function"""
        self.index_file.close()
        if hasattr(self, 'delete_upon_exit') and self.delete_upon_exit:
            os.remove(self.index_file_path)
            os.remove(self.metadata_file_path)
        else:
            with open(self.metadata_file_path, 'wb') as f:
                pkl.dump([self.postings_dict, self.terms], f)