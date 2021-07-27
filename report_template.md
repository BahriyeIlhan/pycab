# Embodied Carbon Report

**pyCAB Version**: %(GitID)s  
**Report Generation Date**: %(Date)s  

**Project Filename**: %(IFCFilename)s.ifc  
**Building Name**: %(BuildingID)s  
**Year of Construction**: %(YearOfConstruction)s  
**Location**: %(Location)s  
**Building Type**: %(BuildingType)s  

## Embodied Carbon Overview

| Description                          | Value                                               |
| :-----------------------------       | :-------------------------------------------------- |
| Internal Building Area               | %(BuildingAreaInternal)20.2f m²                     |
| Total Embodied Carbon     [A1-A3]    | %(BuildingEC)20.2f kgCO₂                            |
| Total Embodied Carbon/m²             | %(BuildingECPerAreaInternal)20.2f kgCO₂/m²          |
| Potential Embodied Carbon [A1-A3]    | %(BuildingPotentialEC)20.2f kgCO₂                   |
| Potential Embodied Carbon/m² [A1-A3] | %(BuildingPotentialECPerAreaInternal)20.2f kgCO₂/m² |

### Benchmark [¹][riba2030]

![Benchmark Plot](benchmark.svg)

## Embodied Carbon Analysis

### Embodied Carbon by Building Elements

![Element Plot](element_counts.svg)

### Embodied Carbon by Building Materials

![Material Plot](material_counts.svg)

### Replacement Suggestions

%(ECReplacements)s


[riba2030]:  https://www.architecture.com/about/policy/climate-action/2030-climate-challenge/resources "RIBA 2030 Climate Challenge Target Benchmarks Review"
