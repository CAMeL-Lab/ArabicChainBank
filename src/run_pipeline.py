import subprocess

def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(["python", script_name], check=True)
        print(f"{script_name} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")


scripts_to_run = [
    "src/merge_data.py",
    "src/build_trees.py",
    "src/visualize_trees.py"
   
]

for script in scripts_to_run:
    run_script(script)
