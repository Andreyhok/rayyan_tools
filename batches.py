import os
import random


def random_batches(file, batch_size, output_dir="batches", seed=1111):
    SEED = seed
    random.seed(SEED)
    records = file.read().split('\n\n')
    if len(records[-1]) == 0:
        records.pop(-1)
    n = len(records)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    randomized_indices = random.sample(range(1, (n + 1)), n)
    randomized_records = [records[i - 1] for i in randomized_indices]
    num_batches = (len(randomized_records) + batch_size - 1) // batch_size
    for i in range(num_batches):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(randomized_records))
        batch_records = randomized_records[start_index:end_index]

        output_path = os.path.join(output_dir, f'batch_{i + 1}.ris')
        with open(output_path, 'w') as output_file:
            output_file.write('\n\n'.join(batch_records))
            output_file.write('\n\n')


def get_batches(file, batch_size, output_dir="batches"):
    records = file.read().split('\n\n')
    if len(records[-1]) == 0:
        records.pop(-1)
    n = len(records)
    num_batches = (len(records) + batch_size - 1) // batch_size
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(num_batches):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(records))
        batch_records = records[start_index:end_index]

        output_path = os.path.join(output_dir, f'batch_{i + 1}.ris')
        with open(output_path, 'w') as output_file:
            output_file.write('\n\n'.join(batch_records))
            output_file.write('\n\n')


def main():
    path = input("Please enter path to Rayyan's ris file: ")
    assert os.path.exists(path), "wrong path"
    batch_size = int(input("Please enter batch size: "))
    output_dir = input("Please enter output directory: ")
    while True:
        randomness = input('Please enter "random" if you want your batches to be randomized or "nonrandom" if you don\'t: ')
        with open(path, "r") as file:
            if randomness == "random":
                random_batches(file,batch_size,output_dir)
                print("Batches was created successfully.")
            elif randomness == "nonrandom":
                get_batches(file,batch_size,output_dir)
                print("Batches was created successfully.")
            else:
                print("Please enter random or nonrandom.")
                continue
        break


if __name__ == '__main__':
    main()
