# SPDX-FileCopyrightText: 2022 Contributors to the Power Grid Model IO project <dynamic.grid.calculation@alliander.com>
#
# SPDX-License-Identifier: MPL-2.0

import logging

import pandapower.networks
import pandas as pd
import structlog
from power_grid_model import PowerGridModel
from power_grid_model.validation import errors_to_string, validate_input_data

from power_grid_model_io.converters.pandapower_converter import PandaPowerConverter
from power_grid_model_io.converters.pgm_json_converter import PgmJsonConverter

structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG))

# Source data
pp_net = pandapower.networks.example_simple()

# Convert
pp_converter = PandaPowerConverter(std_types=pp_net._std_types)
input_data, extra_info = pp_converter.load_input_data(pp_net)

# Validate and display validation results
id_lookup = {idx: "{table:s}.{index:d}".format(**obj) for idx, obj in extra_info.items()}  # type: ignore
print(errors_to_string(validate_input_data(input_data=input_data), details=True, id_lookup=id_lookup))

# Store the source data in JSON format
converter = PgmJsonConverter(destination_file="data/pandapower/example_simple_input.json")
converter.save(data=input_data, extra_info=extra_info)

# Perform power flow calculation
grid = PowerGridModel(input_data=input_data)
output_data = grid.calculate_power_flow()

# Store the result data in JSON format
converter = PgmJsonConverter(destination_file="data/pandapower/example_simple_output.json")
converter.save(data=output_data, extra_info=extra_info)
