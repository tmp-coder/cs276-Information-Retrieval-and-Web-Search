
import heapq
class BSBIIndex(BSBIIndex):
    def merge(self, indices, merged_index,buffur_size=1024*1024):
        """Merges multiple inverted indices into a single index
        
        Parameters
        ----------
        indices: List[InvertedIndexIterator]
            A list of InvertedIndexIterator objects, each representing an
            iterable inverted index for a block
        merged_index: InvertedIndexWriter
            An instance of InvertedIndexWriter object into which each merged 
            postings list is written out one at a time
        """
        ### Begin your code
        cur_term=None
        buffer= []
    
        for merged_item in heapq.merge(*indices,key=lambda x : x[0]):
            if cur_term is None or cur_term == merged_item[0]:
                cur_term = merged_item[0]
                buffer.extend(merged_item[1])
            else :
                merged_index.append(cur_term,buffer)
                cur_term = merged_item[0]
                buffer=[]
                buffer.extend(merged_item[1])
            
            if len(buffer) > buffur_size:
                merged_index.append(cur_term,buffer)
                buffer = []
                
        ### End your code