class BSBIIndex(BSBIIndex):
    def retrieve(self, query):
        """Retrieves the documents corresponding to the conjunctive query
        
        Parameters
        ----------
        query: str
            Space separated list of query tokens
            
        Result
        ------
        List[str]
            Sorted list of documents which contains each of the query tokens. 
            Should be empty if no documents are found.
        
        Should NOT throw errors for terms not in corpus
        """
        if len(self.term_id_map) == 0 or len(self.doc_id_map) == 0:
            self.load()

        ### Begin your code
        tokens = query.strip().split()
        if len(tokens) ==0:
            return []
        terms = list(map(lambda x : self.term_id_map[x],tokens))
        
        ret =[]
        with InvertedIndexMapper(self.index_name, directory=self.output_dir, 
                                 postings_encoding=
                                 self.postings_encoding) as mapper:
            ret.extend(mapper[terms[0]])
#             assert(len(set(ret)) == len(ret)),ret
            for i in range(1,len(terms)):
                ret = sorted_intersect(ret,mapper[terms[i]])
        return sorted(list(map(lambda x : self.doc_id_map[x],ret)))
             
#         with InvertedIndexMapper('test',directory='tmp/') as mapper:
        ### End your code