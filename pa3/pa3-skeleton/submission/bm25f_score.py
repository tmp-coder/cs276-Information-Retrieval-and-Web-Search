from submission.ascore import * #modified
import math
class BM25FScorer(AScorer):

    def __init__(self, idf, query_dict, params, query_weight_scheme=None, doc_weight_scheme=None): #modified
        super().__init__(idf, query_weight_scheme=query_weight_scheme, doc_weight_scheme=doc_weight_scheme) #modified
        self.query_dict = query_dict
        
        self.url_weight = params['url_weight']
        self.title_weight  = params['title_weight']
        self.body_hits_weight = params['body_hits_weight']
        self.header_weight = params['header_weight']
        self.anchor_weight = params['anchor_weight']
        # bm25 specific weights
        self.b_url = params['b_url']
        self.b_title = params['b_title']
        self.b_header = params['b_header']
        self.b_body_hits = params['b_body_hits']
        self.b_anchor = params['b_anchor']
        self.k1 = params['k1']
        self.pagerank_lambda = params['pagerank_lambda']
        self.pagerank_lambda_prime = params['pagerank_lambda_prime']
        self.__b = {
            "url":self.b_url,
            "title":self.b_title,
            "header":self.b_header,
            "body_hits":self.b_body_hits,
            "anchor": self.b_anchor,
        }
        self.weight = {
            "url":self.url_weight,
            "title": self.title_weight,
            "header": self.header_weight,
            "body_hits": self.body_hits_weight,
            "anchor": self.anchor_weight,
        }
        # BM25F data structures feel free to modify these
        # Document -> field -> length
        self.length = {}
        self.avg_length = {}
        # log func
        self.pagerank_scores = lambda x : math.log(self.pagerank_lambda_prime + 1+x) # sure it's positive
        
        self.calc_avg_length()
        
    def calc_avg_length(self):
        """ Set up average lengths for BM25F, also handling PageRank. 
        You need to 
        Initialize any data structures needed.
        Perform any preprocessing you would like to do on the fields.
        Handle pagerank
        Accumulate lengths of fields in documents. 
        Hint: You could use query_dict
        """
        ### Begin your code
        
        length_counter = lambda x : (sum(x.values()) if x else 0)
        
        for docs in self.query_dict.values():
            for _,doc in docs.items():
                if (doc.url not in self.length):
                    self.length[doc.url] = dict(list (map(lambda x : (x, length_counter(self.parse(x,doc))),self.TFTYPES )))
                    for k, v in self.length[doc.url].items():
                        self.avg_length[k] = self.avg_length.get(k,0) + v
        ### End your code
        
    def get_net_score(self, q, query_vec, d, doc_vec):
        """ Compute the overall score using above equation
        Args:
            q (Query) : the query
            query_vec (dict) : the query vector
            d (Document) : the document
            doc_vec (dict) : the doc vector
        Return:
            score (float) : the net score
        """
        ### Begin your code
        terms = set(q.query_words)
        wd = dict(list(map( lambda x : (x, sum([doc_vec[e][x] * self.weight[e] for e in doc_vec])),terms)))
        
        return  self.pagerank_scores(d.pagerank if d.pagerank else 0) * self.pagerank_lambda +sum([wd[t] / (self.k1 + wd[t]) * query_vec[t] for t in terms])
        ### End your code
        return score
    
    
    def bm25f_normalize_doc_vec(self, q, d, doc_vec):
        """ Normalize the raw term frequencies in fields in document d 
            using above equation (1).
        Args:
            q (Query) : the query       
            d (Document) : the document
            doc_vec (dict) : the doc vector
        Return: 
            doc_vec (dict) : the doc vector after normalization
        """
        ### Begin your code
        norm_vec = {}
        
        norm_func = lambda field_type,raw_tf : raw_tf / (1 + self.__b[field_type] * 
                                                         (self.length[d.url][field_type] / self.avg_length[field_type] -1)) if self.avg_length[field_type]> 0 else 0
        
        for f,v in doc_vec.items():
            norm_vec[f] = dict( list( map(lambda x :(x, norm_func(f,v[x])),set(q.query_words))))
        
        return norm_vec
        ### End your code    
        
    def get_sim_score(self, q, d):
        """ Get the similarity score between a document and a query.
        Args:
            d (Document) : the document
            q (Query) : the query
            
        Return:
            the similarity score
        """
        query_vec = self.get_query_vector(q)
        # Define normalizattion functon here or directly pass in normalize_func as shown in below cell
        self.doc_weight_scheme['norm'] = self.bm25f_normalize_doc_vec #modified
        norm_doc_vec = self.get_doc_vector(q, d, self.doc_weight_scheme) #modified
        # Normalization
        return self.get_net_score(q, query_vec, d, norm_doc_vec)