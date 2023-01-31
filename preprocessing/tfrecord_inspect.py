#!/usr/bin/env python3

import argparse

import numpy as np
import tensorflow as tf
import os.path as path

parser = argparse.ArgumentParser(
    description="Inspect TFRecord file")
parser.add_argument("-i",
                    "--input_file",
                    help="TFRecord (.record) file to inspect.",
                    type=str,
                    required=True)
parser.add_argument("-n",
                    "--num_examples",
                    help="Number of examples to print.",
                    type=int,
                    default=5)


def main():
    args = parser.parse_args()

    examples = tf.data.TFRecordDataset(path.normpath(args.input_file))
    all_classes = np.array([])
    for i, x in enumerate(examples):
        if i >= args.num_examples:
            break

        record = tf.io.parse_single_example(x, {
            'image/object/class/label': tf.io.VarLenFeature(dtype=tf.int64),
            'image/encoded': tf.io.VarLenFeature(dtype=tf.string)
        })

        classes = record['image/object/class/label']
        np_arr = classes.values.numpy()
        all_classes = np.append(all_classes, np_arr)
        print(f'Sample {i+1}: ', end='')
        for c in np_arr:
            print(c, end=', ')

        print()

    all_classes = np.unique(all_classes)
    print(f'Classes ({len(all_classes)}): {all_classes}')


if __name__ == '__main__':
    main()
