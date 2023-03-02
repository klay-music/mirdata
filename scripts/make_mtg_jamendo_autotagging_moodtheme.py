import argparse
import csv
import glob
import hashlib
import json
import os
from mirdata.validate import md5


def make_mtg_jamendo_autotagging_index(data_path):
    label_type_list = ["genre", "instrument", "top50tags", "moodtheme"]

    for label_type in label_type_list:
        mtg_jamendo_autotagging_INDEX_PATH = '../mirdata/datasets/indexes/mtg_jamendo_autotagging_' + label_type + '_index_1.0.json'
        
        mtg_jamendo_autotagging_index = {
            'version': '1.0',
            'tracks': {}
        }
        meta_path = os.path.join(data_path, "data", "autotagging_" + label_type + ".tsv")

        with open(meta_path, "r") as fhandle:
            d = list(csv.DictReader(fhandle, delimiter="\t", fieldnames=["TRACK_ID", "ARTIST_ID", "ALBUM_ID", "PATH",
                                                                        "DURATION", "TAGS"]))
            meta = {m["TRACK_ID"]: m["PATH"] for m in d[1:]}

        for track_id, path in meta.items():
            audio_path = os.path.join(data_path, 'audios', path)
            mtg_jamendo_autotagging_index['tracks'][track_id] = {
                'audio': (audio_path.replace(data_path + '/', ''), md5(audio_path)),
            }
        with open(mtg_jamendo_autotagging_INDEX_PATH, 'w') as fhandle:
            json.dump(mtg_jamendo_autotagging_index, fhandle, indent=2)


def main(args):
    make_mtg_jamendo_autotagging_index(args.mtg_jamendo_autotagging_data_path)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Make mtg_jamendo_autotagging index file.')
    PARSER.add_argument('mtg_jamendo_autotagging_data_path', type=str, help='Path to mtg_jamendo_autotagging data folder.')
    main(PARSER.parse_args())
