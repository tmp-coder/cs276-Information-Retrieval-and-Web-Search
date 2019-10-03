class BSBIIndex(BSBIIndex):
    def invert_write(self, td_pairs, index):
        """Inverts td_pairs into postings_lists and writes them to the given index
        
        Parameters
        ----------
        td_pairs: List[Tuple[Int, Int]]
            List of termID-docID pairs
        index: InvertedIndexWriter
            Inverted index on disk corresponding to the block       
        """
        ### Begin your code
        sorted_td = sorted(td_pairs)
        cur_term = sorted_td[0][0]
        posting_list = []
        for i in range(len(sorted_td)):
            if sorted_td[i][0] !=cur_term:
#                 print(cur_term,posting_list)
                index.append(cur_term,posting_list)
                cur_term = sorted_td[i][0]
                posting_list=[sorted_td[i][1]]
            elif len(posting_list)==0 or posting_list[-1] != sorted_td[i][1]:
                posting_list.append(sorted_td[i][1])
        index.append(cur_term,posting_list)
        ### End your code