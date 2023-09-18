import hashlib
from tqdm import tqdm
import os
import string
import itertools

graffiti = r"""
    .___             __                                         __                 
  __| _/_ __   ____ |  | __           ________________    ____ |  | __ ___________ 
 / __ |  |  \_/ ___\|  |/ /  ______ _/ ___\_  __ \__  \ _/ ___\|  |/ // __ \_  __ \
/ /_/ |  |  /\  \___|    <  /_____/ \  \___|  | \// __ \\  \___|    <\  ___/|  | \/
\____ |____/  \___  >__|_ \          \___  >__|  (____  /\___  >__|_ \\___  >__|   
     \/           \/     \/              \/           \/     \/     \/    \/       
    """


def generate_hash(input_string, algorithm):
    if algorithm == "md5":
        return hashlib.md5(input_string.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(input_string.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(input_string.encode()).hexdigest()
    elif algorithm == "sha224":
        return hashlib.sha224(input_string.encode()).hexdigest()
    elif algorithm == "sha384":
        return hashlib.sha384(input_string.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(input_string.encode()).hexdigest()
    else:
        raise ValueError(f"Algorithm not supported: {algorithm}")


def load_wordlist(filename, buffer_size=2048 * 2048):
    words = []

    file_size = os.path.getsize(filename)
    progress = tqdm(total=file_size, desc="dictionary loading")

    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        while True:
            data = file.readlines(buffer_size)
            if not data:
                break
            words.extend(data)

            progress.update(buffer_size)

    progress.close()
    return words


def dictionary(target_hash, word_list, algorithm, categorie, mode2, directory2):
    if mode2 == "single":
        print("Method : Dictionary\n")
        print(f"hash type : {algorithm}")
        print(f"{categorie} : {target_hash}\n")

        pbar = tqdm(total=len(word_list), desc="Search in progress")

        for word in word_list:
            if generate_hash(word.strip(), algorithm) == target_hash:
                pbar.close()
                return word
            pbar.update(1)
        pbar.close()
        return None

    elif mode2 == "multi":

        with open(directory2, "r") as hash_file:
            repertory = [line.strip() for line in hash_file]

        results = {}
        for hashe in repertory:
            results[hashe] = None

        found_count = 0
        not_found_count = len(repertory)

        print("\nMethod : Dictionary")
        print(f"hash type : {algorithm}\n")

        pbar = tqdm(total=len(word_list), desc="currently researching")
        pbar.set_postfix(found=f"{found_count}", not_found=f"{not_found_count}")

        for word in word_list:
            current_hash = generate_hash(word.strip(), algorithm)
            if current_hash in results and results[current_hash] is None:
                results[current_hash] = word.strip()
                found_count += 1
                not_found_count -= 1
                pbar.set_postfix(found=f"{found_count}", not_found=f"{not_found_count}")

            if found_count == len(repertory):
                break

            pbar.update(1)

        pbar.close()
        return results


def brute_force(target_hash, algorithm, categorie, mode2, directory2,
                chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    max_length = int(input("define a max length : "))

    if mode2 == "single":

        print("Method : Brute-Force\n")
        print(f"Max length : {max_length}")
        print(f"hash type : {algorithm}")
        print(f"{categorie} : {target_hash}\n")

        total_attempts = sum(len(chars) ** i for i in range(1, max_length + 1))

        pbar = tqdm(total=total_attempts, desc="Bruteforce in progress")

        for length in range(1, max_length + 1):
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                pbar.set_postfix(currentpassword=f"{password}")
                current_hash = generate_hash(password, algorithm)
                if current_hash == target_hash:
                    pbar.close()
                    return password
                pbar.update(1)

        pbar.close()
        return None

    elif mode2 == "multi":
        with open(directory2, "r") as hash_file:
            repertory = [line.strip() for line in hash_file]

        results = {hashe: None for hashe in repertory}

        found_count = 0
        not_found_count = len(repertory)

        total_attempts = sum(len(chars) ** i for i in range(1, max_length + 1))

        pbar = tqdm(total=total_attempts, desc="Bruteforce in progress")
        pbar.set_postfix(found=f"{found_count}", not_found=f"{not_found_count}")

        for length in range(1, max_length + 1):
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                current_hash = generate_hash(password, algorithm)
                if current_hash in results and results[current_hash] is None:
                    results[current_hash] = password
                    found_count += 1
                    not_found_count -= 1
                    pbar.set_postfix(found=f"{found_count}", not_found=f"{not_found_count}")

                if found_count == len(repertory):
                    break

                pbar.update(1)

            if found_count == len(repertory):
                break

        pbar.close()
        return results


def choices(mode, mode2, categorie, algorithm, passwordlists, repertory):
    global target_hash
    try:
        if categorie == "hash":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(graffiti)
            if mode2 == "single":
                target_hash = input("Enter the hash to search: ")

            if algorithm == "Automatically":
                if len(target_hash) == 32:
                    algorithm = "md5"
                elif len(target_hash) == 40:
                    algorithm = "sha1"
                elif len(target_hash) == 56:
                    algorithm = "sha224"
                elif len(target_hash) == 64:
                    algorithm = "sha256"
                elif len(target_hash) == 96:
                    algorithm = "sha384"
                elif len(target_hash) == 128:
                    algorithm = "sha512"

            if mode == "brute-force":

                if mode2 == "single":
                    found_word = brute_force(target_hash, algorithm, categorie, mode2, repertory)
                    if found_word:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(graffiti)
                        print("Method : Brute-force")
                        print(f"\nhash : {target_hash}")
                        print(f"hash type : {algorithm}")
                        print(f"found : {found_word.strip()}")
                    else:
                        print("\nnot found.")
                elif mode2 == "multi":
                    target_hash = None
                    found_word = brute_force(target_hash, algorithm, categorie, mode2, repertory)
                    print("Method : Brute-force\n")
                    for hashe, word in found_word.items():
                        if word:
                            print(f"{hashe} : {word}")
                        else:
                            print(f"{hashe} : not found")
            elif mode == "dictionary":
                word_list = load_wordlist(passwordlists)

                if mode2 == "single":
                    found_word = dictionary(target_hash, word_list, algorithm, categorie, mode2, repertory)
                    if found_word:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(graffiti)
                        print("Method : dictionary")
                        print(f"\nhash : {target_hash}")
                        print(f"hash type : {algorithm}")
                        print(f"found : {found_word.strip()}")

                    else:
                        print("\nnot found in this list.")

                elif mode2 == "multi":
                    target_hash = None
                    found_word = dictionary(target_hash, word_list, algorithm, categorie, mode2, repertory)
                    print("\n")
                    for hashe, word in found_word.items():
                        if word:
                            print(f"{hashe} : {word}")
                        else:
                            print(f"{hashe} : not found")

        elif categorie == "zip":
            print("zip")
    except KeyboardInterrupt:
        exit()


def settings():
    try:
        # noinspection PyGlobalUndefined
        global passwordlist, mode2s, directory

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
        else:
            print("in dev")
            exit()

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

        print(graffiti)
        os.system('cls' if os.name == 'nt' else 'clear')

        choices(modes, mode2s, categories, algorithm, passwordlist, directory)
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    settings()
