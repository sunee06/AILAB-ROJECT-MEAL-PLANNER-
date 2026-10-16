import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from PIL import Image, ImageTk


# Load the recipes from Excel
def load_recipes(filename="C:/Users/sunee/OneDrive/Desktop/recipes.xlsx"):
    df = pd.read_excel(filename, sheet_name='Recipes')
    recipes = []
    for _, row in df.iterrows():
        # Parse ingredients into dictionary
        ingredients = {}
        for item in str(row['Ingredients']).split(','):
            if ':' in item:
                ing, qty = item.split(':')
                ingredients[ing.strip().lower()] = float(qty)
        # Parse tags into list
        tags = [tag.strip().lower() for tag in str(row['Tags']).split(',')]
        recipes.append({
            'name': row['Name'],
            'ingredients': ingredients,
            'prep_time': int(row['PrepTime']),
            'tags': tags
        })
    return recipes

# Heuristic function: returns a score for each recipe
def heuristic(recipe, available_ingredients):
    total_ingredients = len(recipe['ingredients'])
    matched_ingredients = sum(1 for ing in recipe['ingredients'] if ing in available_ingredients)
    
    ingredient_score = matched_ingredients / total_ingredients  # proportion matched
    time_score = 1 / (recipe['prep_time'] + 1)  # inverse of time
    
    return 0.7 * ingredient_score + 0.3 * time_score  # weighted score

# Planning function using heuristic
def plan_recipes(recipes, diet, available_ingredients):
    scored = []
    for r in recipes:
        if diet.lower() not in r['tags']:
            continue
        score = heuristic(r, available_ingredients)
        scored.append((r, score))
    # Sort recipes by score descending
    scored.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in scored if r[1] > 0.3]  # Filter out too-low scores

# GUI code
def on_generate():
    diet = diet_var.get()
    if not diet:
        messagebox.showerror("Input Error", "Please select a diet type.")
        return
    available_raw = ingredients_entry.get()
    if not available_raw.strip():
        messagebox.showerror("Input Error", "Please enter available ingredients.")
        return
    available = set(item.strip().lower() for item in available_raw.split(','))

    plan = plan_recipes(recipes, diet, available)
    output.delete('1.0', tk.END)
    if not plan:
        output.insert(tk.END, "No meal plans match your criteria.\n")
        return
    output.insert(tk.END, "Top Recommended Meal Plans:\n\n")
    for meal in plan[:3]:  # Show top 3
        ing_list = ', '.join(meal['ingredients'].keys())
        output.insert(tk.END,
                      f"• {meal['name']} (Prep time: {meal['prep_time']} min)\n"
                      f"  Ingredients: {ing_list}\n\n")

# Load dataset once
recipes = load_recipes()

# Modern GUI using ttk and better layout
# Modern GUI using ttk and better layout
root = tk.Tk()
root.title("🍽️ Smart Meal Planner")
root.geometry("600x500")

# Load background image
bg_image = Image.open("C:/Users/sunee/OneDrive/Desktop/background.jpg")
bg_image = bg_image.resize((600, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Place background image using a Label
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


style = ttk.Style()
style.theme_use("clam")  # More modern than 'default'
style.configure("TLabel", font=("Segoe UI", 11), background="#f8f9fa")
style.configure("TButton", font=("Segoe UI", 11, "bold"), foreground="white", background="#28a745")
style.configure("TEntry", font=("Segoe UI", 11))
style.configure("TCombobox", font=("Segoe UI", 11))

# Main Frame
frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Load logo image
logo_image = Image.open("C:/Users/sunee/OneDrive/Desktop/logo.png")
logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Title frame with logo
title_frame = ttk.Frame(frame)
title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))

logo_label = tk.Label(title_frame, image=logo_photo, bg="#f8f9fa")
logo_label.pack(side='left', padx=(0, 10))

title = tk.Label(title_frame, text="Smart Personalized Meal Planner", font=("Segoe UI", 16, "bold"), bg="#f8f9fa", fg="#343a40")
title.pack(side='left')



# Diet Type
ttk.Label(frame, text="Select Diet Type:").grid(row=1, column=0, sticky='w')
diet_var = tk.StringVar()
diet_combo = ttk.Combobox(frame, textvariable=diet_var, state='readonly', width=25)
diet_combo['values'] = ('vegetarian', 'non-vegetarian', 'gluten-free')
diet_combo.grid(row=1, column=1, sticky='e', pady=5)

# Ingredients Input
ttk.Label(frame, text="Available Ingredients (comma separated):").grid(row=2, column=0, columnspan=2, sticky='w')
ingredients_entry = ttk.Entry(frame, width=60)
ingredients_entry.grid(row=3, column=0, columnspan=2, pady=5)

# Generate Button
generate_btn = ttk.Button(frame, text="🍲 Generate Meal Plan", command=on_generate)
generate_btn.grid(row=4, column=0, columnspan=2, pady=15)

# Output Text Box with Scrollbar
output_frame = ttk.Frame(frame)
output_frame.grid(row=5, column=0, columnspan=2)

output_scrollbar = ttk.Scrollbar(output_frame)
output_scrollbar.pack(side='right', fill='y')

output = tk.Text(output_frame, height=15, width=70, font=("Segoe UI", 10), wrap='word', yscrollcommand=output_scrollbar.set)
output.pack(side='left', fill='both')
output_scrollbar.config(command=output.yview)


root.mainloop()