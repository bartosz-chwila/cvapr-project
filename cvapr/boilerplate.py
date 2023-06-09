import argparse
import signal

import cv2 as cv
import numpy as np

true_positive = 0
true_negative = 0
false_positive = 0
false_negative = 0

def main():
    parser = argparse.ArgumentParser(
        description='This program shows how to use background subtraction methods provided by OpenCV. You can process both videos and images.')
    parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
    parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
    parser.add_argument('--gt', type=str, help='Ground truth for the substraction', required=True)
    args = parser.parse_args()

    if args.algo == 'MOG2':
        backSub = cv.createBackgroundSubtractorMOG2()
    elif args.algo == 'MOG':
        backSub = cv.bgsegm.createBackgroundSubtractorMOG()
    else:
        backSub = cv.createBackgroundSubtractorKNN()

    capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
    if not capture.isOpened():
        print('Unable to open: ' + args.input)
        exit(0)

    gt = cv.VideoCapture(args.gt)

    global true_positive
    global true_negative
    global false_positive
    global false_negative

    while True:
        ret, frame = capture.read()
        if frame is None:
            print("--------------------------------")
            print("Experiment finished")
            print("Algo:", args.algo)
            print("Input:", args.input)
            print_accuracy()
            break

        fgMask = backSub.apply(frame)

        ret2, ground_truth_rgb = gt.read()

        ground_truth = cv.cvtColor(ground_truth_rgb, cv.COLOR_BGR2GRAY)

        cv.imshow("Ground truth", ground_truth)

        true_positive += np.sum(np.logical_and(ground_truth == 255, fgMask == 255))
        true_negative += np.sum(np.logical_and(ground_truth == 0, fgMask == 0))
        false_positive += np.sum(np.logical_and(ground_truth == 0, fgMask == 255))
        false_negative += np.sum(np.logical_and(ground_truth == 255, fgMask == 0))

        cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
        cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', fgMask)

        _ = cv.waitKey(1)

def handler(signum, frame):
    print_accuracy()

    #exit(0)


def print_accuracy():
    print("--------------------------------")

    # Wyświetlenie wyników macierzy pomyłek
    print("True Positive:", true_positive)
    print("True Negative:", true_negative)
    print("False Positive:", false_positive)
    print("False Negative:", false_negative)

    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = 2 * (precision * recall) / (precision + recall)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1_score)

    print("--------------------------------")

signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    main()
