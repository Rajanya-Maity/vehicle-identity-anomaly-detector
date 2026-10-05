import os
import csv
import xml.etree.ElementTree as ET

DATASET_PATH = "data/IndianVehicleDataset"
OUTPUT_FILE = "data/registry.csv"

plates = []

# Search through the dataset for XML files
for root, dirs, files in os.walk(DATASET_PATH):

    for file in files:

        if file.lower().endswith(".xml"):

            xml_path = os.path.join(root, file)

            try:
                tree = ET.parse(xml_path)
                xml_root = tree.getroot()

                for obj in xml_root.findall("object"):
                    name = obj.find("name")

                    if name is not None and name.text:
                        plate = name.text.strip()
                        plates.append(plate)

            except Exception as e:
                print(f"Could not read {xml_path}: {e}")


# Remove duplicate plate numbers
unique_plates = sorted(set(plates))


# Create registry records
registry = []

for i, plate in enumerate(unique_plates, start=1):

    registry.append({
        "tag_id": f"TAG{i:04d}",
        "registered_plate": plate,
        "vehicle_class": "unknown"
    })


# Save as CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=["tag_id", "registered_plate", "vehicle_class"]
    )

    writer.writeheader()
    writer.writerows(registry)


print(f"Created: {OUTPUT_FILE}")
print(f"Total vehicles in registry: {len(registry)}")