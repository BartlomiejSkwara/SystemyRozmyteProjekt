import  pkg_resources
# 1. Create a new fuzzy system object

# 2. Define the input variable (oxygen flow) and its fuzzy sets
#    Each FuzzySet is defined by a list of [x, y] points that form a polygon.
S_low = sf.FuzzySet(points=[[0, 1.], [1., 1.], [1.5, 0]], term="low_flow")
S_medium = sf.FuzzySet(points=[[0.5, 0], [1.5, 1.], [2.5, 1], [3., 0]], term="medium_flow")
S_high = sf.FuzzySet(points=[[2., 0], [2.5, 1.], [3., 1.]], term="high_flow")

# Add the linguistic variable 'OXI' to the system
FS.add_linguistic_variable("OXI", sf.LinguisticVariable([S_low, S_medium, S_high]))

# 3. Define the output values for the Sugeno rules
FS.set_crisp_output_value("LOW_POWER", 0)       # Constant output for low oxygen
FS.set_crisp_output_value("MEDIUM_POWER", 25)   # Constant output for medium oxygen
FS.set_output_function("HIGH_FUN", "OXI**2")    # Mathematical function for high oxygen

# 4. Define the fuzzy rules
RULE1 = "IF (OXI IS low_flow) THEN (POWER IS LOW_POWER)"
RULE2 = "IF (OXI IS medium_flow) THEN (POWER IS MEDIUM_POWER)"
RULE3 = "IF (NOT (OXI IS low_flow)) THEN (POWER IS HIGH_FUN)"
FS.add_rules([RULE1, RULE2, RULE3])

# 5. Set an input value and perform Sugeno inference
FS.set_variable("OXI", 0.51)
output = FS.Sugeno_inference(['POWER'])

# 6. Print the result
print(f"The calculated heating power is: {output['POWER']}")