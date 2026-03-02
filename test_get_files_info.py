from functions.get_files_info import get_files_info

def main():
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))

main()