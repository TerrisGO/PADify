from __future__ import division

import sys
from statistics import mean

from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

from tools.classifier.evaluate_hter import evaluate_with_values

# from classifier.evaluate_hter import evaluate_predictions, evaluate_with_values

sys.path.append('/Users/rodrigobresan/Documents/dev/github/anti_spoofing/spoopy')

import os

from pandas import *

# from tools.file_utils import file_helper

ARTIFACT_CLEAN_RESULTS_NAME = "results_prediction_names_clean_all.txt"
ARTIFACT_DIRT_RESULTS_NAME = "results_prediction_names_dirt_all.txt"

ARTIFACT_CLEAN_RESULTS_NAME_INCEPTION = "results_prediction_names_clean_mean_inception.txt"
ARTIFACT_DIRT_RESULTS_NAME_INCEPTION = "results_prediction_names_dirt_mean_inception.txt"

TESTING_ALL_FRAMES = True


def generate_results(base_path, output_path, is_inception, perform_clean=False):
    try:
        if is_inception:
            names, y_pred_proba, y_pred, y_test = load_file_info_inception(base_path)
        else:
            names, y_pred_proba, y_pred, y_test = load_file_info_target(base_path)

        dict_results = extract_results(names, y_pred_proba, y_pred, y_test)

        if perform_clean:
            file_name = generate_predictions_names_cleaned(output_path, dict_results, is_inception)
        else:
            file_name = generate_predictions_names_dirt(output_path, dict_results, is_inception)
    except Exception as e:
        print(e)

    return file_name, dict_results


def get_metrics(count_fake, count_real, fa, fr):
    bpcer = fr / count_real
    apcer = fa / count_fake
    hter = (apcer + bpcer) / 2

    if hter == 0:
        print('woah')
    return hter, apcer, bpcer


def generate_predictions_names_cleaned(output_path, dict_results, is_inception):
    if is_inception:
        file_name = os.path.join(output_path, ARTIFACT_CLEAN_RESULTS_NAME_INCEPTION)
    else:
        file_name = os.path.join(output_path, ARTIFACT_CLEAN_RESULTS_NAME)

    file = open(file_name, "w")
    empty_probas = 0

    print('total results: ', len(dict_results))
    for result in dict_results:
        try:
            y_pred = dict_results[result][2]

            if TESTING_ALL_FRAMES:
                for result_proba in dict_results[result][0]:
                    line = result + "," + str(result_proba)
                    file.write(str(line) + "\n")
            else:
                right_pred = 0
                right_probas = []
                for i, pred in enumerate(y_pred):
                    ground_truth = dict_results[result][1][i]
                    if ground_truth == pred:
                        proba = dict_results[result][0][i]
                        right_probas.append(proba)

                if len(right_probas) == 0:
                    empty_probas = empty_probas + 1
                    mean_right_probas = 0
                else:
                    mean_right_probas = mean(right_probas)

                line = result + "," + str(mean_right_probas)
                file.write(str(line) + "\n")


        except Exception as e:
            print(e)

    print('empty: ', empty_probas)

    file.close()
    return file_name


def generate_predictions_names_dirt(path, dict_results, is_inception):
    if is_inception:
        file_name = os.path.join(path, ARTIFACT_DIRT_RESULTS_NAME_INCEPTION)
    else:
        file_name = os.path.join(path, ARTIFACT_DIRT_RESULTS_NAME)

    file = open(file_name, "w")
    print(file_name)

    print('total results: ', len(dict_results))
    for result in dict_results:
        try:

            if TESTING_ALL_FRAMES:
                for result_proba in dict_results[result][0]:
                    line = result + "," + str(result_proba)
                    file.write(str(line) + "\n")
            else:
                mean_right_probas = mean(dict_results[result][0])

                line = result + "," + str(mean_right_probas)
                file.write(str(line) + "\n")

        except Exception as e:
            print(e)

    file.close()
    return file_name


def extract_results(names, y_pred_proba, y_pred, y_test):
    dict_results = {}
    for i, prediction_proba in enumerate(y_pred_proba[:, 1]):
        current_id = names[i]

        if current_id not in dict_results:  # condition for initializing
            dict_results[current_id] = []
            dict_results[current_id].append([])  # prediction proba
            dict_results[current_id].append([])  # real
            dict_results[current_id].append([])  # prediction

        dict_results[current_id][0].append(prediction_proba)
        dict_results[current_id][1].append(y_test[i])
        dict_results[current_id][2].append(y_pred[i])

    return dict_results


def load_file_info_target(path):
    file = open(os.path.join(path, "names_test.txt"), "r")
    lines = file.readlines()
    names = pandas.io.json.loads(lines[0])
    y_test = np.load(os.path.join(path, 'y_test.npy'))
    y_pred_proba = np.load(os.path.join(path, 'y_pred_proba.npy'))
    y_pred = np.load(os.path.join(path, 'y_pred.npy'))
    return names, y_pred_proba, y_pred, y_test


def load_file_info_inception(path):
    file = open(os.path.join(path, "names_test_inception.txt"), "r")
    lines = file.readlines()
    names = pandas.io.json.loads(lines[0])
    y_test = np.load(os.path.join(path, 'y_test_inception.npy'))
    y_pred_proba = np.load(os.path.join(path, 'y_pred_proba_inception.npy'))
    y_pred = np.load(os.path.join(path, 'y_pred_inception.npy'))
    return names, y_pred_proba, y_pred, y_test


def list_files(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]


def generate_results_intra(features_path, base_output_path):
    datasets_origin = list_files(features_path)

    for dataset_origin in datasets_origin:
        path_origin = os.path.join(features_path, dataset_origin)
        attack_types = list_files(path_origin)
        for attack_type in attack_types:
            path_target = os.path.join(features_path, dataset_origin, attack_type)
            properties = list_files(path_target)

            for property in properties:
                target = os.path.join(features_path, dataset_origin, attack_type, property, "features", "resnet")
                try:

                    output_path = os.path.join(base_output_path, dataset_origin, attack_type, property)
                    os.makedirs(output_path, exist_ok=True)

                    generate_results(target, output_path, True, perform_clean=False)
                    generate_results(target, output_path, True, perform_clean=True)


                    generate_results(target, output_path, False, perform_clean=False)
                    generate_results(target, output_path, False, perform_clean=True)
                except Exception as e:
                    print(e)


# result_prediction_names.txt
# nome_video, 0.1

# result_prediction_names.txt
# nome_video_frame_1, 0.1

def evaluate_combinated_all(base_probas):
    results = [
        ['Origin', 'Attack', 'HTER', 'APCER', 'BPCER']
    ]

    datasets = list_files(base_probas)
    print('datasets: ', datasets)
    # evaluate_results('ra', 'cbsr')

    for dataset_origin in datasets:
        dataset_path = os.path.join(base_probas, dataset_origin)
        attack_types = os.listdir(dataset_path)
        for attack in attack_types:
            print('===============Train: %s Attack: %s=============' % (dataset_origin, attack))
            try:

                hter, apcer, bpcer = evaluate_results(base_probas, dataset_origin, attack)

                row = [dataset_origin, attack, hter, apcer, bpcer]
                results.append(row)
            except Exception as e:
                print(e)

    df = DataFrame(results)
    print(df)
    df.to_csv('results_hter_combinations_intra.csv', sep=' ')


def evaluate_results(path_probas, origin, attack):
    train_depth = path_probas + origin + '/' + attack + '/depth/' + ARTIFACT_DIRT_RESULTS_NAME_INCEPTION
    train_illumination = path_probas + origin + '/' + attack + '/illumination/' + ARTIFACT_DIRT_RESULTS_NAME_INCEPTION
    train_saliency = path_probas + origin + '/' + attack + '/saliency/' + ARTIFACT_DIRT_RESULTS_NAME_INCEPTION

    test_depth = path_probas + origin + '/' + attack + '/depth/' + ARTIFACT_DIRT_RESULTS_NAME
    test_illumination = path_probas + origin + '/' + attack + '/illumination/' + ARTIFACT_DIRT_RESULTS_NAME
    test_saliency = path_probas + origin + '/' + attack + '/saliency/' + ARTIFACT_DIRT_RESULTS_NAME

    X_train, y_train, names_train = get_item_data(train_depth, train_illumination, train_saliency)
    X_test, y_test, names_test = get_item_data(test_depth, test_illumination, test_saliency)
    #
    # from matplotlib import pyplot
    #
    # pyplot.plot(X_train, y_train)
    # pyplot.plot(X_test, y_test)
    # pyplot.show()

    # print('Running with SVC')
    top_model = OneVsRestClassifier(BaggingClassifier(SVC(verbose=False), n_jobs=-1))
    top_model.fit(X_train, y_train)

    y_pred = top_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print('acc: ', acc)

    # print('Running with RBF kernel')
    param_grid = [{'kernel': ['rbf'], 'gamma': [1e-4, 1e-3], 'C': [1, 10, 100, 1000, 10000]}]
    grid_model = GridSearchCV(SVC(), param_grid, verbose=False, n_jobs=3)
    grid_model.fit(X_train, y_train)
    y_pred = grid_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print('acc grid search: ', acc)

    hter, apcer, bpcer = evaluate_with_values(y_pred, y_test, names_test)
    print('%.4f %.4f %.4f' % (hter, apcer, bpcer))

    return hter, apcer, bpcer
    #
    # model = XGBClassifier()
    # model.fit(X_train, y_train)
    # # make predictions for test data
    # y_pred = model.predict(X_test)
    # predictions = [round(value) for value in y_pred]
    # # evaluate predictions
    # accuracy = accuracy_score(y_test, predictions)
    # print("Accuracy XGBoost: %.2f%%" % (accuracy * 100.0))
    # output_path = '/Users/rodrigobresan/Documents/dev/github/anti_spoofing/spoopy/spoopy/tools/classifier_probas'
    #
    # y_test_path = os.path.join(output_path, 'y_test.npy')
    # y_pred_path = os.path.join(output_path, 'y_pred.npy')
    # names_path = os.path.join(output_path, 'names_test.txt')
    #
    # np.save(y_test_path, y_test)
    # np.save(y_pred_path, y_pred)
    # file = open(names_path, "w")
    # file.write(str(json.dumps(test_names)) + "\n")
    # file.close()


def dict_to_nparray(dict):
    for i, result in enumerate(dict):
        print(result)


def get_item_data(path_dept, path_illumination, path_saliency):
    with open(path_dept) as f:
        depth_results = f.readlines()
    with open(path_illumination) as f:
        illumination_results = f.readlines()
    with open(path_saliency) as f:
        saliency_results = f.readlines()

    dict_results = {}
    item_names = []

    list_sizes = [len(depth_results), len(illumination_results), len(saliency_results)]
    min_size = min(list_sizes)

    middle = min_size // 2
    margin = 200
    step = 10

    print()

    for i, result in enumerate(depth_results[0:min_size]):
        current_item = depth_results[i].split(',')[0]
        item_names.append(current_item)

        if current_item not in dict_results:
            dict_results[current_item] = []
            dict_results[current_item].append([])  # depth
            dict_results[current_item].append([])  # illumination
            dict_results[current_item].append([])  # saliency
            dict_results[current_item].append([])  # ground truth

        try:
            dict_results[current_item][0].append(clean(depth_results[i]))
            dict_results[current_item][1].append(clean(illumination_results[i]))
            dict_results[current_item][2].append(clean(saliency_results[i]))
            dict_results[current_item][3].append(name_to_int(current_item))
        except Exception as e:
            print(e)
    np_results = None

    for key, value in dict_results.items():
        if np_results is None:
            np_results = np.array(value)
        else:
            np_single = np.array(value)
            np_results = np.hstack([np_results, np_single])

    np_results = np.transpose(np_results)
    x = np_results[:, :3]
    y = np_results[:, -1]

    return x, y, item_names


def name_to_int(item_name):
    item = item_name.split('/')[0]

    if item == 'fake':
        return 0
    else:
        return 1


def clean(content):
    return float(content.split(',')[1].replace('\n', ''))


if __name__ == '__main__':
    features_path = '/codes/bresan/remote/spoopy/spoopy/data/6_features'
    output_path = '/codes/bresan/remote/spoopy/spoopy/data/7_probas'
    generate_results_intra(features_path, output_path)
    # evaluate_combinated_all(output_path)
