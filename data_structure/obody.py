from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config

#"Skyrim.esm": ["00013BB8", "00013BBD"]
Filter = dict[str,list[str]]
#"Skyrim.esm": {"00013BA3": ["Bardmaid"],"00013BA2": ["Wench Preset", "IA - Demonic", "Tasty Temptress - BHUNP Preset (Nude)"]}
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