
def get_features (signal_file, idf):
    '''
    Create a feature vector from the signal file and from the idf_dict. 

    Args:
        signal_file: filepath to signal file
        idf: object of class Idf (with idf built)

    Returns:
        feature_vec (numpy array of dimension (N, 5)): N is the number of (query, document)
        pairs in the relevance file.
    '''

    # Experiment with different values of weighting below. Note that this uses dddqqq notation.
    # Make sure to set weighting to the best value prior to submitting your code.
    # You should be able to support lnn.ltc weighting, along with any other weighting that you experiment with


    WEIGHTING = 'lnnltc' 

    assert len(WEIGHTING) == 6, "Invalid weighting scheme."        

    feature_vec = []

    ### Begin your code
    query_dict = load_train_data(signal_file)
    scorer =AScorer(idf)
    
    types = ["url","title","body_hits","header","anchor"]
    for q,docs in query_dict.items():
        qc = Counter(q.query_words)
        qv = np.array(list(map(lambda x : (1 +np.log10(qc[x])) * idf.get_idf(x),qc.keys())))
        qv = qv / np.linalg.norm(qv)
        for doc in docs.values():
            dv = scorer.get_doc_vector(q,doc)
            
            dv_func = lambda filed : np.array(list(map(lambda x : dv[filed][x],qc.keys())))
            
            feature_vec.append([(sum(qv * dv_func(field)) if (field in dv) else 0) for field in types ])
    
    feature_vec = np.array(feature_vec)
    ### End your code
    assert feature_vec.shape[1] == 5,"feature_vec.shape = (N,5)"
    print("in get_feature : feature_vec.shape",feature_vec.shape)
    return feature_vec


def get_relevance (relevance_file):
    '''
    Extract relevance scores from the relevance file. This should be a simple wrapper (<10 lines) over
    the get_rel_scores() function in the NDCG class.

    Args:
        relevance_file: filepath to relevance file

    Returns:
        relevance_vec (numpy array of dimension (N,)): N is the number of (query, document)
        pairs in the relevance file.   
        ndcg_obj: NDCG object which contains relevance scores
    '''  


    relevance_vec = []
    ndcg_obj = NDCG()

    ### Begin your code
    ndcg_obj.get_rel_scores(relevance_file)
    for q,urls in ndcg_obj.rel_scores.items():
        relevance_vec.extend(list(urls.values()))
    relevance_vec = np.array(relevance_vec)
    ### End your code

    return relevance_vec, ndcg_obj



    
   
    