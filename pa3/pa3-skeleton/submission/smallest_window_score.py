from submission.cosine_score import * #modified
from submission.bm25f_score import * #modified
class SmallestWindowScorer(BM25FScorer): 
    """
     A skeleton for implementing the Smallest Window scorer in Task 3.
     Note: The class provided in the skeleton code extends BM25Scorer in Task 2. 
     However, you don't necessarily have to use Task 2. (You could also use Task 1, 
     in which case, you'd probably like to extend CosineSimilarityScorer instead.)
     Also, feel free to modify or add helpers inside this class.
     
     Note: If you plan to use cosine similarity scorer
             - change parent class to CosineSimilarityScorer 
             - change normalization method in get_sim_score 
    """
    def __init__(self, idf, query_dict, params, query_weight_scheme=None, doc_weight_scheme=None): #modified
        super().__init__(idf, query_dict, params, query_weight_scheme=query_weight_scheme, doc_weight_scheme=doc_weight_scheme) #modified
        self.query_dict = query_dict
        
        # smallest window specific weights
        self.B = params["B"]
    
    # Write helper functions here
    ### Begin your code

    ### End your code
        
    def get_boost_score(self, q, d):
        """ calculate boost score based on smallest window size"""
        ### Begin your code

        ### End your code
    

    def get_sim_score(self, q, d):
        """ Get the similarity score between a document and a query.
        Args:
            d (Document) : the document
            q (Query) : the query
            
        Return:
            the raw similarity score times boost
        """
        boost = self.get_boost_score(q, d)
        query_vec = self.get_query_vector(q)
        # Define normalizattion functon here or directly pass in normalize_func as shown in below cell
        # Depends on which parent class you are using 
        self.doc_weight_scheme['norm'] = self.bm25f_normalize_doc_vec #modified
        norm_doc_vec = self.get_doc_vector(q, d, self.doc_weight_scheme) #modified
        raw_score = self.get_net_score(q, query_vec, d, norm_doc_vec)
       
        return boost * raw_score