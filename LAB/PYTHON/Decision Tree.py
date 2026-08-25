from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report
from sklearn import tree
import matplotlib.pyplot as plt


def load_data():
    data = load_iris()
    X = data.data
    y = data.target
    feature_names = data.feature_names
    target_names = data.target_names
    return X, y, feature_names, target_names


def train_model(X_train, y_train):
    model = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test, target_names):
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, target_names=target_names)
    return accuracy, report


def show_tree_rules(model, feature_names):
    rules = export_text(model, feature_names=feature_names)
    print(rules)


def plot_tree(model, feature_names, target_names):
    plt.figure(figsize=(14, 8))
    tree.plot_tree(model, feature_names=feature_names, class_names=target_names, filled=True)
    plt.show()


def predict_sample(model, sample, target_names):
    prediction = model.predict([sample])
    return target_names[prediction[0]]


if __name__ == "__main__":
    X, y, feature_names, target_names = load_data()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = train_model(X_train, y_train)

    accuracy, report = evaluate_model(model, X_test, y_test, target_names)

    print(f"Model Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(report)

    print("Decision Tree Rules:")
    show_tree_rules(model, feature_names)

    sample = [5.1, 3.5, 1.4, 0.2]
    result = predict_sample(model, sample, target_names)
    print(f"Prediction for sample {sample}: {result}")

    plot_tree(model, feature_names, target_names)
