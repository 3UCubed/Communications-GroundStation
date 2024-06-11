//this generates the index and the float number into a file to be read by python code

#include <iostream>
#include <fstream>
#include <vector>

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

    // Write data to a CSV file
    std::ofstream outputFile("data.csv");
    for (int i = 0; i < data.size(); ++i) {
        outputFile << i << "," << data[i] << std::endl;
    }
    outputFile.close();

    // Output the data read from the file
    std::cout << "Data read from file: " << std::endl;
    for (int i = 0; i < data.size(); ++i) {
        std::cout << i << ": " << data[i] << std::endl;
    }

    return 0;
}
