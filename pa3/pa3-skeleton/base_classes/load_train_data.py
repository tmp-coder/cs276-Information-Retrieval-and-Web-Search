from .query import Query
from .document import Document

def load_train_data(feature_file_name):
    """
    Args:
        feature_file_name (str): name/path of feature file

    Returns:
       query_dict. Mapping of Query-url-Document. For example
        {computer science master: {'http://cs.stanford.edu/people/eroberts/mscsed/Admissions-MSInCSEducation.html':
           title: ms in computer science education stanford computer science
           headers: ["master's degree in computer science education"]
           body_hits: {'computer': [15], 'science': [16]}
           body_length: 741
           anchors: {'computer science': 2},
          'http://scpd.stanford.edu/online-engineering-courses.jsp': title: online engineering courses stanford university
           headers: ['computer science and information technology']
           body_hits: {'science': [136], 'master': [188], 'computer': [223]}
           body_length: 687,
         ...,
         }
    """
    line = None
    url = None
    anchor_text = None
    query = None # Qurey
    query_dict = {} #feature dictionary: Query -> (url -> Document)

    # Tokenization
    # [TODO] consider whether provide it to sutdent
    try:
        with open(feature_file_name, 'r', encoding = 'utf8') as f:
            for line in f:
                token_index = line.index(":")
                key = line[:token_index].strip()
                value = line[token_index + 1:].strip()

                if key == "query":
                    query = Query(value)
                    query_dict[query] = {}
                elif key == "url":
                    url = value;
                    query_dict[query][url] = Document(url);
                elif key == "title":
                    query_dict[query][url].title = str(value);
                elif key == "header":
                    if query_dict[query][url].headers is None:
                        query_dict[query][url].headers = []
                    query_dict[query][url].headers.append(value)
                elif key == "body_hits":
                    if query_dict[query][url].body_hits is None:
                        query_dict[query][url].body_hits = {}
                    temp = value.split(" ",maxsplit=1);
                    term = temp[0].strip();
                    if term not in query_dict[query][url].body_hits:
                        positions_int = []
                        query_dict[query][url].body_hits[term] = positions_int
                    else:
                        positions_int = query_dict[query][url].body_hits[term]
                    positions = temp[1].strip().split(" ")
                    for position in positions:
                        positions_int.append(int(position))
                elif key == "body_length":
                    query_dict[query][url].body_length = int(value);
                elif key == "pagerank":
                    query_dict[query][url].pagerank = int(value);
                elif key == "anchor_text":
                    anchor_text = value
                    if query_dict[query][url].anchors is None:
                        query_dict[query][url].anchors = {}
                elif key == "stanford_anchor_count":
                    query_dict[query][url].anchors[anchor_text] = int(value)
    except FileNotFoundError:
        print("feature_file_name Not Found!")

    return query_dict
