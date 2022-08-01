import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("FeatureFlags")

# ADD SETTINGS TO SECTION
config_file.set("FeatureFlags", "establish_connection", "False")
config_file.set("FeatureFlags", "retrieve_all_files", "False")
config_file.set("FeatureFlags", "retrieve_specific_file", "False")

# SAVE CONFIG FILE
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()