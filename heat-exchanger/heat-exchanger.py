import numpy as np
import chemicals as chem
import ht
import pprint

np.set_printoptions(legacy="1.25")

# Reference
ref = chem.heat_capacity.Cp_data_Poling

print("A. Energy Balance")

def pick_cold_components(df, column_name):
    cold_component = input("Enter your cold fluid components (> 1 please separate with comma): ")
    user_inputs = [item.strip().lower() for item in cold_component.split(',')]

     # Lowercase the reference column values and keep a mapping to the original values
    reference_values = df[column_name].str.strip().tolist()
    original_values = [item.strip() for item in df[column_name]]
    
    cold_comp_list = []
    
    # Match each user input to reference values
    for user_component in user_inputs:
        if user_component in reference_values:
            # Find the index of the matched item and use it to get the original value
            index = reference_values.index(user_component)
            cold_comp_list.append(original_values[index])
        else:
            print(f"'{user_component}' not found in reference column. Please check the spelling.")
            exit()
    
    return cold_comp_list

def pick_hot_components(df, column_name):
    hot_component = input("Enter your hot fluid components (> 1 please separate with comma): ")
    user_inputs = [item.strip().lower() for item in hot_component.split(',')]

     # Lowercase the reference column values and keep a mapping to the original values
    reference_values = df[column_name].str.strip().tolist()
    original_values = [item.strip() for item in df[column_name]]
    
    hot_comp_list = []
    
    # Match each user input to reference values
    for user_component in user_inputs:
        if user_component in reference_values:
            # Find the index of the matched item and use it to get the original value
            index = reference_values.index(user_component)
            hot_comp_list.append(original_values[index])
        else:
            print(f"'{user_component}' not found in reference column. Please check the spelling.")
            exit()
    
    return hot_comp_list

def select_input(cold_comp_list, hot_comp_list):
    user_select_input = input("Input for Energy Balance, from cold or hot fluid? [enter cold/hot]: ")
    if str.lower(user_select_input) == 'cold':
        component_for_energy_bal = cold_comp_list
        return component_for_energy_bal
    elif str.lower(user_select_input) == 'hot':
        component_for_energy_bal = hot_comp_list
        return component_for_energy_bal
    else:
        print("Please enter valid value.")
        exit()
    
    print(component_for_energy_bal)

cold_component = pick_cold_components(ref, 'Chemical')

hot_component = pick_hot_components(ref, 'Chemical')

def input_mf(c_comp, h_comp):
    mf_data = {}
    combined_mf = c_comp + h_comp
    for item in combined_mf:
        flow_rate = float(input(f"Enter input flow rate for '{item}' (Kg/s): "))
        mf_data[item] = flow_rate
    return mf_data

all_massfl = input_mf(cold_component, hot_component)

ene_bal = select_input(cold_component, hot_component)

def separate_dict(user_inputs, list1, list2):
    dict_a = {key: user_inputs[key] for key in list1 if key in user_inputs}
    dict_b = {key: user_inputs[key] for key in list2 if key in user_inputs}
    return dict_a, dict_b

# Separate the dictionary into parts corresponding to the original lists
cf_data, hf_data = separate_dict(all_massfl, cold_component, hot_component)

def fraction(dict):
    # Calculate the total mass flow
    total_mf= sum(dict.values())
    
    # Create a new dictionary with relative values
    mole_fraction = {key: value / total_mf for key, value in dict.items()}
    
    return mole_fraction

cf_fraction = fraction(cf_data)
hf_fraction = fraction(hf_data)

# Asumption for operating conditions (T in K and Pressure in atm)
temp_ref = 298.15

component_data = ref[ref['Chemical'].str.strip().isin(ene_bal)].copy()

# Data tidying to remove whitespace in Chemical column
component_data['Chemical'] = component_data['Chemical'].str.strip()

eb_temp_input = float(input("Temperature input (K):"))
eb_temp_output = float(input("Temperature output (K):"))

def fluid_input_heat_capacity(df, temp_prompt):

    delta_cold_temp = temp_prompt - temp_ref

    # Loop through each components, calculate and store their heat capacity
    cp_input_components = {}
    for i in range(len(df['Chemical'])):

        component = df['Chemical'].iloc[i]
        a_value = df['a0'].iloc[i]
        b_value = df['a1'].iloc[i]
        c_value = df['a2'].iloc[i]
        d_value = df['a3'].iloc[i]
        e_value = df['a4'].iloc[i]
        mol_weight = df['MW'].iloc[i]

        result = chem.Poling(delta_cold_temp, a_value, b_value, c_value, d_value, e_value)
        result = round(result / mol_weight, 4)
        cp_input_components[component] = result

    for key in cp_input_components:
        if key in cf_fraction:
            frac = cf_fraction[key]
            cp_input_components[key] = round((cp_input_components[key] * frac), 4)
    
    return cp_input_components

def fluid_output_heat_capacity(df, temp_prompt):

    delta_hot_temp = temp_prompt - temp_ref

    # Loop through each components, calculate and store their heat capacity
    cp_output_components = {}
    for i in range(len(df['Chemical'])):

        component = df['Chemical'].iloc[i]
        a_value = df['a0'].iloc[i]
        b_value = df['a1'].iloc[i]
        c_value = df['a2'].iloc[i]
        d_value = df['a3'].iloc[i]
        e_value = df['a4'].iloc[i]
        mol_weight = df['MW'].iloc[i]

        result = chem.Poling(delta_hot_temp, a_value, b_value, c_value, d_value, e_value)
        result = round(result / mol_weight, 4)
        cp_output_components[component] = result
    
    for key in cp_output_components:
        if key in cf_fraction:
            frac = cf_fraction[key]
            cp_output_components[key] = round(cp_output_components[key] * frac, 4)
    
    return cp_output_components

eb_cp_input = fluid_input_heat_capacity(component_data, eb_temp_input)
eb_cp_output = fluid_output_heat_capacity(component_data, eb_temp_output)

print("Input heat components (J/kg/K):")
pprint.pprint(eb_cp_input)

print("Output heat components (J/kg/K):")
pprint.pprint(eb_cp_output)

# Heat transferred (Q)
def q_calculation(cp_input, cp_output, cf_data, hf_data):
    q_in_dict = {}
    q_out_dict = {}

    # Determine the appropriate eb_flow_rate dictionary
    if set(cp_input.keys()) == set(cold_component):
        eb_flow_rate_dict = cf_data
    elif set(cp_input.keys()) == set(hot_component):
        eb_flow_rate_dict = hf_data
    else:
        raise ValueError("cp_input keys must match either cold_fluid_list or hot_fluid_list")
    
    # Calculate q_in_dict
    for key in cp_input:
        if key in eb_flow_rate_dict:
            eb_flow_rate = eb_flow_rate_dict[key]
            q_in_dict[key] = cp_input[key] * eb_flow_rate
    
    # Calculate q_out_dict
    for key in cp_output:
        if key in eb_flow_rate_dict:
            eb_flow_rate = eb_flow_rate_dict[key]
            q_out_dict[key] = cp_output[key] * eb_flow_rate
    
    return q_in_dict, q_out_dict

q_in, q_out = q_calculation(eb_cp_input, eb_cp_output, cf_data, hf_data)

print("Input heat transferred:")
pprint.pprint(q_in)

print("Output heat transferred:")
pprint.pprint(q_out)

total_q_in = sum(q_in.values())
total_q_out = sum(q_out.values())

heat_load = round(abs(total_q_out - total_q_in), 4)

print("Necessary heat load is " + str(heat_load))

"""
Enough heat balance, lets jump in to the equipment design.
"""

print("B. Heat Exchanger equipment analysis")

cf_input_temp = float(input("Enter cold fluid input temperature (K): "))
cf_output_temp = float(input("Enter cold fluid output temperature (K): "))

hf_input_temp= float(input("Enter hot fluid input temperature (K): "))
hf_output_temp = float(input("Enter hot fluid output temperature (K): "))

cf_avg_temp = (cf_input_temp + cf_output_temp) / 2
hf_avg_temp = (hf_input_temp + hf_output_temp) / 2

# LMTD calculation
log_mean_td = ht.LMTD(hf_input_temp, hf_output_temp, cf_input_temp, cf_output_temp)
print("LMTD = " + str(log_mean_td))

cf_hc_data = ref[ref['Chemical'].str.strip().isin(cold_component)].copy()
hf_hc_data = ref[ref['Chemical'].str.strip().isin(hot_component)].copy()

cf_hc_calc = fluid_input_heat_capacity(cf_hc_data, cf_avg_temp)
hf_hc_calc = fluid_input_heat_capacity(hf_hc_data, hf_avg_temp)

# Try effectiveness
pprint.pprint((ht.effectiveness_NTU_method(
    mh = sum(hf_data.values()) / len(hf_data),
    mc = sum(cf_data.values()) / len(cf_data),
    Cph = sum(cf_hc_calc.values()),
    Cpc = sum(hf_hc_calc.values()),
    Thi = hf_input_temp,
    Tho = hf_output_temp,
    Tci = cf_input_temp,
    Tco = cf_output_temp
)))