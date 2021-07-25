#!/usr/bin/env python
import os
import glob
import json


def main(base_dir):

    all_terms = {}
    sections_dir = os.path.join(base_dir, 'sections')

    for section_file in sorted(glob.glob(sections_dir + '/*.json', recursive=False)):
        with open(section_file, 'r') as f:
            section = json.load(f)
            section_name, _ = os.path.splitext(os.path.basename(section_file))
        all_terms[section_name] = section

    products_dir = os.path.join(sections_dir, 'products')

    with open(os.path.join(products_dir, 'vtm'), 'r') as f:
        vtm = json.load(f)

    products = {
        vtm['code']: {
            "term": vtm["term"],
            "type": "VTM"
        }
    }

    for products_file in sorted(glob.glob(products_dir + '/*.json', recursive=False)):

        with open(products_file, 'r') as f:
            products_and_manufacturer = json.load(f)

        vmp = None
        amp = None
        manufacturer = products_and_manufacturer['manufacturer']
        product_set = {}
        for product in products_and_manufacturer['products']:

            snomed_code = product['code']
            product_type = product['type']

            if snomed_code in products or snomed_code in product_set:
                raise ValueError(f"product {snomed_code} is not distinct {products_file}")

            if product_type == 'VMP':
                if vmp is not None:
                    raise ValueError(f'VPM already assigned {snomed_code} {products_file}')
                vmp = product

            if product_type == 'AMP':
                if amp is not None:
                    raise ValueError(f'VPM already assigned {snomed_code} {products_file}')
                amp = product

            product_set[snomed_code] = {
                "term": product["term"],
                "type": product_type,
                "manufacturer": manufacturer,
                "rels": []
            }

        for code, product in product_set.items():

            if product['type'] != "APM":
                product["rels"].append({"type": "APM", "code": amp['code']})

            if product['type'] != "VMP":
                product["rels"].append({"type": "VMP", "code": vmp['code']})

            products[code] = product

    all_terms['products'] = products

    print(json.dumps(all_terms, indent=2))


if __name__ == "__main__":
    main(os.path.dirname(os.path.dirname(__file__)))
