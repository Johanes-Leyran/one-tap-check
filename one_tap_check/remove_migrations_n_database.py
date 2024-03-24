from pathlib import Path
import os
import warnings

BASE_PATH: Path = Path(__file__).parent
warnings.warn(
    """ 
        This script is only used for development only where the database in use and
        the default database is db.sqlite3
    """
)


def main():
    dirs = [i.path for i in os.scandir(BASE_PATH) if i.is_dir()]
    db_path = Path(BASE_PATH, 'db.sqlite3')

    if db_path.exists():
        os.remove(Path(BASE_PATH, 'db.sqlite3'))
        print("db.sqlite3 deleted \n")

    for path in dirs:
        # Get all the folder with migrations folder inside
        current_path = Path(path, 'migrations')

        if current_path.exists():
            print(f"Found migrations on {current_path.parent.name}")

            # get all the files inside each migrations folder
            list_file = [i for i in os.scandir(current_path) if i.is_file()]
            print(f"\t Files inside: {len(list_file) - 1} \n")

            for file in list_file:
                # delete all the files inside except for __init__.py
                if not file.name == '__init__.py':
                    os.remove(file.path)
                    print(f"\t -- deleted {file.name} \n")


if __name__ == "__main__":
    main()
