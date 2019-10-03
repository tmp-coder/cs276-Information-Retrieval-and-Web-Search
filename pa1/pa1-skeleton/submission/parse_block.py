class BSBIIndex(BSBIIndex):            
    def parse_block(self, block_dir_relative):
        """Parses a tokenized text file into termID-docID pairs
        
        Parameters
        ----------
        block_dir_relative : str
            Relative Path to the directory that contains the files for the block
        
        Returns
        -------
        List[Tuple[Int, Int]]
            Returns all the td_pairs extracted from the block
        
        Should use self.term_id_map and self.doc_id_map to get termIDs and docIDs.
        These persist across calls to parse_block
        """
        ### Begin your code
        ret = []
        read_dir = os.path.join(self.data_dir,block_dir_relative)
#         print(read_dir)
        for dir_name, subdir,file_list in os.walk(read_dir):
            for fname in file_list:
#                 print(dir_name+" ",fname)
                read_path = os.path.join(dir_name,fname)
                with open(read_path,'r') as f:
                    for line in f:
                        for words in line.strip().split():
#                             print(words,self.term_id_map[words])
                            ret.append((self.term_id_map[words],self.doc_id_map[os.path.join(block_dir_relative,fname)])) # just for pass test in windows
                            
        return ret
        ### End your code