import flet as ft
import json
import os
from foods import FOODS
foods = FOODS
PROFILE_FILE = "user_profile.json"


# ---------- CALORIE CALCULATION ----------
def calculate_daily_calories(profile):
    weight = profile["weight"]
    height = profile["height"]
    age = profile["age"]

    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    maintenance = bmr * 1.4

    if profile["goal"] == "lose":
        maintenance -= 400
    elif profile["goal"] == "gain":
        maintenance += 400

    return int(round(maintenance))


def main(page: ft.Page):
    page.title = "Daily Calories"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    profile = None

    # ---------- PROFILE STORAGE ----------
    def safe_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


    def safe_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def load_profile():
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_profile(data):
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def delete_profile():
        if os.path.exists(PROFILE_FILE):
            os.remove(PROFILE_FILE)
    def close_dialog(e=None):
        if page.overlay:
            page.overlay[-1].open = False
        page.update()

    def open_dialog(dialog: ft.AlertDialog):
        page.overlay.clear()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    # ---------- DAILY STATE ----------
    total_calories = 0.0
    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0

    # ---------- HOME CONTROLS ----------
    calories_text = ft.Text("0", size=64, weight=ft.FontWeight.BOLD)
    progress_bar = ft.ProgressBar(width=300, value=0)

    remaining_text = ft.Text("", size=16, color=ft.Colors.GREY)

    protein_text = ft.Text("Protein: 0 g", size=12)
    fat_text = ft.Text("Fat: 0 g", size=12)
    carbs_text = ft.Text("Carbs: 0 g", size=12)
    weight_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
    water_grid = ft.Column(
    spacing=6,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)


    # ---------- HOME ----------
    def update_home():
        calories_text.value = str(int(total_calories))
        progress_bar.value = min(total_calories / profile["daily_calories"], 1)

        remaining = max(profile["daily_calories"] - int(total_calories), 0)
        remaining_text.value = f"Remaining: {remaining} kcal"

        protein_text.value = f"Protein: {int(total_protein)} g"
        fat_text.value = f"Fat: {int(total_fat)} g"
        carbs_text.value = f"Carbs: {int(total_carbs)} g"

        weight_text.value = f"{profile['current_weight']:.1f} kg"
        water_grid.controls.clear()

        index = 0
        for row in range(2):
            row_controls = []
            for col in range(4):
                filled = index < profile["water_glasses"]

                row_controls.append(
                    ft.IconButton(
                        icon=ft.Icons.LOCAL_DRINK,
                        icon_color=ft.Colors.BLUE if filled else ft.Colors.GREY_400,
                        on_click=lambda e: add_water()
                    )
                )
                index += 1

            water_grid.controls.append(
                ft.Row(
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=row_controls
                )
            )

        page.update()

    def change_weight(delta):
        profile["current_weight"] = round(profile["current_weight"] + delta, 1)
        save_profile(profile)
        update_home()

    def add_water():
        if profile["water_glasses"] < 8:
            profile["water_glasses"] += 1
            save_profile(profile)
            update_home()
    def reset_day():
        nonlocal total_calories, total_protein, total_fat, total_carbs

        total_calories = 0.0
        total_protein = 0.0
        total_fat = 0.0
        total_carbs = 0.0

        profile["water_glasses"] = 0
        save_profile(profile)

        update_home()
    def confirm_reset_day(e):
        def confirm(e):
            reset_day()
            close_dialog()
    def confirm_reset_day(e):
        def confirm(e):
            reset_day()
            close_dialog()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Finish day"),
            content=ft.Text(
                "This will reset today's calories, macros and water intake.\n\n"
                "Your weight and profile will remain unchanged."
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton(
                    "Reset day",
                    icon=ft.Icons.REFRESH,
                    on_click=confirm
                ),
            ],
        )

        open_dialog(dialog)



    def show_home():
        page.controls.clear()
        page.add(
            ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        width=300,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"Hi, {profile['name']}",
                                size=16,
                                color=ft.Colors.GREY
                            ),
                            ft.IconButton(
                                icon=ft.Icons.SETTINGS,
                                on_click=lambda e: show_settings()
                            )
                        ]
                    ),
                    card(
                        title="Calories",
                        subtitle="Track your daily energy intake!",
                        content=ft.Column(
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                calories_text,
                                ft.Text("Consumed today", size=14),
                                progress_bar,
                                remaining_text,
                                ft.Row(
                                    spacing=20,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[protein_text, fat_text, carbs_text]
                            ),
                            ft.FloatingActionButton(
                                icon=ft.Icons.ADD,
                on_click=lambda e: show_add_food()
            )
        ]
    )
),

card(
    title="Weight",
    subtitle="Track your weight progress!",
    content=ft.Column(
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            weight_text,
            ft.Row(
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.REMOVE,
                        on_click=lambda e: change_weight(-0.1)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ADD,
                        on_click=lambda e: change_weight(0.1)
                    ),
                ]
            )
        ]
    )
),

card(
    title="Water",
    subtitle="Stay hydrated throughout the day!",
    content=water_grid
),
ft.TextButton(
    "Finish day",
    icon=ft.Icons.REFRESH,
    on_click=confirm_reset_day
),

                ]
            )
        )
        update_home()
    def card(title, subtitle, content):
        return ft.Container(
            width=320,
            padding=20,
            border_radius=16,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            content=ft.Column(
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        subtitle,
                        size=12,
                        color=ft.Colors.GREY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    content
                ]
            )
        )

    # ---------- SETTINGS ----------
    def show_settings():
        page.controls.clear()

        name = ft.TextField(label="Name", value=profile["name"], width=300)
        age = ft.TextField(
            label="Age",
            value=str(profile["age"]),
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        height = ft.TextField(
            label="Height (cm)",
            value=str(profile["height"]),
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        weight = ft.TextField(
            label="Weight (kg)",
            value=str(profile["weight"]),
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        calories = ft.TextField(
            label="Daily calorie goal",
            value=str(profile["daily_calories"]),
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        def on_goal_change(e):
            profile["goal"] = e.control.value
            calories.value = str(calculate_daily_calories(profile))
            page.update()

        goal_group = ft.RadioGroup(
            value=profile["goal"],
            on_change=on_goal_change,
            content=ft.Column(
                width=300,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Radio(value="lose", label="Lose weight"),
                    ft.Radio(value="maintain", label="Maintain weight"),
                    ft.Radio(value="gain", label="Gain weight"),
                ]
            )
        )

        def save_changes(e):
            profile["name"] = name.value
            profile["age"] = int(age.value)
            profile["height"] = int(height.value)
            profile["weight"] = float(weight.value)
            profile["goal"] = goal_group.value
            profile["daily_calories"] = int(calories.value)
            age_v = safe_int(age.value)
            height_v = safe_int(height.value)
            weight_v = safe_float(weight.value)
            cal_v = safe_int(calories.value)

            if None in (age_v, height_v, weight_v, cal_v):
                open_dialog(
                    ft.AlertDialog(
                        title=ft.Text("Invalid input"),
                        content=ft.Text("Please enter valid numeric values."),
                        actions=[ft.TextButton("OK", on_click=close_dialog)],
                    )
                )
                return

            save_profile(profile)
            show_home()
        
        def confirm_delete_profile(e):
            def confirm(e):
                delete_profile()
                close_dialog()
                show_onboarding_user()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Delete profile"),
                content=ft.Text(
                    "This will permanently delete your profile and all your data.\n\n"
                    "Are you sure?"
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=close_dialog),
                    ft.TextButton(
                        "Delete",
                        on_click=confirm,
                        style=ft.ButtonStyle(color=ft.Colors.RED),
                    ),
                ],
            )

            open_dialog(dialog)





        page.add(
            ft.Column(
                width=320,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Profile settings", size=26, weight=ft.FontWeight.BOLD),
                    name,
                    age,
                    height,
                    weight,
                    ft.Text("Goal"),
                    goal_group,
                    calories,
                    ft.ElevatedButton(
                        content=ft.Text("Save"),
                        on_click=save_changes
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Back"),
                        on_click=lambda e: show_home()
                    ),
                    ft.Divider(height=30),


                    ft.TextButton(
                        "Delete profile",
                        icon=ft.Icons.DELETE,
                        style=ft.ButtonStyle(color=ft.Colors.RED),
                        on_click=confirm_delete_profile
                    ),
                ]
            )
        )
        page.update()

    # ---------- MANUAL FOOD ----------
    def show_manual_food():
        page.controls.clear()

        name = ft.TextField(label="Food name", width=300)
        calories = ft.TextField(
            label="Calories",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        protein = ft.TextField(
            label="Protein (g)",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        fat = ft.TextField(
            label="Fat (g)",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        carbs = ft.TextField(
            label="Carbs (g)",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        def add_manual(e):
            nonlocal total_calories, total_protein, total_fat, total_carbs

            c = safe_float(calories.value)
            p = safe_float(protein.value)
            f = safe_float(fat.value)
            ca = safe_float(carbs.value)

            if c is None or p is None or f is None or ca is None:
                open_dialog(
                    ft.AlertDialog(
                        title=ft.Text("Invalid input"),
                        content=ft.Text("Please enter valid numbers in all fields."),
                        actions=[ft.TextButton("OK", on_click=close_dialog)],
                    )
                )
                return

            total_calories += c
            total_protein += p
            total_fat += f
            total_carbs += ca

            show_home()


        page.add(
            ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Add food manually", size=24, weight=ft.FontWeight.BOLD),
                    name,
                    calories,
                    protein,
                    fat,
                    carbs,
                    ft.ElevatedButton(
                        content=ft.Text("Add"),
                        on_click=add_manual
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Back"),
                        on_click=lambda e: show_add_food()
                    ),
                ]
            )
        )
        page.update()

    # ---------- ADD FOOD ----------
    def show_add_food():
        page.controls.clear()

        selected_food = {"name": None}

        search_input = ft.TextField(label="Search food", width=300)
        results = ft.ListView(width=300, height=160, visible=False)

        food_chip = ft.Row(
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False
        )
        amount_input = ft.TextField(
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER,
            visible=False
        )
        result_text = ft.Text("", visible=False)

        def reset_selection(e=None):
            selected_food["name"] = None
            food_chip.visible = False
            food_chip.controls.clear()
            search_input.visible = True
            search_input.value = ""
            results.controls.clear()
            results.visible = False
            amount_input.visible = False
            result_text.visible = False
            page.update()

        def calculate(amount):
            food = foods[selected_food["name"]]
            grams = (
                amount * food["unit_weight"]
                if food["measurement"] == "units"
                else amount
            )
            return (
                grams * food["calories"] / 100,
                grams * food["protein"] / 100,
                grams * food["fat"] / 100,
                grams * food["carbs"] / 100,
            )

        def on_search_change(e):
            query = search_input.value.strip().lower()
            results.controls.clear()

            if not query:
                results.visible = False
                page.update()
                return

            for name in foods:
                if query in name.lower():
                    def select_food(e, n=name):
                        selected_food["name"] = n
                        search_input.visible = False
                        results.visible = False
                        food_chip.controls[:] = [
                            ft.Text(n),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                on_click=reset_selection
                            )
                        ]
                        food_chip.visible = True
                        amount_input.label = (
                            "Units"
                            if foods[n]["measurement"] == "units"
                            else "Grams"
                        )
                        amount_input.visible = True
                        page.update()

                    results.controls.append(
                        ft.TextButton(
                            content=ft.Text(name),
                            on_click=select_food
                        )
                    )

            results.visible = True
            page.update()

        def on_amount_change(e):
            if not selected_food["name"]:
                return

            try:
                amount = float(amount_input.value)
                c, p, f, ca = calculate(amount)

                result_text.value = (
                    f"Calories: {int(c)} | "
                    f"Protein: {int(p)} g | "
                    f"Fat: {int(f)} g | "
                    f"Carbs: {int(ca)} g"
                )
                result_text.visible = True
                page.update()

            except ValueError:
                result_text.visible = False
                page.update()


        def add_food(e):
            nonlocal total_calories, total_protein, total_fat, total_carbs

            if not selected_food["name"]:
                return

            try:
                amount = float(amount_input.value)
            except (ValueError, TypeError):
                return

            c, p, f, ca = calculate(amount)
            total_calories += c
            total_protein += p
            total_fat += f
            total_carbs += ca

            show_home()


        search_input.on_change = on_search_change
        amount_input.on_change = on_amount_change

        page.add(
            ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Add food", size=24, weight=ft.FontWeight.BOLD),
                    search_input,
                    ft.TextButton(
                        "Add food manually",
                        on_click=lambda e: show_manual_food()
                    ),
                    results,
                    food_chip,
                    amount_input,
                    result_text,
                    ft.ElevatedButton(
                        content=ft.Text("Add"),
                        on_click=add_food
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Back"),
                        on_click=lambda e: show_home()
                    ),
                ]
            )
        )
        page.update()

    # ---------- ONBOARDING ----------
    def show_onboarding_user():
        page.controls.clear()

        name = ft.TextField(label="Name", width=300)
        age = ft.TextField(label="Age", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        height = ft.TextField(label="Height (cm)", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        weight = ft.TextField(label="Weight (kg)", width=300, keyboard_type=ft.KeyboardType.NUMBER)

        def continue_step(e):
            nonlocal profile

            if not name.value.strip():
                return

            age_v = safe_int(age.value)
            height_v = safe_int(height.value)
            weight_v = safe_float(weight.value)

            if age_v is None or height_v is None or weight_v is None:
                open_dialog(
                    ft.AlertDialog(
                        title=ft.Text("Invalid data"),
                        content=ft.Text("Please enter valid age, height and weight."),
                        actions=[ft.TextButton("OK", on_click=close_dialog)],
                    )
                )
                return

            profile = {
                "water_glasses": 0,
                "name": name.value.strip(),
                "age": age_v,
                "height": height_v,
                "weight": weight_v,
                "current_weight": weight_v,
            }

            show_onboarding_goal()


        page.add(
            ft.Column(
                width=320,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Welcome", size=26, weight=ft.FontWeight.BOLD),
                    name,
                    age,
                    height,
                    weight,
                    ft.ElevatedButton(
                        content=ft.Text("Continue"),
                        on_click=continue_step
                    ),
                ]
            )
        )
        page.update()

    def show_onboarding_goal():
        page.controls.clear()

        def select_goal(goal):
            profile["goal"] = goal
            profile["daily_calories"] = calculate_daily_calories(profile)
            show_calorie_plan()

        page.add(
            ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Your goal", size=26, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton(
                        content=ft.Text("Lose weight"),
                        on_click=lambda e: select_goal("lose")
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Maintain weight"),
                        on_click=lambda e: select_goal("maintain")
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Gain weight"),
                        on_click=lambda e: select_goal("gain")
                    ),
                ]
            )
        )
        page.update()

    def show_calorie_plan():
        page.controls.clear()
        page.add(
            ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Your calorie plan", size=26, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Based on your data and your goal, "
                        "your recommended intake is:"
                    ),
                    ft.Text(
                        f"{profile['daily_calories']} kcal / day",
                        size=32,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "This is an estimate. You can change it later.",
                        size=12,
                        color=ft.Colors.GREY
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Continue"),
                        on_click=lambda e: (
                            save_profile(profile),
                            show_home()
                        )
                    ),
                ]
            )
        )
        page.update()

    # ---------- APP START ----------


    loaded = load_profile()
    if loaded:
        profile = loaded

        if "current_weight" not in profile:
            profile["current_weight"] = profile["weight"]

        if "water_glasses" not in profile:
            profile["water_glasses"] = 0
        save_profile(profile)
        show_home()
    else:
        show_onboarding_user()



ft.app(target=main)
