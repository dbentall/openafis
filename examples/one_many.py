import math
from pathlib import Path
from pprint import pprint

from openafis.openafis import PyTemplateISO19794_2_2005, PyMatchSimilarity


def main(query_path, enroll_dir):
    # Set matcher parameters:
    param = {
        "max_local_dist": 12, # default: 12
        "max_global_dist": 12, # default: 12
        "min_minutiae": 4, # default: 4
        "max_rotations": 3, # default: 3
        "max_angle_diff": math.pi / 6, # default: math.pi / 6
        "max_direction_diff": math.pi / 4, # default: math.pi / 4
    }

    similarity = PyMatchSimilarity(**param)

    results = []
    # for query_path in query_dir.iterdir():
    query_id = query_path.name.split("_")[0]
    t1 = PyTemplateISO19794_2_2005.from_file(str(query_path))
    similarities = []
    for enrol_path in enroll_dir.glob("*.iso"):
        enrol_id = enrol_path.name
        t2 = PyTemplateISO19794_2_2005.from_file(str(enrol_path))
        similarities.append((enrol_id, similarity.compute(t1, t2)))
    # Keep top 5 similarities
    results.append(
        (query_id, sorted(similarities, key=lambda x: x[1], reverse=True)[:5])
    )

    pprint(results)


if __name__ == "__main__":
    import sys

    main(Path(sys.argv[1]), Path(sys.argv[2]))
