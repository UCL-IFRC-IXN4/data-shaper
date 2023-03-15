# data-shaper

Simple formatter for DesInventar raw data

This tool is part of a UCL-IXN Project "Enhanced Assessments of Seasonal Hazards" with IFRC

This repository transfers the gathered data to a unique tree structure (required step before processing the data).

We used ISO-3 country codes as a consistent way for countries to be named, as different databases may have different names for the same country - Burma vs Myanmar for example.

We store all the initial raw data we need in a unique tree strucutre tree (in the form of nodes). Each node contains info about itself in “name” and initialised with an empty set of its child nodes i.e., the country node is initialised with its name and a set of month nodes.

The shaped data is stored in "data.csv" in the `./data` directory.

## Installation

```
git clone https://github.com/UCL-IFRC-IXN4/data-shaper.git
cd src
```

## Requirements

Gather data using teh data-gatherer package

## Usage

### Functions:

```
clean(raw_line)
    cleans a line of data from Desinventar

copy(list)
    copies a list of lists
```

### Usage:

To use this module run the file `src/DI-formatter.py`

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- Dylan Penney [@DylanPenney](https://www.github.com/DylanPenney)
- Omung Bhasin [@Omung789](https://www.github.com/Omung789)
- Ryan Lock [@RyanLockQr](https://www.github.com/RyanLockQr)
- Hogan Ma [@HoganMa23](https://www.github.com/HoganMa23)
