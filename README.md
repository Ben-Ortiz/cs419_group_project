# cs419_group_project
cs419 computer security group project
encryption

Basic Functionality:

Baseline algorithm for encryption is the vigener cipher. Instead of using a key of letters that repeats, the algorithm uses a pseudorandom sequence equal to the length of the maximum message size that the messenger will allow. This will eliminate the kasisky test as a possible attack as sequence will not repeat. To add further randomness to the ciphertext, the algorithm will also insert a random character at every odd index of the ciphertext. This will make it that the same message encrypted with the same key will not be encrypted the same way twice thus making the algorithm non-deterministic.
