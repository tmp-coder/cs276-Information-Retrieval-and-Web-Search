
class GBDTLearner:
    
    def __init__(self):
        self.params = {
            "booster":"gbtree",
            "objective":"rank:pairwise",
            "eval_metric":"ndcg",
            "eta":0.01,
            "max_depth":10,
            "gamma":0.01
            "subsample":1,
        }
        self.model = None

    def train_model (self, dtrain, evallist):
    
        '''
        - Specifies parameters for XGBoost training
        - Trains model

        Args:
                dtrain (type DMatrix): DMatrix is a internal data structure that used by XGBoost 
                which is optimized for both memory efficiency and training speed.
                
                evallist (array of tuples): The datasets on which the algorithm reports performance as training takes place
                

        Returns: none
        '''
        num_rounds = 100 #Experiment with different values of this parameter
        
        ### Begin your code
        self.model = xgb.train(self.params,dtrain=dtrain,evals=evallist,early_stopping_rounds=num_rounds,num_boost_round=num_rounds)
        ### End your code
    
    def predict_model (self, dtest):
    
        '''
        - Output predicted scores based on the trained model.

        Args:
                dtest (type DMatrix): DMatrix that contains the dev/test signal data

        Returns:
                y_pred (numpy array of dimension (N,)): Predicted relevance scores for each query, document pair
                based on the trained  model.
        '''
        ### Begin your code
        return self.model.predict(dtest,self.model.best_ntree_limit)
        ### End your code

