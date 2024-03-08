import math
from gpx import GPX, track, track_segment, waypoint
from datetime import datetime, timedelta

def calculate_new_position(latitudeDegrees, longitudeDegrees, distanceMeters):
  """
  Calculates a new latitude and longitude position by going north a given distance.

  Args:
      latitude: The current latitude in degrees.
      longitude: The current longitude in degrees.
      distance: The distance to travel north in meters.

  Returns:
      A tuple containing the new latitude and longitude (in degrees).
  """

  # Earth's mean radius in meters
  earth_radius = 6371000

  # Convert latitude and longitude to radians
  latitudeRadians = math.radians(latitudeDegrees)
  #longitudeRadians = math.radians(longitudeDegrees)

  # Calculate the change in latitude
  deltaLatitude = distanceMeters / earth_radius

  # Calculate the new latitude
  newLatitudeDegrees = math.degrees(latitudeRadians + deltaLatitude)

  # Keep the new latitude within the valid range (-90 to 90 degrees)
  newLatitudeDegrees = max(-90, min(90, newLatitudeDegrees))

  return newLatitudeDegrees, longitudeDegrees

def ConvertSlopePercentToRadians(slope_percent):
    return math.atan(slope_percent / 100)

def compute_vertical_climb(distance, slope_radians):
    return distance * math.sin(slope_radians)

# receive in each second the data on the treadmill screen: speed index, incline
# needs internal conversion of speed index -> m/s
# simulate a workout
# segments of number of seconds spent at what speed at what incline
# for each speed/incline change -> create new tuple
# assume speed is mph -> 1mph = 0.44704 m/s
# assume speed is kmh -> 1kmh = 0.27777 m/s
# inclination:
# 0 -> 4.5%
# 1..15 => 6.3 + (k - 1) * 0.3 %
# compute elevation based on angle in percents and distance
treadmillResume = [
    ( 60,  6,  0),      # 60 seconds at speed 6 (pace 10) on incline 0
    (300, 10,  1),      # 5 minutes at speed 10 (pace 6) on incline 1
    (600, 12, 15)       # 10 minutes at speed 12 (pace 5) on incline 15
]

factorKmhToMps = 0.277777
# TODO: starting point needs to be randomized, otherwise Strava says it's duplicate activity
startLat, startLon, startEle = 47.386263996538865, 9.518609977010899, 0
base_timestamp = datetime(2024, 2, 27, 7, 0, 1)
currentLat, currentLon, currentEle = startLat, startLon, startEle

gpx = GPX()
gpx.creator = "Best app ever with Barometer" # apparently Strava doesn't validate the point elevation if creator ends in `Barometer`
track = track.Track()
track.name = "Treadmill run"
track.type = "VirtualRun"
trackSegment = track_segment.TrackSegment()

for seconds, speedIndex, inclineIndex in treadmillResume:
    metersPerSecond = speedIndex * factorKmhToMps
    inclineDegrees = 4.5 if (inclineIndex == 0) else 6.3 + (inclineIndex - 1) * 0.3
    #print(f"Creating GPX points for tuple: running for {seconds}s, at {metersPerSecond}m/s, on incline {inclineDegrees}%")
    #elevationClimbed = 

    for second in range(seconds):
        point = waypoint.Waypoint()
        point.lat, point.lon = currentLat, currentLon
        point.ele = currentEle
        base_timestamp += timedelta(seconds=1)
        point.time = base_timestamp

        trackSegment.points.append(point)

        # in this 1 second interval we ran `metersPerSecond`
        currentLat, currentLon = calculate_new_position(currentLat, currentLon, metersPerSecond) # go North !
        currentEle += compute_vertical_climb(metersPerSecond, ConvertSlopePercentToRadians(inclineDegrees))

track.trksegs.append(trackSegment)
gpx.tracks.append(track)

print(gpx.to_string())
gpx.to_file("virtual_run_elevation.gpx");