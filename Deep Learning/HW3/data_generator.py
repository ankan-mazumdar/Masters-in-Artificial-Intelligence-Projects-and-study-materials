import numpy as np
n_context = 32
n_features = 3
n_samples = 100
np.random.seed(42)
def generate_single_data_point(n_context, n_features):
    base_flip_prob=0.2
    X = np.random.randn(n_context, n_features-1)
    X /= np.linalg.norm(X, axis=1, keepdims=True) # Normalize to lie on unit circle

    last_point = X[-1]
    distances = np.linalg.norm(X - last_point, axis=1) # Distances to the last point

    sorted_indices = np.argsort(-distances) # Sort X by distance from furthest to closest
    X_sorted = X[sorted_indices]

    y_output = 2.0*(np.random.randn()>0)-1 # Generate a label

    # Compute label flip probabilities
    dot_products = np.dot(X_sorted, last_point)
    label_flip_prob = ((base_flip_prob-(1/2))/2) * dot_products + ((base_flip_prob+(1/2))/2)

    random_values = np.random.rand(n_context)
    flip_labels = random_values <= label_flip_prob
    y = np.where(flip_labels, -y_output, y_output)
    X_output = np.hstack([X_sorted,y.reshape((-1,1))])
    return X_output, y_output

X_list = []
y_list = []
for _ in range(n_samples):
    Xi, yi = generate_single_data_point(n_context,n_features)
    X_list.append(Xi)
    y_list.append(yi)
X = np.stack(X_list,axis=0)
y = np.array(y_list)

X_flattened = X.reshape(n_samples*n_context,n_features)

np.savetxt("X.csv", X_flattened, delimiter=",", fmt="%f")

np.savetxt("y.csv", y, delimiter=",", fmt="%f")
