#Global variables 
previous_plates = 0
previous_glasses = 0
previous_weight = 0

def calculate_food_waste(total_weight, items_on_scale):
    global previous_plates, previous_glasses, previous_weight

    # Define the weight of one plate and one glass
    plate_weight = 500  # Adjust according to the actual weight of one plate in grams
    glass_weight = 200  # Adjust according to the actual weight of one glass in grams
    threshold = 20
    # Extract the number of plates and glasses from the dictionary
    num_plates = items_on_scale.get('plates', 0)
    num_glasses = items_on_scale.get('glasses', 0)
    
    # Calculate the total weight of the plates and glasses
    current_plate_weight = (num_plates-previous_plates) * plate_weight
    current_glass_weight = (num_glasses- previous_glasses) * glass_weight
    
    # Subtract the total weight of plates and glasses from the total weight
    food_waste_weight = total_weight - (current_plate_weight+ current_glass_weight+ previous_weight)

    # Update previous values
    previous_plates += num_plates
    previous_glasses += num_glasses
    previous_weight = total_weight
    

    if(food_waste_weight<=threshold):
        return 0
    else:
        return food_waste_weight
    

def plates_removed(total_weight, items_on_scale):
    global previous_plates, previous_glasses, previous_weight
    num_plates = items_on_scale.get('plates', 0)
    num_glasses = items_on_scale.get('glasses', 0)

    # Update previous values
    previous_plates += num_plates
    previous_glasses += num_glasses
    previous_weight = total_weight
