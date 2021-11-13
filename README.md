# cs419 computer security group project

encryption

Basic Functionality:

Baseline algorithm for encryption is the vigener cipher. Instead of using a key of letters that repeats, the algorithm uses a pseudorandom sequence equal to the length of the maximum message size that the messenger will allow. This will eliminate the kasisky test as a possible attack as sequence will not repeat. To add further randomness to the ciphertext, the algorithm will also insert a random character at every odd index of the ciphertext. This will make it that the same message encrypted with the same key will not be encrypted the same way twice thus making the algorithm non-deterministic.

Future Plans:

Instead of inserting numbers completely randomly, create a probability distribution that makes some letters much more likely to be inserted than others. This will create the illusion of patterns being present in the encrypted text. If an attacker were to try to run a frequency analysis on the ciphertext the frequencies of the letters will all be thrown off by the inserted letters. Note that for a frequency analysis to even be somewhat effective on this encryption scheme an extremly large amount of ciphertext woul need to be captured.

There will also be multiple keys asscoiated with each user in the chatroom. How these keys will rotate I'm not sure of yet. Possible ideas are rotating the keys by message such that each message is encrypted by a different key until the keys repeat. Another possibility is to keep the server and client in sync timewise and rotate the keys every x amount of time. 