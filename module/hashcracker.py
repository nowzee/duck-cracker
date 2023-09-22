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
        os.system('cls' if os.name == 'nt' else 'clear')
        print(graffiti)
        print("Method : Dictionary\n")
        print(f"mode : {mode2}")
        print(f"hash algorithm : {algorithm}")
        print(f"{categorie} : {target_hash}\n")

        pbar = tqdm(total=len(word_list), desc="Search in progress")

        for word in word_list:
            if generate_hash(word.strip(), algorithm) == target_hash.lower():
                pbar.close()
                return word
            pbar.update(1)
        pbar.close()
        return None

    elif mode2 == "multi":

        with open(directory2, "r") as hash_file:
            repertory = [line.strip() for line in hash_file]

        hash_lengths = {len(h) for h in repertory}
        results = {hashe.lower(): None for hashe in repertory}

        if algorithm == "Automatically":
            hash_length = hash_lengths.pop()

            if hash_length == 32:
                algorithm = "md5"
            elif hash_length == 40:
                algorithm = "sha1"
            elif hash_length == 56:
                algorithm = "sha224"
            elif hash_length == 64:
                algorithm = "sha256"
            elif hash_length == 96:
                algorithm = "sha384"
            elif hash_length == 128:
                algorithm = "sha512"
            else:
                raise ValueError(f"Longueur de hash non reconnue: {hash_length}")

        found_count = 0
        not_found_count = len(repertory)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(graffiti)
        print("Method : Dictionary\n")
        print(f"mode : {mode2}")
        print(f"hash algorithm : {algorithm}")

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
        os.system('cls' if os.name == 'nt' else 'clear')
        print(graffiti)
        print("Method : Brute-Force\n")
        print(f"Max length : {max_length}")
        print(f"mode : {mode2}")
        print(f"hash algorithm : {algorithm}")
        print(f"{categorie} : {target_hash}\n")

        total_attempts = sum(len(chars) ** i for i in range(1, max_length + 1))

        pbar = tqdm(total=total_attempts, desc="Bruteforce in progress")

        for length in range(1, max_length + 1):
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                pbar.set_postfix(currentpassword=f"{password}")
                current_hash = generate_hash(password, algorithm)
                if current_hash == target_hash.lower():
                    pbar.close()
                    return password
                pbar.update(1)

        pbar.close()
        return None

    elif mode2 == "multi":

        with open(directory2, "r") as hash_file:
            repertory = [line.strip() for line in hash_file]

        hash_lengths = {len(h) for h in repertory}
        results = {hashe.lower(): None for hashe in repertory}

        if algorithm == "Automatically":
            hash_length = hash_lengths.pop()

            if hash_length == 32:
                algorithm = "md5"
            elif hash_length == 40:
                algorithm = "sha1"
            elif hash_length == 56:
                algorithm = "sha224"
            elif hash_length == 64:
                algorithm = "sha256"
            elif hash_length == 96:
                algorithm = "sha384"
            elif hash_length == 128:
                algorithm = "sha512"
            else:
                raise ValueError(f"Longueur de hash non reconnue: {hash_length}")
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(graffiti)
        print("Method : Brute-Force\n")
        print(f"Max length : {max_length}")
        print(f"mode : {mode2}")
        print(f"hash algorithm : {algorithm}")

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
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(graffiti)
                    print("Method : Brute-force\n")
                    print(f"hash type : {algorithm}")
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
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(graffiti)
                    print("Method : dictionary\n")
                    print(f"hash type : {algorithm}")
                    for hashe, word in found_word.items():
                        if word:
                            print(f"{hashe} : {word}")
                        else:
                            print(f"{hashe} : not found")

        elif categorie == "zip":
            print("zip")
    except KeyboardInterrupt:
        exit()
