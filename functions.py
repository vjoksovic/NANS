import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper
from sklearn.linear_model import LinearRegression    


matplotlib.rcParams['figure.figsize'] = (8, 4)
sb.set(font_scale=1.)


def remove_outliers(data, threshold):
    z_scores = np.abs((data - data.mean()) / data.std())
    rows_to_remove = z_scores.apply(lambda x: any(x > threshold), axis=1)
    cleaned_data = data[~rows_to_remove]
    return cleaned_data

def calculate_residuals(model, features, labels):
    y_pred = model.predict(features)
    df_results = pd.DataFrame({'Actual': labels, 'Predicted': y_pred})
    df_results['Residuals'] = abs(df_results['Actual']) - abs(df_results['Predicted'])
    return df_results


def linear_assumption(model: LinearRegression| RegressionResultsWrapper, features: np.ndarray|pd.DataFrame, labels: pd.Series, p_value_thresh=0.05, plot=True):
    df_results = calculate_residuals(model, features, labels)
    y_pred = df_results['Predicted']

    if plot:
        plt.figure(figsize=(6,6))
        plt.scatter(labels, y_pred, alpha=.5)
        line_coords = np.linspace(np.concatenate([labels, y_pred]).min(), np.concatenate([labels, y_pred]).max())
        plt.plot(line_coords, line_coords, color='darkorange', linestyle='--')
        plt.title('Linear assumption')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.show()

    if type(model) == RegressionResultsWrapper:
        p_value = model.f_pvalue
        is_linearity_found = True if p_value < p_value_thresh else False
        return is_linearity_found, p_value
    else:
        pass


def independence_of_errors_assumption(model, features, labels, plot=True):
    df_results = calculate_residuals(model, features, labels)

    if plot:
        sb.scatterplot(x='Predicted', y='Residuals', data=df_results)
        plt.axhline(y=0, color='darkorange', linestyle='--')
        plt.show()

    from statsmodels.stats.stattools import durbin_watson
    dw_value = durbin_watson(df_results['Residuals'])

    autocorrelation = None
    if dw_value < 1.5: autocorrelation = 'positive'
    elif dw_value > 2: autocorrelation = 'negative'
    else: autocorrelation = None
    return autocorrelation, dw_value

def normality_of_errors_assumption(model, features, label, p_value_thresh=0.05, plot=True):
    df_results = calculate_residuals(model, features, label)
    
    if plot:
        plt.title('Distribution of residuals')
        sb.histplot(df_results['Residuals'], kde=True, kde_kws={'cut':3})
        plt.show()

    from statsmodels.stats.diagnostic import normal_ad
    p_value = normal_ad(df_results['Residuals'])[1]
    dist_type = 'normal' if p_value >= p_value_thresh else 'non-normal'
    return dist_type, p_value



def equal_variance_assumption(model, features, labels, p_value_thresh=0.05, plot=True):
    df_results = calculate_residuals(model, features, labels)

    if plot:
        sb.scatterplot(x='Predicted', y='Residuals', data=df_results)
        plt.axhline(y=0, color='darkorange', linestyle='--')
        plt.show()

    if type(model) == LinearRegression:
        features = sm.add_constant(features)
    p_value =  sm.stats.het_goldfeldquandt(df_results['Residuals'], features)[1]
    dist_type = 'equal' if p_value >= p_value_thresh else 'non-equal'
    return dist_type, p_value


def perfect_collinearity_assumption(features: pd.DataFrame, plot=True):
    correlation_matrix = features.corr() # racunamo matricu korelacije

    if plot:
        sb.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.1)
        plt.title('Matrica korelacije')
        plt.show()
    
    np.fill_diagonal(correlation_matrix.values, np.nan)
    pos_perfect_collinearity = (correlation_matrix > 0.999).any().any()
    neg_perfect_collinearity = (correlation_matrix < -0.999).any().any()
    has_perfect_collinearity = pos_perfect_collinearity or neg_perfect_collinearity
    return has_perfect_collinearity


def are_assumptions_satisfied(model, features, labels, p_value_thresh=0.05):
    x_with_const = sm.add_constant(features)
    is_linearity_found, p_value = linear_assumption(model, x_with_const, labels, p_value_thresh, plot=False)
    autocorrelation, dw_value = independence_of_errors_assumption(model, x_with_const, labels, plot=False)
    n_dist_type, p_value = normality_of_errors_assumption(model, x_with_const, labels, p_value_thresh, plot=False)
    e_dist_type, p_value = equal_variance_assumption(model, x_with_const, labels, p_value_thresh, plot=False)
    has_perfect_collinearity = perfect_collinearity_assumption(features, plot=False)

    if is_linearity_found and autocorrelation is None and n_dist_type == 'normal' and e_dist_type == 'equal' and not has_perfect_collinearity:
        return True
    else:
        return False



def get_fitted_model(features, labels):
    x_with_const = sm.add_constant(features, has_constant='add')
    model = sm.OLS(labels, x_with_const).fit()
    return model


def get_rmse(model, features, labels):
    y_pred = model.predict(sm.add_constant(features, has_constant='add'))
    rmse = np.sqrt(np.mean(((labels - y_pred) ** 2)))
    return rmse

def get_rmse_rf(model, features, labels):
    y_pred = model.predict(features)
    rmse = np.sqrt(np.mean(((labels - y_pred) ** 2)))
    return rmse

def get_rsquared_adj(model, features, labels):
    num_attributes = features.shape[1]
    y_pred = model.predict(sm.add_constant(features, has_constant='add'))

    from sklearn.metrics import r2_score
    r_squared = r2_score(labels, y_pred)
    
    n = len(y_pred)
    p = num_attributes
    adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
    return adjusted_r_squared

def get_rsquared_adj_rf(model, features, labels):
    y_pred = model.predict(features)

    from sklearn.metrics import r2_score
    r_squared = r2_score(labels, y_pred)
    
    n = len(y_pred)
    p = features.shape[1]
    adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
    return adjusted_r_squared


def get_pred_interval(model, features: int | float | np.ndarray | pd.Series | pd.DataFrame, p_value_trash=0.05):
    if type(features) == int or type(features) == float:
        pred_intervals = model.get_prediction(sm.add_constant([features, 0])).summary_frame(alpha=p_value_trash)
        low = pred_intervals['obs_ci_lower'].values[0]
        high = pred_intervals['obs_ci_upper'].values[0]
        return low, high
    
    if type(features) == list or type(features) == np.ndarray:
        const = np.array([1])
        datapoint = np.concatenate([features, const])
        pred_intervals = model.get_prediction(datapoint).summary_frame(alpha=p_value_trash)
        low = pred_intervals['obs_ci_lower'].values[0]
        high = pred_intervals['obs_ci_upper'].values[0]
        return low, high

    else:
        pred_intervals = model.get_prediction(sm.add_constant(features)).summary_frame(alpha=p_value_trash)
        low = pred_intervals['obs_ci_lower'].values
        high = pred_intervals['obs_ci_upper'].values
        return low, high
    
    
def calculate_residuals_rf(model, features, labels):
    y_pred = model.predict(features)
    df_results = pd.DataFrame({'Actual': labels, 'Predicted': y_pred})
    df_results['Residuals'] = df_results['Actual'] - df_results['Predicted']
    return df_results



    


