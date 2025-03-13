import numpy as np

# variables_used = np.array([
#     [1, 1, 1, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0],
#     [0, 1, 1, 0, 0, 1],
#     [1, 0, 0, 0, 1, 1],
#     [0, 1, 0, 1, 0, 1],
#     [0, 1, 1, 1, 0, 0],
#     [1, 0, 0, 1, 1, 0]
# ])
# scores = [15, 19, 11, 15, 14, 15, 19]
variables_used = np.array([
  [1, 1, 0, 0, 1, 0],
  [0, 1, 1, 0, 0, 1],
  [1, 0, 1, 1, 0, 0],
  [0, 1, 0, 1, 1, 0],
  [1, 0, 0, 1, 0, 1],
  [0, 0, 1, 1, 1, 0],
  [1, 1, 1, 0, 0, 0],
  [0, 1, 0, 0, 1, 1],
  [1, 0, 0, 0, 1, 1],
  [0, 0, 1, 0, 1, 1]
])

scores = [47, 52, 51, 50, 48, 49, 56, 50, 51, 50]  

# expected values: [14.8, 14.1, 12.9, 12.2, 10.9, 10.2]  

# expected values: 
# a = 


# Compute the rank of the matrix
rank = np.linalg.matrix_rank(variables_used)
print(f"Rank of variables_used matrix: {rank}")

X = variables_used
y = np.array(scores)

# print(X.T)

print(X.T @ y)


# Compute the normal equation
XT_X = np.dot(X.T, X)
XT_y = np.dot(X.T, y)
theta = np.linalg.inv(XT_X).dot(XT_y)

# Extract the values of a, b, c, d, e, f
a, b, c, d, e, f = theta

# Print the results
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"d = {d}")
print(f"e = {e}")
print(f"f = {f}")