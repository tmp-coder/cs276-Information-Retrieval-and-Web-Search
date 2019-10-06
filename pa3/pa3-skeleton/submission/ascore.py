import math
from collections import Counter
class AScorer:
    """ An abstract class for a scorer. 
        Implement query vector and doc vector.
        Needs to be extended by each specific implementation of scorers.
    """
    def __init__(self, idf, query_weight_scheme=None, doc_weight_scheme=None): #Modified
        self.idf = idf
        self.TFTYPES = ["url","title","body_hits","header","anchor"]
        
        self.default_query_weight_scheme = {"tf": 'b', "df": 't', "norm": None} # boolean, idf, none
        self.default_doc_weight_scheme = {"tf": 'n', "df": 'n', "norm": None}   # natural, none
        
        self.query_weight_scheme = query_weight_scheme if query_weight_scheme is not None \
                                   else self.default_query_weight_scheme #Modified (added)
        self.doc_weight_scheme = doc_weight_scheme if doc_weight_scheme is not None \
                                 else self.default_doc_weight_scheme #Modified (added)

    def get_sim_score(self, q, d):
        """ Score each document for each query.
        Args:
            q (Query): the Query
            d (Document) :the Document

        Returns:
            pass now, will be implement in task 1, 2 and 3
        """        
        raise NotImplementedError

    # Include any initialization and/or parsing methods that 
    # you may want to perform on the Document fields prior to accumulating counts.
    # See the Document class to see how the various fields are represented
    # We have provided a few parser functions for you. Feel free to change them, and add more if you find its useful

    ### Begin your code
    def parse(self,parser_type,doc,token=False):
        """
        helper function of parser
        
        doc : Docment
        parser_type: must be in self.TFTYPES
        """
        
        switch = {
            "url": lambda : (self.parse_url(doc.url,token) if doc.url else None ),
            "title":lambda : (self.parse_title(doc.title,token) if doc.title else None),
            "body_hits": lambda: (self.parse_body_hits(doc.body_hits) if doc.body_hits else None),
            "header":lambda: (self.parse_headers(doc.headers) if doc.headers else None),
            "anchor": lambda: (self.parse_anchors(doc.anchors) if doc.anchors else None),
        }
        
        return switch[parser_type]()
        
        
    ### End your code
    def parse_url(self, url, token=False):
        """Parse document's url. Return Counter of url's tokens"""
        # token indicate whether we want the raw token or Counter of it
        if url:
            url_token_in_term = url.replace("http:",".").replace('/','.').replace('?','.') \
                                   .replace('=','.').replace("%20",".").replace("...",".").replace("..",".")\
                                   .lower();
            url_token = url_token_in_term.split('.')[1:]
            if token:
                return url_token 
            else:
                return Counter(url_token)
        return Counter([])

    def parse_title(self, title, token=False):
        """Parse document's title. Return Counter of title's tokens"""
        if title:
            if token:
                return title.split(" ") 
            else:
                return Counter(title.split(" "))
        else:
            return Counter([])

    def parse_headers(self, headers):
        """Parse document's headers. Return Counter of headers' tokens"""
        headers_token = []
        if headers is not None:
            for header in headers:
                header_token = header.split(" ")
                headers_token.extend(header_token)
        return Counter(headers_token)

    def parse_anchors(self, anchors):
        """Parse document's anchors. Return Counter of anchors' tokens"""
        anchor_count_map = Counter({})
        if anchors is not None:
            for anchor in anchors:
                count = anchors[anchor]
                anchor_tokens = anchor.split(" ")
                for anchor_token in anchor_tokens:
                    if(anchor_token in anchor_count_map.keys()):
                        anchor_count_map[anchor_token] += count
                    else:
                        anchor_count_map[anchor_token] = count           
        return anchor_count_map
 
    def parse_body_hits(self, body_hits):
        """Parse document's body_hits. Return Counter of body_hits' tokens"""
        body_hits_count_map = Counter({})
        if body_hits is not None:
            for body_hit in body_hits:
                body_hits_count_map[body_hit] = len(body_hits[body_hit])
        return body_hits_count_map
    
    
    def get_query_vector(self, q, query_weight_scheme=None):

        """ Handle the query vector. 
        1. get term freq 2. get doc freq 3. normalization
        Refer to above SMART notificaton and figure
        
        Compute the raw term (and/or sublinearly scaled) frequencies
        Additionally weight each of the terms using the idf value of the term in the query 
        (we use the PA1 corpus to determine how many documents contain the query terms 
        which is calculated above and stored in self.idf).
        
        Note that no normalization is needed for query length 
        because any query length normalization applies to all docs and so is not relevant to ranking.
        
        Args:
            q (Query): Query("some query")
            
        Returns:
            query_vec (dict):  the query vector
        """  
       
        if query_weight_scheme is None:
            query_weight_scheme = self.query_weight_scheme #modified
            
        query_vec = {}
        ### Begin your code
        query_vec = dict(list(map(lambda x : (x,self.idf.get_idf(x)),set(q.query_words)))) # idf
        ### End your code
        return query_vec
    
    def get_doc_vector(self, q, d, doc_weight_scheme=None):
        
        """get term freqs for documents
        You will need to 
        1. Initialize tfs for tf types (as in self.TFTYPES)
        2. Initialize tfs for query_words
        3. Tokenize url, title, and headers, anchors, body_hits if exits
        4. (we've already provided parse functions above)
        5. Loop through query terms increasing relevant tfs
        
        Args:
        q (Query) : Query("some query")
        d (Document) : Query("some query")["an url"]
        
        Returns:
        doc_vec (dict) :A dictionary of doc term frequency:
                    tf type -> query_word -> score
                    For example: the output of document d
                    Should be look like "{'url': {'stanford': 1, 'aoerc': 0, 'pool': 0, 'hours': 0},
                                     'title': {'stanford': 1, 'aoerc': 0, 'pool': 0, 'hours': 0},...""
        """
        if doc_weight_scheme is None:
            doc_weight_scheme = self.doc_weight_scheme #modified
            
        doc_vec = {} 
        
        qwords = set(q.query_words)
        ### Begin your code
        for parse_type in self.TFTYPES:
            parse_ans = self.parse(parse_type,d)
            if parse_ans is None:
                continue
            doc_vec[parse_type] = dict(list(map( lambda x : (x,parse_ans.get(x,0)),set(qwords))))
        ### End your code
        
        # Normalization
        if doc_weight_scheme['norm']:
            norm_func = doc_weight_scheme["norm"]
            doc_vec = norm_func(q, d, doc_vec)
        return doc_vec
        
        
    def normalize_doc_vec(self, q, d, doc_vec):
        """ Normalize the doc vector
        Task 1 and 2 will use different normlization. You can also try other different normalization methods.
        Args: 
            doc_vec (dict) : the doc vector
            q (Query) : the query
            d (Document) : the document
        """
        raise NotImplementedError
        
    # For the learning-to-rank ipython notebook, you may choose to define additional function(s)
    # below for various possible kinds of normalization. 
    # You will not need to fill this section out for the "ranking" notebook. 

    ### Begin your code

    ### End your code 
    
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
        raise NotImplementedError