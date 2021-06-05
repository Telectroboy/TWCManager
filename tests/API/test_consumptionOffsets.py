#!/usr/bin/env python3

# test_consumptionOffsets.py
# This module tests the get and set API functions for the Consumption Offsets
# feature which allows offsets to be defined for the purpose of controlling
# artificial load or generation values

import datetime
import json
import random
import requests
import time

# Configuration
skipFailure = 1
maxRequest = datetime.timedelta(seconds=2)

# Disable environment import to avoid proxying requests
session = requests.Session()
session.trust_env = False

values = {
  "elapsed": {},
  "expected": {},
  "response": {},
  "status": {},
  "target": {},
  "tests": {}
}

def getOffsets(tag):
    # Query getConsumptionOffsets to see our current configured offsets
    try:
        response = session.get("http://127.0.0.1:8088/api/getConsumptionOffsets", timeout=30)
        values["response"][tag] = response.status_code
    except requests.Timeout:
        print("Error: Connection Timed Out at " + tag)
    except requests.ConnectionError:
        print("Error: Connection Error at " + tag)

    # Return json
    jsonOut = False
    try:
        jsonOut = response.json()
    except json.decoder.JSONDecodeError as e:
        print("Could not parse JSON at " + tag)
    except UnboundLocalError:
        print("Request object is not valid - look for connection error previously")

    return jsonOut

# Generate random offset values
values["target"]["ampsFirst"]  = random.randint(2, 6)
values["target"]["ampsSecond"] = 0
while (not values["target"]["ampsSecond"] or values["target"]["ampsFirst"] == values["target"]["ampsSecond"]):
    values["target"]["ampsSecond"] = random.randint(2, 6)

values["target"]["wattsFirst"]  = random.randint(100, 500)
values["target"]["wattsSecond"] = 0
while (not values["target"]["wattsSecond"] or values["target"]["wattsFirst"] == values["target"]["wattsSecond"]):
    values["target"]["wattsSecond"] = random.randint(100, 500)


# Test 1 - Call addConsumptionOffset with no arguments
values["expected"]["addConNoArgs"] = 400
values["tests"]["addConNoArgs"] = {}
try:
    response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset", timeout=30)
    values["elapsed"]["addConNoArgs"] = response.elapsed
    values["response"]["addConNoArgs"] = response.status_code
except requests.Timeout:
    print("Error: Connection Timed Out at addConNoArgs")
    values["tests"]["addConNoArgs"]["fail"] = 1
except requests.ConnectionError:
    print("Error: Connection Error at addConNoArgs")
    values["tests"]["addConNoArgs"]["fail"] = 1

time.sleep(2)

# Get offsets prior to adding our random offsets
values["status"]["Before"] = getOffsets("getOffsetsBefore")

# Test 2 - Call addConsumptionOffset with positive first Amps offset
values["expected"]["addConAmpsFirst"] = 204
values["tests"]["addConAmpsFirst"] = {}

data = {
    "offsetName": "First Amp Offset Positive",
    "offsetValue": values["target"]["ampsFirst"],
    "offsetUnit": "A"
}

try:
    response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset",
        json=data, timeout=30)
    values["elapsed"]["addConAmpsFirst"] = response.elapsed
    values["response"]["addConAmpsFirst"] = response.status_code
except requests.Timeout:
    print("Error: Connection Timed Out at addConAmpsFirst")
    values["tests"]["addConAmpsFirst"]["fail"] = 1
except requests.ConnectionError:
    print("Error: Connection Error at addConAmpsFirst")
    values["tests"]["addConAmpsFirst"]["fail"] = 1

values["status"]["AmpsFirst"] = getOffsets("getOffsetsAmpsFirst")

# Test 3 - Call addConsumptionOffset with negative second Amps offset
values["expected"]["addConAmpsSecond"] = 204
values["tests"]["addConAmpsSecond"] = {}

data = {
    "offsetName": "Second Amp Offset Negative",
    "offsetValue": (-1 * values["target"]["ampsSecond"]),
    "offsetUnit": "A"
}

try:
    response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset",
        json=data, timeout=30)
    values["elapsed"]["addConAmpsSecond"] = response.elapsed
    values["response"]["addConAmpsSecond"] = response.status_code
except requests.Timeout:
    print("Error: Connection Timed Out at addConAmpsSecond")
    values["tests"]["addConAmpsSecond"]["fail"] = 1
except requests.ConnectionError:
    print("Error: Connection Error at addConAmpsSecond")
    values["tests"]["addConAmpsSecond"]["fail"] = 1

values["status"]["AmpsSecond"] = getOffsets("getOffsetsAmpsSecond")

# Test 4 - Call addConsumptionOffset with positive first watts offset
values["expected"]["addConWattsFirst"] = 204
values["tests"]["addConWattsFirst"] = {}

data = {
    "offsetName": "First Watt Offset Positive",
    "offsetValue": values["target"]["wattsFirst"],
    "offsetUnit": "W"
}

try:
    response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset",
        json=data, timeout=30)
    values["elapsed"]["addConWattsFirst"] = response.elapsed
    values["response"]["addConWattsFirst"] = response.status_code
except requests.Timeout:
    print("Error: Connection Timed Out at addConWattsFirst")
    values["tests"]["addConWattsFirst"]["fail"] = 1
except requests.ConnectionError:
    print("Error: Connection Error at addConWattsFirst")
    values["tests"]["addConWattsFirst"]["fail"] = 1

values["status"]["WattsFirst"] = getOffsets("getOffsetsWattsFirst")

# Test 5 - Call addConsumptionOffset with negative second watts offset
values["expected"]["addConWattsSecond"] = 204
values["tests"]["addConWattsSecond"] = {}

data = {
    "offsetName": "Second Watts Offset Negative",
    "offsetValue": (-1 * values["target"]["wattsSecond"]),
    "offsetUnit": "W"
}

try:
    response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset",
        json=data, timeout=30)
    values["elapsed"]["addConWattsSecond"] = response.elapsed
    values["response"]["addConWattsSecond"] = response.status_code
except requests.Timeout:
    print("Error: Connection Timed Out at addConWattsSecond")
    values["tests"]["addConWattsSecond"]["fail"] = 1
except requests.ConnectionError:
    print("Error: Connection Error at addConWattsSecond")
    values["tests"]["addConWattsSecond"]["fail"] = 1

values["status"]["WattsSecond"] = getOffsets("getOffsetsWattsSecond")

# Test 6 - Call addConsumptionOffset with float value
values["expected"]["addConFloat"] = 204
values["tests"]["addConFloat"] = {}

data = {
    "offsetName": "Float Value",
    "offsetValue": 1.123456789012345678901234567890,
    "offsetUnit": "W"
}

try:
    response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset",
        json=data, timeout=30)
    values["elapsed"]["addConFloat"] = response.elapsed
    values["response"]["addConFloat"] = response.status_code
except requests.Timeout:
    print("Error: Connection Timed Out at addConFloat")
    values["tests"]["addConFloat"]["fail"] = 1
except requests.ConnectionError:
    print("Error: Connection Error at addConFloat")
    values["tests"]["addConFloat"]["fail"] = 1

values["status"]["addConFloat"] = getOffsets("getOffsetsFloat")


# Test 7 - Call addConsumptionOffset with non-Amp or Watt value
values["expected"]["addConInvalidUnit"] = 400
values["tests"]["addConInvalidUnit"] = {}

data = {
    "offsetName": "Offset with Invalid Unit",
    "offsetValue": 500,
    "offsetUnit": "Z"
}

try:
    response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset",
        json=data, timeout=30)
    values["elapsed"]["addConInvalidUnit"] = response.elapsed
    values["response"]["addConInvalidUnit"] = response.status_code
except requests.Timeout:
    print("Error: Connection Timed Out at addConInvalidUnit")
    values["tests"]["addConInvalidUnit"]["fail"] = 1
except requests.ConnectionError:
    print("Error: Connection Error at addConInvalidUnit")
    values["tests"]["addConInvalidUnit"]["fail"] = 1

values["status"]["addConInvalidUnit"] = getOffsets("getOffsetsInvalidUnit")

# Test 8 - Add offset with excessively long name
name = "Offset "
for x in range(0, 4096):
    name += str(x)

values["expected"]["addConLongName"] = 400
values["tests"]["addConLongName"] = {}

data = {
    "offsetName": name,
    "offsetValue": 5,
    "offsetUnit": "W"
}

# Test 9 - Update all existing offsets (except Tests 7 or 8) by setting them all to 5A
for offsetName in [ "First Amp Offset Positive", "Second Amp Offset Negative", 
   "First Watt Offset Positive", "Second Watts Offset Negative" ]:
    print(offsetName)
    runname = "Update " + offsetName

    values["expected"][runname] = 204
    values["tests"][runname] = {}

    data = {
        "offsetName": offsetName,
        "offsetValue": 5,
        "offsetUnit": "A"
    }

    try:
        response = session.post("http://127.0.0.1:8088/api/addConsumptionOffset",
            json=data, timeout=30)
        values["elapsed"][runname] = response.elapsed
        values["response"][runname] = response.status_code
    except requests.Timeout:
        print("Error: Connection Timed Out at %s" % runname)
        values["tests"][runname]["fail"] = 1
    except requests.ConnectionError:
        print("Error: Connection Error at %s" % runname)
        values["tests"][runname]["fail"] = 1

    values["status"][runname] = getOffsets("getOffsets" + runname)

# For each request, check that the status codes match
for reqs in values["expected"].keys():
    if values["response"].get(reqs, None):
        if values["response"][reqs] != values["expected"][reqs]:
            print("Error: Response code " + str(values["response"][reqs]) + " for test " + str(reqs) + " does not equal expected result " + str(values["expected"][reqs]))
            values["tests"][reqs]["fail"] = 1
    else:
        print("No response was found for test " + str(reqs) + ", skipping")

# Check the request times and see if any exceeded the maximum set in maxRequest
for reqs in values["elapsed"].keys():
    if values["elapsed"][reqs] > maxRequest:
        print("Error: API request " + str(reqs) + " took longer than maximum duration " + str(maxRequest) + ". Failing test")
        values["tests"][reqs]["fail"] = 1

# Check the getConsumptionOffsets output of each test
#  Test 2
#  Test 3
#  Test 4
if not values["tests"]["addConWattsFirst"]["fail"]:
    values["tests"]["addConWattsFirst"]["fail"] = 1
    for offsets in values["status"]["WattsFirst"]:
        if offsets["offsetName"] == "First Watt Offset Positive":
            if offsets["offsetValue"] == values["target"]["wattsFirst"]:
                if offsets["offsetUnit"] == "W":
                    values["tests"]["WattsFirst"]["fail"] = 0

# Test 5
if not values["tests"]["addConWattsSecond"]["fail"]:
    values["tests"]["addConWattsSecond"]["fail"] = 1
    for offsets in values["status"]["WattsSecond"]:
        if offsets["offsetName"] == "Second Watts Offset Negative":
            if offsets["offsetValue"] == values["target"]["wattsSecond"]:
                if offsets["offsetUnit"] == "W":
                    values["tests"]["addConWattsSecond"]["fail"] = 0


# Print out values dict
f = open("/tmp/twcmanager-tests/consumptionOffsets.json", "a")
f.write(str(values))
f.close()

for test in values["tests"].keys():
    if values["tests"][test].get("fail", 0):
        print("At least one test failed. Please review logs")
        if skipFailure:
            print("Due to skipFailure being set, we will not fail the test suite pipeline on this test.")
            exit(0)
        else:
            exit(255)

print("All tests were successful")
exit(0)
