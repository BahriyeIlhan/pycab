#!/usr/bin/env python3
import os
import shutil
import datetime
import argparse
from subprocess import check_output as shell_call, CalledProcessError, STDOUT

import pandas as pd
import numpy as np
import markdown
import matplotlib.pyplot as plt
import ifcopenshell
#import ifcopenshell.geom
#import ifcopenshell.util.pset

#
# Plotting
#

def plot_barchart(filename, names, values, yaxis, values2 = None):
    # Plot
    #sns.set()
    #sns.set_palette('pastel')

    fig, ax = plt.subplots(figsize=(7.5, 6),  constrained_layout=True)

    plt.ylabel(yaxis)
    plt.xticks(rotation=90)
    # plt.xlabel
    plt.bar(names, values, color='#4C7998', label='Current', edgecolor='#4C7998')
    if values2:
        plt.bar(names, values2, color='#C5E0B4', label='Potential', edgecolor='#4C7998')

    ax.text(0.95, 0.95, 'pycab', ha='center', va='center', transform=ax.transAxes, font='Andale Mono', fontsize=12, color='grey')
    plt.legend(loc='upper right', bbox_to_anchor=(1., 0.9))

    #fig.tight_layout()
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.savefig(filename + '.svg')


def plot_benchmark(filename, benchmark_value, suggested_benchmark_value):
    #Plot
    names = ['Current (Max)','','','Current (Avg)','','','Current (Min)','2030 (Max)','','2030 (Avg)','','2030 (Min)']
    vals = [367.50, 338.10, 289.80, 275.10, 231.00, 215.25, 210.00, 178.50, 157.50, 110.25, 63.00, 42.00]

    # Choose some nice levels
    levels = [-3, -2, -2, -3, -2, -2, -3, 3, 2, 3, 2, 3]
    colors = ['#F8CBAD','#F8CBAD','#F8CBAD','#F8CBAD','#F8CBAD','#F8CBAD','#F8CBAD',
              '#93DBDB','#93DBDB','#93DBDB','#93DBDB','#93DBDB']

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(7.5, 4), constrained_layout=True)

    ax.invert_xaxis()
    ax.vlines(vals, 0, levels, colors=colors)  # The vertical stems.
    ax.plot(vals, np.zeros_like(vals), "-o", color="k", markerfacecolor="w")  # Baseline and markers on it.

    ax.plot(benchmark_value, np.zeros_like(benchmark_value), "o", color="black", markerfacecolor="w", markersize=10, fillstyle='full')
    ax.plot(benchmark_value, np.zeros_like(benchmark_value), "o", color="#4C7998", markerfacecolor="#4C7998", markersize=5, fillstyle='full')
    ax.vlines(benchmark_value, 0, [2], colors='#4C7998')

    ax.plot(suggested_benchmark_value, np.zeros_like(suggested_benchmark_value), "o", color="black", markerfacecolor="w", markersize=10, fillstyle='full')
    ax.plot(suggested_benchmark_value, np.zeros_like(suggested_benchmark_value), "o", color="#9BCA7E", markerfacecolor="#9BCA7E", markersize=5, fillstyle='full')
    ax.vlines(suggested_benchmark_value, 0, [-2], colors='#9BCA7E')

    # annotate lines
    for d, l, r in zip(vals+[benchmark_value, suggested_benchmark_value], levels + [2, -2], names + [
        'Current Building EC (' + str(round(benchmark_value)) + ')',
        'Potential Building EC (' + str(round(suggested_benchmark_value)) + ')'
    ]):
        ax.annotate(r, xy=(d, l),
                    xytext=(-3, np.sign(l) * 3), textcoords="offset points",
                    horizontalalignment="right",
                    verticalalignment="bottom" if l > 0 else "top")

    # format xaxis with 4 month intervals
    #ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    #ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.text(0.95, 0.05, 'pycab', ha='center', va='center', transform=ax.transAxes, font='Andale Mono', fontsize=12, color='grey')
    plt.xlabel('Embodied Carbon (kgCO₂/m²)')

    # remove y axis and spines
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)
    #plt.show()
    plt.savefig(filename + '.svg')

#
# Misc
#

def get_git_id():
    # get git commit id and write into header file
    try:
        git_id = shell_call(['git', 'rev-parse', 'HEAD'], cwd=os.path.split(os.path.abspath(__file__))[0],
                            stderr=STDOUT).strip()
    except CalledProcessError:
        git_id = 'UNKNOWN'
    # in python3, the return type of `shell_call` may be `bytes` but we need `str`
    if not isinstance(git_id, str):
        git_id = git_id.decode()
    return git_id


def zip_sort(*args):
    return zip(*sorted(zip(*args), reverse=True, key= lambda t: t[-1]))

#
# Report Generation
#

def parse_template_file(src, dest, replacements={}):
    '''
    Copy a file from `src` to `dest` replacing
    ``%(...)`` instructions in the standard python
    way.

    .. warning::
        If the file specified in `dest` exists, it
        is overwritten without prompt.

    :param src:
        str;
        The path to the template file.

    :param dest:
        str;
        The path to the destination file.

    :param replacements:
        dict;
        The replacements to be performed.
        The standard python replacement rules
        apply:

            >>> '%(var)s = %(value)i' % dict(
            ...     var = 'my_variable',
            ...     value = 5)
            'my_variable = 5'

    '''
    # read template file
    with open(src, 'r') as src_file:
        string = src_file.read()

    # apply replacements
    string = string % replacements

    # write parsed file
    with open(dest, 'w') as dest_file:
        dest_file.write(string)


def generate_report(ifc_filename, replacement_dict):

    # Generate markdown
    parse_template_file('report_template.md',os.path.join('reports',ifc_filename,'report.md'),replacement_dict)
    shutil.copy('markdown.css',os.path.join('reports',ifc_filename,'markdown.css'))

    # Generate HTML
    html_template = """<!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>pycab report</title>
        <link href="markdown.css" rel="stylesheet">
        <style>
            body {
                font-family: Helvetica,Arial,sans-serif;
            }
            code, pre {
                font-family: monospace;
            }
            .container {
                margin: auto;
                width : 80%;
            }
        </style>
    </head>
    <body>
    <div class="container">
    <div class="markdown-body">
    {{content}}
    </div>
    </div>
    </body>
    </html>
    """
    with open(os.path.join('reports',ifc_filename,'report.md')) as f:
        html = markdown.markdown(
            f.read(),
            extensions = ['extra', 'smarty'],
            output_format='html5'
        )
    html = html_template.replace('{{content}}', html)
    with open(os.path.join('reports',ifc_filename,'report.html'), 'w') as f:
        f.write(html)

#
# Parsing
#

def parse_ec_code(ec_code):
    ec, ec_class, ec_id = ec_code.split('-')
    assert ec == 'EC'
    return (ec_class, ec_id)


def dump(element):
    print('---------- begin dump ----------')
    for definition in element.IsDefinedBy:
        print('D  ', definition)
        if definition.is_a('IfcRelDefinesByProperties'):
            print('    ', definition.RelatingPropertyDefinition.Name)
            if definition.RelatingPropertyDefinition.is_a('IfcPropertySet'):
                for sub_definition in definition.RelatingPropertyDefinition.HasProperties:
                    print('     ', sub_definition.Name)
        print(definition)

    for assoc in element.HasAssociations:
        print('A  ', assoc)
    print('---------- end dump ----------')


def get_quantities(element_quantity):
    quantities = {}
    for quantity in element_quantity.Quantities:
        if quantity.is_a('IfcQuantityLength'):
            quantities[quantity.Name] = quantity.LengthValue
        elif quantity.is_a('IfcQuantityArea'):
            quantities[quantity.Name] = quantity.AreaValue
        elif quantity.is_a('IfcQuantityVolume'):
            quantities[quantity.Name] = quantity.VolumeValue
    return quantities


def get_extent(element):
    # Return dictionary of quantities for BaseQuantities
    for definition in element.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            related_data = definition.RelatingPropertyDefinition
            if related_data.is_a('IfcElementQuantity'):
                if related_data.Name == 'BaseQuantities':
                    return get_quantities(related_data)


def get_element_properties(element):
    # Build dictionary of 'Embodied Carbon' and 'MassDensity'
    property_data = {'IsExternal': False}
    embodied_carbon = False
    mass_density = False
    for definition in element.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            related_data = definition.RelatingPropertyDefinition
            if related_data.is_a('IfcPropertySet'):
                if related_data.Name in ('Pset_DoorCommon', 'Pset_WindowCommon', 'Pset_StairCommon'):
                    for prop in related_data.HasProperties:
                        if prop.Name == 'IsExternal':
                            property_data['IsExternal'] = True if prop.NominalValue.wrappedValue is True else False
                if related_data.Name == 'EC_Pset_EmbodiedCarbon':
                    for prop in related_data.HasProperties:
                        # print(property)
                        if prop.Name == 'EmbodiedCarbon':
                            embodied_carbon = prop.NominalValue.wrappedValue
                        elif prop.Name == 'MassDensity':
                            mass_density = prop.NominalValue.wrappedValue
    if embodied_carbon and mass_density:
        property_data['Element'] = {
            'EmbodiedCarbon': embodied_carbon,
            'MassDensity': mass_density
        }
    return property_data


def get_material_properties(element):
    # Build dictionary of 'Embodied Carbon' and 'MassDensity'
    property_data = {'IsExternal': False}
    for definition in element.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            related_data = definition.RelatingPropertyDefinition
            if related_data.is_a('IfcPropertySet'):
                if related_data.Name in ('Pset_WallCommon', 'Pset_SlabCommon'):
                    for prop in related_data.HasProperties:
                        if prop.Name == 'IsExternal':
                            property_data['IsExternal'] = True if prop.NominalValue.wrappedValue is True else False
                if related_data.Name == 'Material Properties':
                    for property in related_data.HasProperties:
                        # print(property.Name)
                        for sub_property in property.HasProperties:
                            # print('here',sub_property.Name)
                            sub_property_name = sub_property.Name
                            # print(sub_property_name)
                            for sub_sub_property in sub_property.HasProperties:
                                if sub_sub_property.Name == 'Embodied Carbon':
                                    embodied_carbon = sub_sub_property.NominalValue.wrappedValue
                                    if embodied_carbon.endswith(' (kgCO₂/kg)'):
                                        embodied_carbon = float(embodied_carbon[:-11])
                                elif sub_sub_property.Name == 'MassDensity':
                                    mass_density = sub_sub_property.NominalValue.wrappedValue
                            if embodied_carbon and mass_density:
                                property_data[sub_property_name] = {
                                    'EmbodiedCarbon': embodied_carbon,
                                    'MassDensity': mass_density
                                }
    return property_data


def get_material_names(element):
    # Build dictionary of names e.g. 'Component 1' = 'Slate Shingle, Roof'
    names_data = {}
    for definition in element.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            related_data = definition.RelatingPropertyDefinition
            if related_data.is_a('IfcPropertySet'):
                if related_data.Name == 'Material Properties':
                    for prop in related_data.HasProperties:
                        component_name = prop.Name
                        for sub_property in prop.HasProperties:
                            names_data[component_name] = sub_property.Name
    return names_data


def get_element_type(element):
    for definition in element.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByType'):
            if definition.RelatingType.is_a('IfcSlabType'):
                return definition.RelatingType.PredefinedType


def yield_material_layers(element, material_names={}):
    element_type = get_element_type(element)

    if element_type == 'ROOF':
        for definition in element.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                related_data = definition.RelatingPropertyDefinition
                if related_data.is_a('IfcElementQuantity'):
                    if related_data.Name == 'Component Quantities':
                        for quantity in related_data.Quantities:
                            # print(quantity.Name)
                            for sub_quantity in quantity.HasQuantities:
                                if sub_quantity.is_a('IfcQuantityLength'):
                                    if sub_quantity.Name == 'Skin Thickness':
                                        material_layer_thickness = sub_quantity.LengthValue
                            yield {'Name': quantity.Name, 'LayerThickness': material_layer_thickness}
    else:
        for assoc in element.HasAssociations:
            if assoc.is_a('IfcRelAssociatesMaterial'):
                if assoc.RelatingMaterial.is_a('IfcMaterialLayerSetUsage'):
                    # print('  ', assoc.RelatingMaterial.ForLayerSet.LayerSetName)
                    for material_layer in assoc.RelatingMaterial.ForLayerSet.MaterialLayers:
                        yield {'Name': material_layer.Material.Name, 'LayerThickness': material_layer.LayerThickness}


def get_building_properties(building):
    building_properties = {}
    for definition in building.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            related_data = definition.RelatingPropertyDefinition
            if related_data.is_a('IfcPropertySet'):
                if related_data.Name == 'Pset_BuildingCommon':
                    for prop in related_data.HasProperties:
                        building_properties[prop.Name] = str(prop.NominalValue.wrappedValue)
    return building_properties


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A python tool for calculating the embodied carbon of IFC files.')
    parser.add_argument('-i','--ifcfile', action='store', type=str, required=True, help='the IFC file to process', metavar="IFC_FILE")
    parser.add_argument('-d','--dbfile', action='store', type=str, required=False, help='the material database file', default='EC_MaterialsDB.csv', metavar="DATABASE_FILE")
    args = parser.parse_args()

    ifc_filename, _ = os.path.splitext(os.path.basename(args.ifcfile))

    # Generate report directory
    os.makedirs(os.path.join('reports',ifc_filename), exist_ok=True)

    # Parse file
    ifc_file = ifcopenshell.open(args.ifcfile)

    area_type_dictionary = {
        'Wall': 'NetSideArea',
        'Slab': 'NetArea'
    }

    element_counts = {
        'Wall': {'Number': 0, 'Carbon': 0},
        'Slab': {'Number': 0, 'Carbon': 0},
        'Roof': {'Number': 0, 'Carbon': 0},
        'Door': {'Number': 0, 'Carbon': 0},
        'Window': {'Number': 0, 'Carbon': 0},
        'Stair': {'Number': 0, 'Carbon': 0}
    }

    element_dict = {}
    element_dict['Wall'] = {}
    element_dict['Slab'] = {}
    element_dict['Roof'] = {}
    element_dict['Door'] = {}
    element_dict['Window'] = {}
    element_dict['Stair'] = {}

    print('Processing Project...')
    buildings = ifc_file.by_type('IfcBuilding')
    if len(buildings) > 1:
        raise Exception('Can not parse IFC files containing multiple IfcBuilding (not yet supported)')

    building_properties = get_building_properties(buildings[0])

    #print('Processing Roofs...')
    roofs = ifc_file.by_type('IfcRoof')
    if len(roofs) > 0:
        raise Exception('Can not parse IFC files containing IfcRoof (user must export roofs as IfcSlab)')

    print('Processing Walls...')
    walls = ifc_file.by_type('IfcWall')
    for wall in walls:
        element_counts['Wall']['Number'] += 1

        quantities = get_extent(wall)
        material_properties = get_material_properties(wall)

        # Iterate over material layers
        total_wall_carbon = 0
        material_layer_dict = {}
        for material_layer in yield_material_layers(wall):
            # Assuming thickness in mm, areas in m^2, embodied_carbon in kgCO2/kg, mass_density in kg/m^3
            embodied_carbon = material_properties[material_layer['Name']]['EmbodiedCarbon']
            mass_density = material_properties[material_layer['Name']]['MassDensity']
            total_layer_carbon = material_layer['LayerThickness'] / 1000. * \
                                 quantities['NetSideArea'] * \
                                 embodied_carbon * \
                                 mass_density
            total_wall_carbon += total_layer_carbon
            if material_layer['Name'] in material_layer_dict:
                material_layer_dict[material_layer['Name']] += total_layer_carbon
            else:
                material_layer_dict[material_layer['Name']] = total_layer_carbon
        element_dict['Wall'][wall.Name + ' (' + wall.GlobalId + ')'] = {
            'IsExternal': material_properties['IsExternal'],
            'Area': quantities['NetSideArea'],
            'Layers': material_layer_dict
        }
        element_counts['Wall']['Carbon'] += total_wall_carbon

    print('Processing Slabs/Roofs...')
    slabs = ifc_file.by_type('IfcSlab')
    for slab in slabs:
        if get_element_type(slab) == 'ROOF':
            element_counts['Roof']['Number'] += 1
        else:
            element_counts['Slab']['Number'] += 1

        quantities = get_extent(slab)
        material_properties = get_material_properties(slab)
        material_names = get_material_names(slab)
        #print(material_names)

        # Iterate over material layers
        total_slab_carbon = 0
        material_layer_dict = {}
        for material_layer in yield_material_layers(slab, material_names):
            if material_layer['Name'] in material_properties:
                embodied_carbon = material_properties[material_layer['Name']]['EmbodiedCarbon']
                mass_density = material_properties[material_layer['Name']]['MassDensity']
            else:
                embodied_carbon = material_properties[material_names[material_layer['Name']]]['EmbodiedCarbon']
                mass_density = material_properties[material_names[material_layer['Name']]]['MassDensity']

            # Assuming thickness in mm, areas in m^2, embodied_carbon in kgCO2/kg, mass_density in kg/m^3
            total_layer_carbon = material_layer['LayerThickness'] / 1000. * \
                                 quantities['NetArea'] * \
                                 embodied_carbon * \
                                 mass_density
            total_slab_carbon += total_layer_carbon
            if material_layer['Name'] in material_properties:
                material_layer_dict[material_layer['Name']] = total_layer_carbon
            else:
                material_layer_dict[material_names[material_layer['Name']]] = total_layer_carbon

        if get_element_type(slab) == 'ROOF':
            element_counts['Roof']['Carbon'] += total_slab_carbon
            element_dict['Roof'][slab.Name + ' (' + slab.GlobalId + ')'] = {
                'IsExternal' : material_properties['IsExternal'],
                'Area': quantities['NetArea'],
                'Layers': material_layer_dict
            }
        else:
            element_counts['Slab']['Carbon'] += total_slab_carbon
            element_dict['Slab'][slab.Name + ' (' + slab.GlobalId + ')'] = {
                'IsExternal' : material_properties['IsExternal'],
                'Area': quantities['NetArea'],
                'Layers': material_layer_dict
            }

    print('Processing Doors...')
    doors = ifc_file.by_type('IfcDoor')
    for door in doors:
        element_counts['Door']['Number'] += 1
        quantities = get_extent(door)
        door_properties = get_element_properties(door)

        # Assuming volumne in m^3, embodied_carbon in kgCO2/kg, mass_density in kg/m^3
        embodied_carbon = door_properties['Element']['EmbodiedCarbon'] * door_properties['Element']['MassDensity'] * \
                          quantities['Volume']
        element_counts['Door']['Carbon'] += embodied_carbon
        composite_layer = 'External Door Composite' if door_properties['IsExternal'] else 'Internal Door Composite'
        element_dict['Door'][door.Name + ' (' + door.GlobalId + ')'] = {
            'IsExternal' : door_properties['IsExternal'],
            'Layers': {composite_layer: embodied_carbon}
        }

    print('Processing Windows/Skylights...')
    windows = ifc_file.by_type('IfcWindow')
    for window in windows:
        element_counts['Window']['Number'] += 1
        quantities = get_extent(window)
        window_properties = get_element_properties(window)

        # Assuming volumne in m^3, embodied_carbon in kgCO2/kg, mass_density in kg/m^3
        embodied_carbon = window_properties['Element']['EmbodiedCarbon'] * window_properties['Element']['MassDensity'] * \
                          quantities['Volume']
        element_counts['Window']['Carbon'] += embodied_carbon
        element_dict['Window'][window.Name + ' (' + window.GlobalId + ')'] = {
            'IsExternal': window_properties['IsExternal'],
            'Layers': {'Window Composite': embodied_carbon}
        }

    print('Processing Stairs...')
    stairs = ifc_file.by_type('IfcStair')
    for stair in stairs:
        element_counts['Stair']['Number'] += 1
        quantities = get_extent(stair)
        stair_properties = get_element_properties(stair)

        # Assuming volumne in m^3, embodied_carbon in kgCO2/kg, mass_density in kg/m^3
        embodied_carbon = stair_properties['Element']['EmbodiedCarbon'] * stair_properties['Element']['MassDensity'] * \
                          quantities['NetVolume']
        # print('  ', 'embodied_carbon', embodied_carbon, 'kgCO2')
        element_counts['Stair']['Carbon'] += embodied_carbon
        element_dict['Stair'][stair.Name + ' (' + stair.GlobalId + ')'] = {
            'IsExternal': stair_properties['IsExternal'],
            'Layers': {'Stair Composite': embodied_carbon}
        }

    #
    # Find Replacements
    #
    print('Processing Replacements...')

    # get list of materials
    material_list = set()
    for element_key, element_val in element_dict.items():
        for sub_key, sub_val in element_val.items():
            for material_key in sub_val['Layers'].keys():
                material_list.add(material_key)
    material_list = list(material_list)

    # process replacement database
    cmp_tol = 1e-5 # Tolerance when comparing floats
    ec_dataframe = pd.read_csv(args.dbfile,sep=';')
    ec_dataframe['Name'] = ec_dataframe['Name'].apply(lambda x: str(x).strip())
    ec_dataframe['EC_Class'] = ec_dataframe['ID'].apply(lambda x: str(x).split('-')[1])
    ec_dataframe['EC_ID'] = ec_dataframe['ID'].apply(lambda x: str(x).split('-')[2])
    ec_dataframe['EC_Per_Volume'] = ec_dataframe['EmbodiedCarbon(kgCO2e/kg)'].apply(lambda x: float(str(x).replace(',','.'))) * \
                                    ec_dataframe['Density'].apply(lambda x: float(str(x).replace(',','.')))
    # build replacement dict
    ec_replacements_dict = {}
    min_ec_dict = {}
    for material in material_list:
        material_dataframe =  ec_dataframe.loc[ec_dataframe['Name'] == material.strip()]
        if len(material_dataframe) > 1:
            raise LookupError('Found more than one entry in database for: ' + material.strip() )
        elif len(material_dataframe) == 0:
            print('WARNING: did not find material %s in database' % material.strip())
        elif len(material_dataframe) == 1:
            # Attempt to find replacement material
            class_dataframe = ec_dataframe.loc[ec_dataframe['EC_Class'] == material_dataframe.squeeze().at['EC_Class']]
            if class_dataframe.EC_Per_Volume.min() < material_dataframe.squeeze().at['EC_Per_Volume'] - cmp_tol:
                min_ec_dict[material.strip()] = class_dataframe.EC_Per_Volume.min()
                possible_replacements = class_dataframe[class_dataframe.EC_Per_Volume == class_dataframe.EC_Per_Volume.min()]
                if len(possible_replacements) > 0:
                    ec_replacements_dict[material_dataframe.squeeze().at['Name']] = pd.concat([
                            material_dataframe[['ID','Name','EC_Per_Volume']],
                            possible_replacements[['ID','Name','EC_Per_Volume']]
                        ])
            else:
                min_ec_dict[material.strip()] = material_dataframe.squeeze().at['EC_Per_Volume']

    building_area_internal = 0
    material_counts = {}
    element_counts = {}
    for element_key, element_val in element_dict.items():
        if element_key == 'Slab':
            for sub_key, sub_val in element_val.items():
                if not sub_val['IsExternal']:
                    building_area_internal += sub_val['Area']
        for sub_key, sub_val in element_val.items():
            for material_key, material_value in sub_val['Layers'].items():
                # build current material counts
                if material_key in material_counts:
                    material_counts[material_key.strip()] += material_value
                else:
                    material_counts[material_key.strip()] = material_value
                # build current element counts
                if sub_val['IsExternal']:
                    element_key_name = 'External' + element_key.strip()
                else:
                    element_key_name = element_key.strip()
                if element_key_name in element_counts:
                    element_counts[element_key_name] += material_value
                else:
                    element_counts[element_key_name] = material_value

    # build min material counts
    min_material_counts = {}
    for material in material_list:
        material_key = material.strip()
        if not ec_dataframe.loc[ec_dataframe['Name'] == material_key].squeeze().empty:
            new_ec = material_counts[material_key] * min_ec_dict[material_key] / float(
                ec_dataframe.loc[ec_dataframe['Name'] == material_key].squeeze().at['EC_Per_Volume'])
            min_material_counts[material_key] = new_ec
        else:
            min_material_counts[material_key] = material_counts[material_key] # current == suggested

    # build min element counts
    min_element_counts = {}
    for element_key, element_val in element_dict.items():
        for sub_key, sub_val in element_val.items():
            for material_key, material_value in sub_val['Layers'].items():
                if not ec_dataframe.loc[ec_dataframe['Name'] == material_key.strip()].squeeze().empty:
                    new_ec = material_value * min_ec_dict[material_key.strip()] / float(
                        ec_dataframe.loc[ec_dataframe['Name'] == material_key.strip()].squeeze().at['EC_Per_Volume'])
                else:
                    new_ec = material_value
                if sub_val['IsExternal']:
                    element_key_name = 'External' + element_key.strip()
                else:
                    element_key_name = element_key.strip()
                if element_key_name in min_element_counts:
                    min_element_counts[element_key_name] += new_ec
                else:
                    min_element_counts[element_key_name] = new_ec


    sorted_material_names = list(material_counts.keys())
    sorted_material_values = [material_counts[sorted_material_names] for sorted_material_names in sorted_material_names]
    sorted_material_names, sorted_material_values = zip_sort(sorted_material_names, sorted_material_values)
    plot_min_values = []
    true_min_values = []
    true_saving_values = []
    for name, value in zip(sorted_material_names, sorted_material_values):
        if not ec_dataframe.loc[ec_dataframe['Name'] == name.strip()].squeeze().empty:
            new_ec = value * min_ec_dict[name] / float(ec_dataframe.loc[ec_dataframe['Name'] == name].squeeze().at['EC_Per_Volume'])
            plot_min_values.append(new_ec)
            true_min_values.append(new_ec)
            true_saving_values.append(value - new_ec)
        else:
            plot_min_values.append(material_counts[name]) # if no suggestion, do not plot a suggested bar
            true_min_values.append(material_counts[name])
            true_saving_values.append(0.)

    # Plot 2
    plot_barchart(os.path.join('reports',ifc_filename,'material_counts'), sorted_material_names, sorted_material_values, 'Total kgCO₂', plot_min_values)

    # Replacement Tables
    names, values, true_min_values, true_saving_values = zip_sort(sorted_material_names, sorted_material_values, true_min_values, true_saving_values)
    true_min_values_dict = {names[i]: true_min_values[i] for i in range(len(names))}
    true_saving_values_dict = {names[i]: true_saving_values[i] for i in range(len(names))}
    ec_replacements_str = []
    i = 1
    for name in names:
        if name in ec_replacements_dict:
            ec_replacements_str.append(
                '\n#### %d. %s: <span style="color:#4C7998">%.0f kgCO₂</span> / <span style="color:#9BCA7E">%.0f kgCO₂</span> (Saving %.0f kgCO₂)  \n' % (
                i, name, material_counts[name], true_min_values_dict[name], true_saving_values_dict[name]))
            ec_replacements_str.append(ec_replacements_dict[name].to_markdown(
                index=False,
                headers=['ID','Name','EC/m³'],
                floatfmt='.2f')
            )
            i = i + 1
    ec_replacements_str = '\n'.join(ec_replacements_str)

    # Plot 3
    element_rename_dict = {
        'ExternalSlab': 'Substructure',
        'ExternalWall': 'External Walls',
        'Slab': 'Upper Floors',
        'Wall': 'Internal Walls',
        'ExternalRoof': 'Roof',
        'ExternalDoor': 'External Doors',
        'Window': 'Windows',
        'Stair': 'Stairs',
        'Door': 'Internal Doors'
    }
    names = list(element_counts.keys())
    values = list(element_counts[name] for name in names)
    min_values = list(min_element_counts[name] for name in names)
    new_names = [element_rename_dict[n] for n in names]
    new_names, values, min_values = zip_sort(new_names, values, min_values)
    plot_barchart(os.path.join('reports',ifc_filename,'element_counts'), new_names, values, 'Total kgCO₂', min_values)

    # Generate Report
    building_ec = sum(element_counts.values())
    replacement_dict = {}
    replacement_dict['Date'] = datetime.date.today().strftime("%d/%m/%Y")
    replacement_dict['GitID'] = get_git_id()[:7]
    replacement_dict['ECReplacements'] = ec_replacements_str
    replacement_dict['BuildingPotentialEC'] = sum(true_min_values_dict.values())
    replacement_dict['BuildingPotentialECPerAreaInternal'] = sum(true_min_values_dict.values()) / building_area_internal
    replacement_dict['BuildingAreaInternal'] = building_area_internal
    replacement_dict['BuildingEC'] = building_ec
    replacement_dict['BuildingECPerAreaInternal'] = building_ec/building_area_internal
    replacement_dict['IFCFilename'] = ifc_filename
    replacement_dict.update(building_properties)

    # Plot 1
    plot_benchmark(os.path.join('reports',ifc_filename,'benchmark'), building_ec/building_area_internal, replacement_dict['BuildingPotentialECPerAreaInternal'])

    generate_report(ifc_filename, replacement_dict)

    # TODO, compare with Leti guide and recompute with new materials (for Bahriye)
