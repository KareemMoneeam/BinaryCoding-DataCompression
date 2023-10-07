seq = input("Enter the sequence: ")
probs = {}
High_Ranges = []
Low_Ranges = []
y = 0
index = {}
for symbol in seq:
    if symbol not in probs.keys():
        p = float(input("Enter P(" + symbol + "): "))
        probs[symbol] = p
        index[symbol] = y
        y += 1

# Calculating Low and High Ranges
LastProb = 0
for symbol in probs.keys():
    Low_Ranges.insert(index[symbol], LastProb)
    High_Ranges.insert(index[symbol], (Low_Ranges[index[symbol]] + list(probs.values())[index[symbol]]))
    LastProb += list(probs.values())[index[symbol]]


# --------------------------------------------------------------------------------------------------------------------
# Compression Function
def compression(seq):
    E = ""
    l = Low_Ranges[0]
    h = High_Ranges[0]
    Range = h - l
    for x in range(len(seq)):
        # Specifying symbols and its High/Low Ranges
        symbol = seq[x]
        LowRange = Low_Ranges[index[symbol]]
        HighRange = High_Ranges[index[symbol]]

        # Scaling
        while (l < 0.5 and h <= 0.5) or (l >= 0.5 and h > 0.5):
            # E1 Condition
            if l < 0.5 and h <= 0.5:
                l = l * 2
                h = h * 2
                E += "0"
                Range = h - l
            # E2 Condition
            if l >= 0.5 and h > 0.5:
                l = (l - 0.5) * 2
                h = (h - 0.5) * 2
                E += "1"
                Range = h - l
        # Calculating Upper and Lower bounds
        h = l + (Range * HighRange)
        l = l + (Range * LowRange)

    # Calculating K value
    # Finding the Smallest Probability
    SmallestProb = min(probs.values())
    k = 1
    while pow(0.5, k) > SmallestProb:
        k += 1

    # Taking random value in the range of last symbol OR just take value 0.5
    # num = random.uniform(h, l)
    num = 0.5

    # Converting the random value from decimal to binary
    binary = ""
    i = k
    while i:
        num *= 2
        fraction_bit = int(num)
        if fraction_bit == 1:
            binary += '1'
            num -= fraction_bit
        else:
            binary += '0'
        i -= 1

    Compressed_Data = E + binary
    return (Compressed_Data, k)


# --------------------------------------------------------------------------------------------------------------------
#  Compression Calling
Compressed_Code = compression(seq)[0]
k = compression(seq)[1]
print("Compressed Code:", Compressed_Code)
print("K:", k)


# --------------------------------------------------------------------------------------------------------------------
# Binary To Decimal Function

def binaryTodecimal(bits):
    decimal = 0
    power = 1
    while bits > 0:
        remainder = bits % 10
        bits = bits // 10     # removes the first bit from the right
        decimal += remainder * power
        power = power * 2

    return decimal

# --------------------------------------------------------------------------------------------------------------------
# Decompression Function
def decompression(k, Compressed_Code, probs):
    i = 0
    while i < len(Compressed_Code):
        k_bits = Compressed_Code[i:k]
        intK_Bits = int(k_bits)
        decimal = (binaryTodecimal(intK_Bits) / pow(2, k))

        lower = Low_Ranges[0]
        upper = High_Ranges[0]
        Range = upper - lower
        Code = (decimal - lower) / Range

        Character = ""
        for x in range(len(seq)):
            # Specifying symbols and its High/Low Ranges
            symbol = seq[x]
            LowRange = Low_Ranges[index[symbol]]
            HighRange = High_Ranges[index[symbol]]
            # Scaling
            while (lower < 0.5 and upper <= 0.5) or (lower >= 0.5 and upper > 0.5):
                # E1 Condition
                if lower < 0.5 and upper <= 0.5:
                    lower = lower * 2
                    upper = upper * 2
                    Range = upper - lower

                # E2 Condition
                if lower >= 0.5 and upper > 0.5:
                    lower = (lower - 0.5) * 2
                    upper = (upper - 0.5) * 2
                    Range = upper - lower

                upper = lower + (Range * HighRange)
                lower = lower + (Range * LowRange)
                Code = (decimal - lower) / Range

            # Calculating Upper and Lower bounds
            for j in range(len(probs)):
                if Low_Ranges[j] < Code < High_Ranges[j]:
                    Character += symbol
        i = i + 1
        k = k + 1
        return Character


# --------------------------------------------------------------------------------------------------------------------
#  Decompression Calling
decompressed_data = decompression(k, Compressed_Code, probs)
print("Decompressed Data:", decompressed_data)
