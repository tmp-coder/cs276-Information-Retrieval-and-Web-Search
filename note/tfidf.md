# tfidf

$tf_{t,d}$: term frequency, # term $t$ in doc $d$

**intuition** rare terms are more informative(e.g stop words, the,a, an, useless)

$df_{t}$: document frequency, # doc contained term $t$

$idf_{t}$: inverse document frequency, # docs / $df_t$

## effect of idf ranking

no effect on ranking one term query(becouse , $idf_t$ is a function of term t, only dependent on term,given a fixed term t idf always same)


## scoring

$w_{t,d} = log(1+tf_{t,d})*log_{10}(N/(df_{t}+1))$

score(Q,d) = $\sum_{t \in Q \bigcap d } w_{t,d}$

# vector sapace model

将每个文档中的查询term表示成一个vector ，在 vector space $R^|term|$
同时将query也表示成一个vecotr
计算文档 vector，与query vector的consine similarity,rank

## storage trick

这样做需要对之前的inverted index 的posting list做一些存储上的修改，不然每次查询都要计算这些特征会非常麻烦。

1. 对posting list中的每个post 存储 tf，
2. 在posting list head上存储frq(方便计算df)

# ref

1. [stanford PPT](https://web.stanford.edu/class/cs276/19handouts/lecture6-tfidf.ppt)