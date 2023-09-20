import os
import argparse
import module.hashcracker
graffiti = r"""
    .___             __                                         __                 
  __| _/_ __   ____ |  | __           ________________    ____ |  | __ ___________ 
 / __ |  |  \_/ ___\|  |/ /  ______ _/ ___\_  __ \__  \ _/ ___\|  |/ // __ \_  __ \
/ /_/ |  |  /\  \___|    <  /_____/ \  \___|  | \// __ \\  \___|    <\  ___/|  | \/
\____ |____/  \___  >__|_ \          \___  >__|  (____  /\___  >__|_ \\___  >__|   
     \/           \/     \/              \/           \/     \/     \/    \/       
    """


def settings():
    try:
        # noinspection PyGlobalUndefined
        global passwordlist, mode2s, directory, target_hash

        os.system('cls' if os.name == 'nt' else 'clear')

        print(graffiti)
        print("catégories : ")
        print("1: zip (do not work)")
        print("2: hash")

        categorie = input("select your categorie : ")

        if categorie == "1":
            categories = "zip"
        elif categorie == "2":
            categories = "hash"
        else:
            print("categories not valid.")
            return

        os.system('cls' if os.name == 'nt' else 'clear')

        print(graffiti)

        if categorie == "2":
            print("Select hash type :")
            print("0: Automatically search ")
            print("1: MD5")
            print("2: SHA-1")
            print("3: SHA-256")
            print("4: SHA-224")
            print("5: SHA-384")
            print("6: SHA-512")

            types = input("Enter your choice (1/2/3/4): ")

            if types == "1":
                algorithm = "md5"
            elif types == "0":
                algorithm = "Automatically"
            elif types == "2":
                algorithm = "sha1"
            elif types == "3":
                algorithm = "sha256"
            elif types == "4":
                algorithm = "sha224"
            elif types == "5":
                algorithm = "sha384"
            elif types == "6":
                algorithm = "sha512"
            else:
                print("choice not valid.")
                return

            os.system('cls' if os.name == 'nt' else 'clear')
            print(graffiti)
            print("mode : ")
            print("1: single hash")
            print("2: multi hash (add a file containing multiple hashes)")

            mode2 = input("select your mode : ")

            if mode2 == "1":
                mode2s = "single"
                directory = None
            elif mode2 == "2":
                mode2s = "multi"
                directory = input("enter directory to list : ")
            else:
                print("Directory not valid.")
                return

        else:
            print("in dev")
            exit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print(graffiti)
        print("attack method : ")
        print("1: Brute-force")
        print("2: dictionary")
        mode = input("select your method attack : ")

        os.system('cls' if os.name == 'nt' else 'clear')

        print(graffiti)

        if mode == "1":
            modes = "brute-force"
            passwordlist = None
        elif mode == "2":
            modes = "dictionary"
            passwordlist = input("enter password list : ")
        else:
            print("method not valid.")
            passwordlist = None
            return

        print(graffiti)
        os.system('cls' if os.name == 'nt' else 'clear')
        module.hashcracker.choices(modes, mode2s, categories, algorithm, passwordlist, directory)
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    settings()
