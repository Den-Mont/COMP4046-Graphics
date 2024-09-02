from graphics import color_rgb

# Function to convert text input to integer, defaulting to 0 if not valid
def get_int_from_input(entry):
    try:
        return int(entry.getText())
    except ValueError:
        return 0

# Function to mix colors and update the display, including K (Black)
def mix_colors(r1_input, g1_input, b1_input, k1_input, r2_input, g2_input, b2_input, k2_input, r_result, g_result, b_result, k_result, color1_display, color2_display, result_display):
    # Get RGB values for Color 1
    r1 = get_int_from_input(r1_input)
    g1 = get_int_from_input(g1_input)
    b1 = get_int_from_input(b1_input)
    k1 = get_int_from_input(k1_input)
    
    # Get RGB values for Color 2
    r2 = get_int_from_input(r2_input)
    g2 = get_int_from_input(g2_input)
    b2 = get_int_from_input(b2_input)
    k2 = get_int_from_input(k2_input)
    
    # Calculate resulting color
    r_result_value = (r1 + r2) // 2
    g_result_value = (g1 + g2) // 2
    b_result_value = (b1 + b2) // 2
    k_result_value = (k1 + k2) // 2
    
    # Set result in the input fields
    r_result.setText(str(r_result_value))
    g_result.setText(str(g_result_value))
    b_result.setText(str(b_result_value))
    k_result.setText(str(k_result_value))
    
    # Display the colors (for simplicity, K is not used in display)
    color1_display.setFill(color_rgb(r1, g1, b1))
    color2_display.setFill(color_rgb(r2, g2, b2))
    result_display.setFill(color_rgb(r_result_value, g_result_value, b_result_value))