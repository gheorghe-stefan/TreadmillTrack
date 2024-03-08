import gpxpy
import sys
from datetime import datetime, timedelta

def add_timestamps(gpx_file):
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)

    base_timestamp = datetime(2024, 2, 27, 7, 0, 1)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if not point.time:
                    point.time = base_timestamp
                base_timestamp += timedelta(seconds=1)

    return gpx

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python AddTimestampsGpx.py <gpx_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    modified_gpx = add_timestamps(input_file)

    output_file = "modified_" + input_file
    with open(output_file, 'w') as f:
        f.write(modified_gpx.to_xml())

    print(f"Modified GPX file with timestamps saved as {output_file}")
