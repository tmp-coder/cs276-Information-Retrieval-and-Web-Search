
from submission.ascore import * #modified
class CosineSimilarityScorer(AScorer):

    def __init__(self, idf, query_dict, params, query_weight_scheme=None, doc_weight_scheme=None): #Modified
        # query_dict is unnecessary for CosineSimilarityScorer,
        # but it's useful for child class SmallestWindowScorer
        super().__init__(idf, query_weight_scheme=query_weight_scheme, doc_weight_scheme=doc_weight_scheme) #Modified
        self.url_weight = params["url_weight"]
        self.title_weight  = params["title_weight"]
        self.body_hits_weight = params["body_hits_weight"]
        self.header_weight = params["header_weight"]
        self.anchor_weight = params["anchor_weight"]
        self.smoothing_body_length = params["smoothing_body_length"]
        self.weight = {
            "url": self.url_weight,
            "title": self.title_weight,
            "body_hits": self.body_hits_weight,
            "header": self.header_weight,
            "anchor": self.anchor_weight,
        }
        
        
    def get_net_score(self, q, query_vec, d, doc_vec):
        """ calculate net score
        Args:
            q (Query) : the query
            query_vec (dict) : the query vector
            d (Document) : the document
            doc_vec (dict) : the document vector
        Return:
            score (float) : the net score
        """
        ### Begin your code
        score =0
        for term in set(q.query_words):
            for parse_type in doc_vec:
                score += self.weight[parse_type] * doc_vec[parse_type][term] * query_vec[term]
        ### End your code
        return score
    
    
    ## Normalization
    def L1_normalize_doc_vec(self, q, d, doc_vec): 
        """ Normalize the doc vector
        Note that we should give uniform normalization to all fields
        as discussed in Session V.2 Document vector - Normalization.
        Args: 
            q (Query) : the query
            d (Document) : the document
            doc_vec (dict) : the doc vector
        Return:
            doc_vec (dict) : the doc vector after normalization
        """
        ### Begin your code
        norm_docvec = {}
        for k in doc_vec:
            norm_docvec[k] = dict(list(map(lambda x : (x,doc_vec[k][x] / (self.smoothing_body_length + d.body_length)), doc_vec[k].keys())))
        ### End your code    
        
        return norm_docvec
        
    def get_sim_score(self, q, d):
        """ Get the similarity score between a document and a query.
        Args:
            q (Query) : the query
            d (Document) : the document
            
        Return: the similarity score of q and d
        """
        query_vec = self.get_query_vector(q) 
        # Define normalizattion functon here or directly pass in normalize_func as shown in below cell
        self.doc_weight_scheme['norm'] = self.L1_normalize_doc_vec #modified
        # Normalization
        norm_doc_vec = self.get_doc_vector(q, d, self.doc_weight_scheme) #modified
        return self.get_net_score(q, query_vec, d, norm_doc_vec)