# Embodied Carbon Report (`%(IFCFilename)s.ifc`)

Below is a summary of the embodied carbon in your project.

## Project Summary

**Building Name**: %(BuildingID)s  
**Year of Construction**: %(YearOfConstruction)s  
**Location**: %(Location)s  
**Building Type**: %(BuildingType)s  

## Embodied Carbon Overview

| Description                       | Value                                                |
| :-----------------------------    | :----------------------------------------            |
| **Internal Building Area**        | %(BuildingAreaInternal)20.2f m²                      |
| **Total Embodied Carbon** [A1-A3] | %(BuildingEC)20.2f kgCO<sub>2</sub>                  |
| **Total Embodied Carbon/m²**      | %(BuildingECPerAreaInternal)20.2f kgCO<sub>2</sub>/m²|

### Benchmark 
[based on RIBA 2030 Climate Challenge Target Benchmarks Review]

![Benchmark Plot](benchmark.png)

### Embodied Carbon by Building Elements

![Element Plot](element_counts.png)

### Embodied Carbon by Building Materials

![Material Plot](material_counts.png)

