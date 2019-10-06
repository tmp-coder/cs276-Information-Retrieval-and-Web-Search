
class PointwiseLearner:
    
    def __init__(self):
        self.model = LinearRegression()

    def train_model (self, x, y):
    
        '''
        - Train your linear regression model using the LinearRegression class 

        Args:
                x (numpy array of dimension (N, 5)): Feature vector for each query, document pair. 
                Dimension is N x 5, where N is the number of query, document pairs. 
                Is the independent variable for linear regression. 

                y (numpy array of dimension (N,)): Relevance score for each query, document pair. 
                Is the dependent variable for linear regresion.

        Returns: none
        '''
        ### Begin your code
        self.model.fit(x,y)
        ### End your code
    
    def predict_model (self, x):
    
        '''
        - Output predicted scores based on the trained model.

        Args:
                x (numpy array of dimension (N, 5)): Feature vector for each query, document pair. 
                Dimension is N x 5, where N is the number of (query, document) pairs. 
                Predictions are made on this input feature array.

        Returns:
                y_pred (numpy array of dimension (N,)): Predicted relevance scores for each query, document pair
                based on the trained linear regression model.
        '''
        ### Begin your code
        return self.model.predict(x)
        ### End your code
    