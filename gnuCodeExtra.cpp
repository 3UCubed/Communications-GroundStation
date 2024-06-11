//this generates the float to binary and splits the components
//including sign bit, exponent, and the mantissa
#include <iostream>
#include <cstring>
#include <fstream>
#include <vector>
#include <bitset>
#include <iomanip>
#include <cmath>

// Function to convert a float to its binary representation and extract its parts
void floatToBinaryParts(float value) {
    // Interpret the float's binary representation as an integer
    uint32_t intValue;
    std::memcpy(&intValue, &value, sizeof(float));

    // Convert the integer to its binary representation
    std::bitset<sizeof(float) * 8> binary(intValue);

    // Extract sign, exponent, and mantissa
    uint32_t sign = (intValue >> 31) & 0x1;
    uint32_t exponent = (intValue >> 23) & 0xFF;
    uint32_t mantissa = intValue & 0x7FFFFF;

    // Print the parts
	std::cout << "Float: " << value << " -> Binary: " << binary.to_string() << std::endl;
    std::cout << "  Sign: " << sign << std::endl;
    std::cout << "  Exponent: " << std::bitset<8>(exponent) << " (decimal: " << exponent << ")" << std::endl;
    std::cout << "  Mantissa: " << std::bitset<23>(mantissa) << std::endl;
}

int main() {
    std::string filename;
    std::cout << "Enter the filename: ";
    std::cin >> filename;

    // Read file info
    std::ifstream file(filename, std::ios::binary);

    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return 1;
    }

    std::vector<float> data;
    float value;
    while (file.read(reinterpret_cast<char*>(&value), sizeof(float))) {
        data.push_back(value);
    }
    file.close();

    // Output the data read from the file
    std::cout << "Data read from file: " << std::endl;
    for (float val : data) {
        floatToBinaryParts(val);
    }

    return 0;
}
