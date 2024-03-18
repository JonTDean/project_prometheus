# C950 NHP3 Task 2

This repository contains the implementation and tests for the C950 NHP3 Task 2. It includes various data structures and algorithms,such as hashing algorithms like `xxHash` and custom data structures such as the `muxmux hash table`.

## Structure

The project directory is structured as follows:

```zsh
.
----META SECTION
├── Readme.md
├── data
│   ├── distance_table.json
│   └── package_file.json
├── docs
│   ├── Notes.md
│   ├── algorithms
│   │   ├── aco_component_plan.md
│   │   ├── aco_pseudocode.md
│   │   ├── murmur3.md
│   │   └── xxHash.md
│   ├── course_assumptions.md
│   ├── data_structures
│   │   └── MuxMux_HashTableKanban.md
│   ├── general
│   │   ├── analytics_plan.md
│   │   └── cli_plan.md
│   └── images
│       ├── double_hash_function.png
│       └── insertion_lookup-double_hash.png
├── files
│   ├── WGUPS_Distance_Table.csv
│   └── WGUPS_Package_File.csv

---- LOGIC SECTION
└── src
    ├── main.py 
    ├── lib
    │   ├── cli
    │   │   ├── cli_manager.py
    │   │   ├── menus
    │   │   │   ├── analytics
    │   │   │   │   ├── analytics_manager.py
    │   │   │   │   ├── package_manager.py
    │   │   │   │   └── truck_manager.py
    │   │   │   ├── file_population_manager.py
    │   │   │   └── main_menu_manager.py
    │   │   └── utils
    │   │       ├── convert_csv_to_json.py
    │   │       └── meta.py
    │   ├── delivery_system
    │   │   ├── DSPackage.py
    │   │   └── DSTruck.py
    │   └── dsa
    │       ├── algorithms
    │       │   ├── VRPAlgorithm.py
    │       │   ├── ant_colony_optimization
    │       │   │   └── ACOAlgorithm.py
    │       │   ├── murmur_3.py
    │       │   ├── sieve_of_atkin.py
    │       │   └── xxHash.py
    │       └── data_structures
    │           └── muxmux_hash_table.py
    ├── tests
    │   ├── algorithms
    │   │   └── test_xxhash32.py
    │   └── data_structures
    │       └── test_hash_table.py
    └── utils
        └── load_package_from_json.py
```

## Running the Application

To run the main application, execute the following command from the root directory of the project:

```zsh
python src/main.py
```

This command runs the CLI tool for the WGUPS package delivery system, as defined in src/main.py.
## Running Tests

The project includes unit tests for its various components. To run these tests, use the -test flag with src/main.py, optionally specifying directories within the tests folder to run tests from.

### Running All Tests

To run all tests in the tests folder:
```zsh
python src/main.py -test
```

### Running Specific Tests

To run tests in specific directories or files, use the -dirs flag followed by the directory names within tests.

#### Target File:

To run tests in a specific file, such as test_xxhash32.py:

```zsh
python src/main.py -test -dirs algorithms/test_xxhash32.py
```

#### Single Directory:

For example, to run tests in a single directory, such as algorithms :

```zsh
python src/main.py -test -dirs algorithms
```

#### Multiple Directories:

To run tests in multiple directories, such as algorithms and data_structures:

```zsh
python src/main.py -test -dirs algorithms data_structures
```

#### Nested Directories:

To run tests in nested directories, such as algorithms/aco:

```zsh
python src/main.py -test -dirs algorithms/aco
```