import os
import csv
import sys
import configparser
from data_structure import obody

DEFAULT_OBODY_JSON_OUTPUT_PATH = r"output\OBody_presetDistributionConfig.json"
DEFAULT_STATISTIC_OUTPUT_PATH = r"output\statistic.csv"
current_path = os.path.dirname(os.path.abspath(__file__))

input_morphs_ini_path = ""
output_obody_json_path = ""
output_csv = False
output_statistic_csv_path = ""

config_path = os.path.join(current_path, "config.ini")
if os.path.exists(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    input_morphs_ini_path = config["CONFIGS"]["input_morphs_ini_path"]
    output_obody_json_path = config["CONFIGS"]["output_obody_json_path"]
    output_csv = bool(config["CONFIGS"].get("output_csv", False))
    output_statistic_csv_path = config["CONFIGS"]["output_statistic_csv_path"]

def usePath(file_name, file_path="", file_required=False):
    if file_path == "":
        local_file = os.path.join(current_path, file_name)
        if file_required and os.path.exists(local_file) is False:
            error = file_name + " is required and cannot be found! The script seems to be in a wrong directory"
            sys.exit(error)
        else:
            return local_file
    else:
        if file_required and os.path.exists(file_path) is False:
            error = file_name + " is required and cannot be found! Check your options!"
            sys.exit(error)
        else:
            return file_path

def addData(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = {}
    dictionary[key] = value

morphs_ini_path = usePath("morphs.ini", input_morphs_ini_path, True)
obody_json_path = usePath(DEFAULT_OBODY_JSON_OUTPUT_PATH, output_obody_json_path)
statistic_csv_path = usePath(DEFAULT_STATISTIC_OUTPUT_PATH, output_statistic_csv_path)

body_statistics = dict()
obody_conversion = obody.OBody()
for line in open(morphs_ini_path):
    l = line.strip()
    if len(l) == 0: # empty lines
        continue
    if l[0] == ";": # comments
        continue
    sl1 = l.split("=") # "filters","bodyslide presets"
    sl2 = sl1[0].split("|")
    bodies = sl1[1].split("|")
    if l[:3] == "All": # general rules 
        sex = sl2[1]
        group = sl2[2]
        race_faction = 0
        if group[-7:] == "Faction": # if not end with Faction, then it is a race rule
            race_faction = 1
        # Obody conversion
        if race_faction == 0:
            if sex == "Female":
                addData(obody_conversion.race_female, group, bodies)
            elif sex == "Male":
                addData(obody_conversion.race_male, group, bodies)
            continue
        if race_faction == 1:
            if sex == "Female":
                addData(obody_conversion.faction_female, group, bodies)
            elif sex == "Male":
                addData(obody_conversion.faction_male, group, bodies)
            continue
        continue
    else: # NPC specific rules
        plugin_name = sl2[0]
        form_id = sl2[1]
        for body in bodies:
            if body in body_statistics:
                body_statistics[body] += 1
            else:
                body_statistics[body] = 1
        # Obody conversion
        if plugin_name not in obody_conversion.npc_form_id:
            obody_conversion.npc_form_id[plugin_name] = {}
        obody_conversion.npc_form_id[plugin_name][form_id] = bodies

with open(obody_json_path, 'w') as json_file:
    json_file.write(obody_conversion.to_json(indent=4))
print("OBody JSON saved in:", obody_json_path)

if output_csv == True:
    sorted_statistics = sorted(body_statistics.items(), key=lambda x: x[0].upper())
    with open(statistic_csv_path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(sorted_statistics)
    print("bodyslide preset statistic saved in:", statistic_csv_path)