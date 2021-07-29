#!/usr/bin/env python
import os
import glob
import json
import shutil
import re


def main(base_dir):
    all_terms = build_terms(base_dir)
    prepare_pip_package(base_dir, all_terms)
    prepare_npm_package(base_dir, all_terms)


def get_release_version():
    version = f'{os.environ["RELEASE_VERSION"]}'
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        raise Exception(f'Invalid tag name {version}. Tag name must be: number.number.number')
    return version


def prepare_pip_package(base_dir, all_terms):
    delete_directory(os.path.join(base_dir, 'pip', 'dist'))
    write_json_file(os.path.join(base_dir, 'pip', 'covid_19_terms', 'terms.json'), all_terms)


def prepare_npm_package(base_dir, all_terms):
    delete_directory(os.path.join(base_dir, 'npm', 'dist'))

    package_json = {
        'name': 'covid-19-terms',
        'version': get_release_version(),
        'description': 'JSON COVID SNOMED codes from "COVID-19 Vaccination Codes"',
        'main': 'dist/index.js',
        'files': [
            'dist/*'
        ],
        'scripts': {},
        'license': 'MIT'
    }

    shutil.copytree(os.path.join(base_dir, 'npm', 'src'), os.path.join(base_dir, 'npm', 'dist'))

    write_json_file(os.path.join(base_dir, 'npm', 'package.json'), package_json)
    write_json_file(os.path.join(base_dir, 'npm', 'dist', 'terms.json'), all_terms)


def delete_directory(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


def write_json_file(filepath, data):
    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=2))


def build_terms(base_dir):
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
        name = products_and_manufacturer['name']
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
                "name": name,
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

    return all_terms


if __name__ == "__main__":
    main(os.path.dirname(os.path.dirname(__file__)))
