import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics

# Provided data
actual = [2, 4, 3, 1, 1, 2, 3, 3, 3, 1, 2, 4, 2, 4, 2, 4, 3, 2, 2, 2, 2, 1, 3, 2, 2, 2, 4, 1, 3, 3, 6, 4, 2, 4, 2, 4, 3, 4, 2, 2, 4, 3, 1, 2, 2, 4, 2, 2, 2, 3, 4, 3, 3, 6, 4, 2, 2, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2, 4, 4, 4, 2, 2, 2, 2, 2, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 3, 3, 3, 2, 3, 2, 2, 2, 4, 4, 1, 4, 2, 2, 3, 3, 3, 2, 2, 2, 2, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 1, 3, 2, 4, 2, 3, 1, 5, 5, 5, 5, 4, 6, 7, 6, 6, 6, 7, 7, 6, 6, 7, 5, 6, 7, 5, 6, 4, 2, 2, 2, 2, 2, 2, 2, 1, 3, 2, 2, 2, 2]
predicted = [2, 2, 3, 3, 1, 2, 4, 1, 3, 1, 2, 1, 2, 4, 2, 4, 3, 2, 2, 2, 4, 1, 1, 2, 2, 4, 4, 3, 1, 3, 3, 4, 2, 2, 2, 4, 3, 2, 2, 2, 4, 1, 1, 2, 2, 2, 2, 2, 2, 3, 2, 3, 3, 1, 4, 2, 2, 3, 3, 1, 4, 2, 2, 2, 1, 2, 2, 4, 4, 4, 2, 2, 2, 2, 2, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 3, 3, 3, 3, 2, 2, 2, 4, 4, 1, 4, 2, 2, 1, 3, 1, 2, 2, 2, 4, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 1, 1, 3, 2, 4, 2, 3, 1, 1, 5, 5, 5, 5, 4, 6, 7, 6, 6, 6, 7, 7, 6, 6, 7, 5, 6, 7, 5, 6, 4, 2, 2, 2, 2, 2, 2, 2, 1, 3, 2, 2, 2, 2]

# Convert lists to numpy arrays
actual = np.array(actual)
predicted = np.array(predicted)

# Create confusion matrix
confusion_matrix = metrics.confusion_matrix(actual, predicted)

# Display confusion matrix
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[1, 2, 3, 4, 5, 6, 7])
cm_display.plot()

# Add labels and title
plt.xlabel('Predicted (LULC)')
plt.ylabel('Actual (Ground Truth)')
plt.title('Confusion Matrix')

# Save the plot to buffer
plt.savefig(sys.stdout.buffer)
sys.stdout.flush()
