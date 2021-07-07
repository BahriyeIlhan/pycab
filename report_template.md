# Embodied Carbon Report (`%(IFCFilename)s.ifc`)

Below is a summary of the embodied carbon in your project.

## Project Summary

**Building Name**: %(BuildingID)s  
**Year Of Construction**: %(YearOfConstruction)s  
**Location**: %(Location)s  
**Building Type**: %(BuildingType)s  

## Embodied Carbon Overview

| Property                       | Value                                     |
| ------------------------------ | ----------------------------------------- |
| **Building Internal Area**     | %(BuildingAreaInternal)20.2f m²           |
| **Total Embodied Carbon**      | %(BuildingEC)20.2f                        |
| **Total Embodied Carbon/m²**   | %(BuildingECPerAreaInternal)20.2f kgCO₂/m²|

### Benchmark

![Benchmark Plot](benchmark.svg)

### Elements

![Element Plot](element_counts.svg)

### Materials

![Material Plot](material_counts.svg)

