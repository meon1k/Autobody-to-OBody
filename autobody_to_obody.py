import os
import csv
import sys
import configparser
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config

# dataclass
# {"Skyrim.esm": ["00013BB8", "00013BBD"]}
Filter = dict[str,list[str]]
# {"Skyrim.esm": {"00013BA3": ["Bardmaid"],"00013BA2": ["Wench Preset", "IA - Demonic", "Tasty Temptress - BHUNP Preset (Nude)"]}}
PluginFilter = dict[str, dict[str, list[str]]]
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class OBody:
    npc_form_id: PluginFilter = field(default_factory=dict, metadata=config(field_name="npcFormID"))
    npc: Filter = field(default_factory=dict)
    faction_female: Filter = field(default_factory=dict)
    faction_male: Filter = field(default_factory=dict)
    npc_plugin_female: Filter = field(default_factory=dict)
    npc_plugin_male: Filter = field(default_factory=dict)
    race_female: Filter = field(default_factory=dict)
    race_male: Filter = field(default_factory=dict)
    blacklisted_npcs: list[str] = field(default_factory=list)
    blacklisted_npcs_form_id: Filter = field(default_factory=dict, metadata=config(field_name="blacklistedNpcsFormID"))
    blacklisted_npcs_plugin_female: list[str] = field(default_factory=list)
    blacklisted_npcs_plugin_male: list[str] = field(default_factory=list)
    blacklisted_races_female: list[str] = field(default_factory=dict)
    blacklisted_races_male: list[str] = field(default_factory=dict)
    blacklisted_outfits_from_orefit_form_id: Filter = field(default_factory=dict, metadata=config(field_name="blacklistedOutfitsFromORefitFormID"))
    blacklisted_outfits_from_orefit: list[str] = field(default_factory=dict, metadata=config(field_name="blacklistedOutfitsFromORefit"))
    blacklisted_outfits_from_orefit_plugin: list[str] = field(default_factory=list, metadata=config(field_name="blacklistedOutfitsFromORefitPlugin"))
    outfits_force_refit_form_id: Filter = field(default_factory=dict, metadata=config(field_name="outfitsForceRefitFormID"))
    outfits_force_refit: list[str] = field(default_factory=list)
    blacklisted_presets_from_random_distribution: list[str] = field(default_factory=dict)
    blacklisted_presets_show_in_obody_menu: bool = field(default=True, metadata=config(field_name="blacklistedPresetsShowInOBodyMenu"))

# paths
DEFAULT_OBODY_JSON_OUTPUT_PATH = r"OBody_presetDistributionConfig.json"
DEFAULT_STATISTICS_OUTPUT_PATH = r"statistics.csv"
AUTOBODY_CONFIG = r"morphs.ini"

current_path = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False): # if bundled in a one-file executable
    current_path = os.path.dirname(sys.executable)

input_morphs_ini_path = ""
output_obody_json_path = ""
output_csv = False
output_statistics_csv_path = ""

config_path = os.path.join(current_path, "config.ini")
if os.path.exists(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    input_morphs_ini_path = config["CONFIGS"]["input_morphs_ini_path"]
    output_obody_json_path = config["CONFIGS"]["output_obody_json_path"]
    output_csv = bool(config["CONFIGS"].get("output_csv", False))
    output_statistics_csv_path = config["CONFIGS"]["output_statistic_csv_path"]

def use_path(file_name, file_path="", file_required=False):
    if file_path == "":
        local_file = os.path.join(current_path, file_name)
        if file_required and os.path.exists(local_file) is False:
            print(local_file)
            print("file_required=",file_required)
            error = file_name + " is required and cannot be found! The script seems to be in a wrong directory"
            safe_exit(error)
        else:
            return local_file
    else:
        if file_required and os.path.exists(file_path) is False:
            error = file_name + " is required and cannot be found! Check your config.ini!"
            safe_exit(error)
        else:
            return file_path

def add_data(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = {}
    dictionary[key] = value
    
def safe_exit(error = None):
    if error is not None:
        print(error)
    os.system('pause')
    exit()

morphs_ini_path = use_path(AUTOBODY_CONFIG, input_morphs_ini_path, True)
obody_json_path = use_path(DEFAULT_OBODY_JSON_OUTPUT_PATH, output_obody_json_path)
statistic_csv_path = use_path(DEFAULT_STATISTICS_OUTPUT_PATH, output_statistics_csv_path)

# handling files
body_statistics = dict()
obody_conversion = OBody()
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
        # OBody conversion
        if race_faction == 0:
            if sex == "Female":
                add_data(obody_conversion.race_female, group, bodies)
            elif sex == "Male":
                add_data(obody_conversion.race_male, group, bodies)
            continue
        if race_faction == 1:
            if sex == "Female":
                add_data(obody_conversion.faction_female, group, bodies)
            elif sex == "Male":
                add_data(obody_conversion.faction_male, group, bodies)
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
        # OBody conversion
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
    print("bodyslide preset statistics saved in:", statistic_csv_path)
    
safe_exit()